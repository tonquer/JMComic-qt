import base64
import hashlib
import json
import urllib.request

from config.global_config import GlobalConfig
from tools.log import Log

# 禁漫官方的域名服务器（同一份列表也会被 jmcomic 库的
# JmModuleConfig.API_URL_DOMAIN_SERVER_LIST 使用）。
# 返回内容为 base64 + AES-256-ECB 加密的 JSON：{"Server": [域名, ...]}
DOMAIN_SERVER_LIST = [
    "https://rup4a04-c01.tos-ap-southeast-1.bytepluses.com/newsvr-2025.txt",
    "https://rup4a04-c02.tos-cn-hongkong.bytepluses.com/newsvr-2025.txt",
]
DOMAIN_SERVER_SECRET = "diosfjckwpqpdfjkvnqQjsik"

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def decode_resp_data(data, secret):
    """解密域名服务器返回值（与禁漫接口数据同一种加密方式）"""
    from Cryptodome.Cipher import AES
    data_b64 = base64.b64decode(data)
    key = hashlib.md5(secret.encode("utf-8")).hexdigest().encode("utf-8")
    decrypted = AES.new(key, AES.MODE_ECB).decrypt(data_b64)
    # 去掉 PKCS#7 padding
    return decrypted[:-decrypted[-1]].decode("utf-8")


def _request(url, timeout, useProxy):
    # 用 curl_cffi 而不是 urllib：macOS 上 python.org 版解释器常常缺少
    # 系统 CA 根证书，urllib 会直接 SSL 校验失败
    from curl_cffi import requests as cffiRequests
    if useProxy:
        raw = urllib.request.getproxies()
        proxy = raw.get("http") or raw.get("https") if isinstance(raw, dict) else None
        if not proxy:
            raise ValueError("no system proxy")
        proxies = {"http": proxy, "https": proxy}
    else:
        # 显式置空，忽略环境变量和系统代理
        proxies = {"http": None, "https": None}

    resp = cffiRequests.get(url, timeout=timeout, proxies=proxies,
                            headers={"User-Agent": USER_AGENT},
                            impersonate="chrome110")
    if resp.status_code != 200:
        raise ValueError("unexpected status {0}".format(resp.status_code))
    return resp.text


def fetch_latest_api_domains(timeout=10):
    """拉取最新可用的 API 域名列表，失败返回 []"""
    for url in DOMAIN_SERVER_LIST:
        # 先直连再走系统代理：这条请求是用来"自救"的，
        # 不能依赖系统代理本身可用
        for useProxy in (False, True):
            try:
                text = _request(url, timeout, useProxy)
                while text and not text[0].isascii():
                    text = text[1:]
                data = json.loads(decode_resp_data(text, DOMAIN_SERVER_SECRET))
                servers = data.get("Server")
                if servers:
                    # 统一成带 https:// 的形式，和应用里 Url2List 的格式保持一致
                    result = []
                    for server in servers:
                        server = str(server).strip()
                        if not server:
                            continue
                        if not server.startswith("http"):
                            server = "https://" + server
                        result.append(server)
                    if result:
                        return result
            except Exception as es:
                Log.Debug("fetch api domain failed, {0} proxy={1}: {2}".format(url, useProxy, es))
                continue
    return []


def apply_api_domains(domains):
    """把域名列表应用到 GlobalConfig，并保证线路索引不越界"""
    from config.setting import Setting
    if not domains:
        return
    GlobalConfig.Url2List.set_value(list(domains))
    for name in ("ProxySelectIndex", "ProxyImgSelectIndex", "RegisterProsyIndex"):
        item = getattr(Setting, name)
        if item.value < 1 or item.value > len(domains):
            item.SetValue(1)


def apply_saved_domains():
    """启动时把上次拉取到的域名列表恢复进 GlobalConfig"""
    from config.setting import Setting
    saved = Setting.ApiDomainListOverride.value
    if not saved:
        return False
    domains = [d.strip() for d in str(saved).split(",") if d.strip()]
    if not domains:
        return False
    apply_api_domains(domains)
    return True


def update_api_domains():
    """拉取并应用最新的 API 域名列表，返回是否发生了更新"""
    latest = fetch_latest_api_domains()
    if not latest:
        return False

    current = list(GlobalConfig.Url2List.value)
    if sorted(latest) == sorted(current):
        Log.Info("api domain already up to date: {0}".format(current))
        return False

    from config.setting import Setting
    apply_api_domains(latest)
    Setting.ApiDomainListOverride.SetValue(",".join(latest))
    Setting.SaveSetting()
    Log.Warn("api domain updated: {0} -> {1}".format(current, latest))
    return True
