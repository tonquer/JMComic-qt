import concurrent.futures
import ipaddress
import socket
import threading
import time

from curl_cffi import requests as curl_requests

from config.setting import Setting
from tools.log import Log
from tools.singleton import Singleton

# 优先用国内能直连的 DoH。Cloudflare 的 DoH 在墙内基本不通，
# 用户自己配的地址排在最后，作为以上都失败时的补充
DEFAULT_DOH_SERVERS = [
    "https://doh.pub/dns-query",
    "https://dns.alidns.com/resolve",
]

DOH_TIMEOUT = 3
PIN_TTL = 1800  # 解析结果缓存 30 分钟，出错会提前作废
FAIL_TTL = 180  # 解析失败后 3 分钟内不再为同一域名重复查询
WAIT_TIMEOUT = 5  # 同域名的其它请求最多等这么久，不陪着一起卡死
PROBE_TIMEOUT = 1.5  # 探测 IP 的 443 是否可连
MAX_PROBE_NUM = 4


class DnsResolver(Singleton):
    """系统 DNS 不可信时的兜底解析。

    只有在请求已经失败之后才会被调用，网络正常时不产生任何额外开销。
    解析出来的 IP 交给 curl 的 RESOLVE 固定，URL 里的域名不做替换，
    这样 TLS 的 SNI / Host 依然是原域名，不会因为“拿 IP 直连”被 CF 拒绝。
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._pins = {}  # host: (ip, expire)
        self._fails = {}  # host: expire
        self._inflight = {}  # host: threading.Event
        # 代次：Clear()/Invalidate() 时 +1，让在途解析的结果作废，
        # 避免旧线程在缓存清空之后又把刚判死的 IP 写回去
        self._generation = 0

    def GetCached(self, host):
        if not host:
            return ""
        with self._lock:
            item = self._pins.get(host)
            if not item:
                return ""
            if item[1] <= time.time():
                self._pins.pop(host, None)
                return ""
            return item[0]

    def Resolve(self, host):
        if not host:
            return ""
        try:
            ipaddress.ip_address(host)
            return host
        except ValueError:
            pass

        now = time.time()
        with self._lock:
            item = self._pins.get(host)
            if item and item[1] > now:
                return item[0]
            if self._fails.get(host, 0) > now:
                return ""
            event = self._inflight.get(host)
            if event is None:
                event = threading.Event()
                self._inflight[host] = event
                isOwner = True
            else:
                isOwner = False

        if not isOwner:
            # 同一域名只发一次 DoH 查询，其它线程等结果
            event.wait(WAIT_TIMEOUT)
            return self.GetCached(host)

        ip = ""
        cacheable = False
        with self._lock:
            generation = self._generation
        try:
            ip, cacheable = self._Query(host)
        except Exception as es:
            Log.Error(es)
        finally:
            with self._lock:
                self._inflight.pop(host, None)
                # 代次已变（期间发生过 Clear/Invalidate）就不再写回，
                # 旧结果很可能已经不可信
                if generation == self._generation:
                    if ip and cacheable:
                        self._pins[host] = (ip, time.time() + PIN_TTL)
                        self._fails.pop(host, None)
                    elif not ip:
                        self._fails[host] = time.time() + FAIL_TTL
                    # ip 存在但没通过探活（最后手段）时不写缓存：
                    # 下一次失败会重新解析，而不是沿用这个死地址 30 分钟
            event.set()
        return ip

    def Invalidate(self, host):
        with self._lock:
            self._pins.pop(host, None)
            self._generation += 1

    def GetPins(self):
        now = time.time()
        with self._lock:
            return {host: item[0] for host, item in self._pins.items() if item[1] > now}

    def Clear(self):
        with self._lock:
            self._pins.clear()
            self._fails.clear()
            self._generation += 1

    def _GetServers(self):
        servers = list(DEFAULT_DOH_SERVERS)
        address = Setting.DohAddress.value
        if address and address.startswith("http") and address not in servers:
            servers.append(address)
        return servers

    def _Query(self, host):
        """依次问每个 DoH 源，返回 (ip, cacheable)。

        候选必须通过 443 探活才采用（并缓存）；一个源的候选全不可达时
        换下一个源。所有源都全军覆没时，把第一个源的首个候选当最后手段
        交出去——但不缓存，本次失败后下一次会重新解析。
        """
        fallback = ""
        for server in self._GetServers():
            answers = self._QueryServer(server, host)
            if not answers:
                continue
            ip = self._PickReachable(answers[:MAX_PROBE_NUM])
            if ip:
                Log.Info("doh resolve, host:{} -> {}, all:{}".format(host, ip, answers))
                return ip, True
            if not fallback:
                fallback = answers[0]
                Log.Warn("doh candidates all unreachable, try next server, host:{}, all:{}".format(host, answers))
        if fallback:
            Log.Warn("doh probe failed on every server, last resort, host:{}".format(host))
        else:
            Log.Warn("doh resolve failed, host:{}".format(host))
        return fallback, False

    @staticmethod
    def _QueryServer(server, host):
        sep = "&" if "?" in server else "?"
        url = "{}{}name={}&type=A".format(server, sep, host)
        try:
            resp = curl_requests.get(url, headers={"accept": "application/dns-json"},
                                     timeout=DOH_TIMEOUT,
                                     # 系统 DNS 已经不可信，DoH 不能再走可能失效的系统代理
                                     proxies={"http": "", "https": ""})
            if resp.status_code != 200:
                return []
            data = resp.json()
        except Exception as es:
            Log.Debug("doh query {} failed: {}".format(server, es))
            return []

        answers = []
        for info in data.get("Answer") or []:
            if info.get("type") != 1:
                continue
            addr = str(info.get("data", ""))
            try:
                ipaddress.IPv4Address(addr)
            except ValueError:
                continue
            if addr not in answers:
                answers.append(addr)
        return answers

    @staticmethod
    def _PickReachable(candidates):
        """并发 TCP 探活，返回最快的可用 IP，全失败返回 ""。

        注意这只证明 443 端口能握手，不代表 TLS/业务可用；
        单个候选也要探——一个域名只解析出一个死 IP 很常见。
        """
        if len(candidates) <= 1:
            return candidates[0] if candidates and DnsResolver._Probe(candidates[0]) is not None else ""

        results = []
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(candidates))
        try:
            futures = {pool.submit(DnsResolver._Probe, ip): ip for ip in candidates}
            for future in concurrent.futures.as_completed(futures, timeout=PROBE_TIMEOUT + 1):
                delay = future.result()
                if delay is not None:
                    results.append((delay, futures[future]))
        except Exception:
            pass
        finally:
            pool.shutdown(wait=False)

        if not results:
            return ""
        results.sort()
        return results[0][1]

    @staticmethod
    def _Probe(ip):
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(PROBE_TIMEOUT)
        try:
            sock.connect((ip, 443))
            return time.time() - start
        except OSError:
            return None
        finally:
            sock.close()
