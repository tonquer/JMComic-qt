import json
import pickle
import threading
from queue import Queue
from curl_cffi import requests as requests2, CurlOpt

import server.req as req
import server.res as res
from config import config
from config.global_config import GlobalConfig
from qt_owner import QtOwner
from task.qt_task import TaskBase
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import ToolUtil
import socket
import httpx
import urllib


host_table = {}
_orig_getaddrinfo = socket.getaddrinfo
# 如果使用代理，無法使用自定義dns
def getaddrinfo2(host, port, *args, **kwargs):
    if host in host_table:
        address = host_table[host]
        Log.Info("dns parse, host:{}->{}".format(host, address))
    else:
        address = host
    results = _orig_getaddrinfo(address, port, *args, **kwargs)
    return results
socket.getaddrinfo = getaddrinfo2


def handler(request):
    def generator(handler):
        Server().handler[request.__name__] = handler()
        return handler
    return generator


class NewSession(requests2.Session):
    def __init__(self, **kwargs):
        requests2.Session.__init__(self, **kwargs)

    def _set_curl_options(self, *args, **kwargs):
        c = args[0]
        if GlobalConfig.WebDnsList.value:
            c.setopt(CurlOpt.RESOLVE, GlobalConfig.WebDnsList.value)
        # c.setopt(CurlOpt.SSL_OPTIONS, CurlOpt.ALLO)
        # c.setopt(CurlOpt.SSLVERSION, 6)
        # c.setopt(CurlOpt.SSL_VERIFYHOST, False)
        # c.setopt(CurlOpt.SSL_VERIFYPEER, False)
        return requests2.Session._set_curl_options(self, *args, **kwargs)


class Task(object):
    def __init__(self, request, backParam="", cacheAndLoadPath="", loadPath=""):
        self.req = request
        self.res = None
        self.timeout = 5
        self.backParam = backParam
        self.status = Status.Ok
        self.cacheAndLoadPath = cacheAndLoadPath
        self.loadPath = loadPath

    @property
    def bakParam(self):
        return self.backParam

    def GetText(self):
        if not self.res:
            return ""
        if hasattr(self.res, "raw"):
            return getattr(self.res.raw, "text", "")
        return ""


class Server(Singleton):
    def __init__(self) -> None:
        Singleton.__init__(self)
        self.handler = {}
        self.session = NewSession()
        self.session2 = NewSession()
        # self.session2 = cloudscraper.session()
        self.address = ""
        self.imageServer = ""

        self.token = ""
        self._inQueue = Queue()
        self._downloadQueue = Queue()
        self.threadHandler = 0
        self.threadNum = config.ThreadNum
        self.downloadNum = config.DownloadThreadNum
        self.threadSession = []
        self.downloadSession = []

        for i in range(self.threadNum):
            self.threadSession.append(httpx.Client(http2=True, verify=False, trust_env=False))
            thread = threading.Thread(target=self.Run, args=[i])
            thread.setName("HTTP-"+str(i))
            thread.setDaemon(True)
            thread.start()

        for i in range(self.downloadNum):
            self.downloadSession.append(httpx.Client(http2=True, verify=False, trust_env=False))
            thread = threading.Thread(target=self.RunDownload, args=[i])
            thread.setName("Download-" + str(i))
            thread.setDaemon(True)
            thread.start()

    def Run(self, index):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._Send(task, index)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")

    def RunDownload(self, index):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                if task == "":
                    break
                self._Download(task, index)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, address, imageAddress, loginProxy=""):
        for domain in GlobalConfig.Url2List.value:
            domain = ToolUtil.GetUrlHost(domain)
            if ToolUtil.IsipAddress(address):
                host_table[domain] = address
            elif not address and domain in host_table:
                host_table.pop(domain)

        for domain in GlobalConfig.PicUrlList.value:
            domain = ToolUtil.GetUrlHost(domain)
            if ToolUtil.IsipAddress(imageAddress):
                host_table[domain] = imageAddress
            elif not imageAddress and domain in host_table:
                host_table.pop(domain)
        domain = ToolUtil.GetUrlHost(GlobalConfig.Url.value)
        if loginProxy:
            host_table[domain] = loginProxy
        else:
            if loginProxy in host_table:
                host_table.pop(domain)

        # 换一个，清空pool
        # self.session = requests.session()
        return

    def ClearDns(self):
        host_table.clear()

    def UpdateProxy(self):
        from config.setting import Setting
        self.UpdateProxy2(Setting.IsHttpProxy.value, Setting.HttpProxy.value, Setting.Sock5Proxy.value)

    def UpdateProxy2(self, httpProxyIndex, httpProxy, sock5Proxy):
        from tools.str import Str
        # sock5代理
        if httpProxyIndex == 2 and sock5Proxy:
            data = sock5Proxy.replace("http://", "").replace("https://", "").replace("sock5://",
                                                                                                   "").replace(
                "socks5://", "")
            trustEnv = False
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                proxy = f"socks5://{host}:{port}"
            else:
                return Str.Sock5Error
        # http代理
        elif httpProxyIndex == 1 and httpProxy:
            proxy = httpProxy
            trustEnv = False
        # 系统代理
        elif httpProxyIndex == 3:
            proxy = None
            proxyDict = urllib.request.getproxies()
            if isinstance(proxyDict, dict) and proxyDict.get("http"):
                proxy = proxyDict.get("http")

            trustEnv = False
        # 其他
        else:
            trustEnv = False
            proxy = None
        Log.Warn(f"update proxy, index:{httpProxyIndex}, proxy:{proxy}, env:{trustEnv}")

        self.threadSession = []
        for i in range(self.threadNum):
            self.threadSession.append(httpx.Client(http2=True, verify=False, trust_env=trustEnv, proxy=proxy))

        self.downloadSession = []
        for i in range(self.downloadNum):
            self.downloadSession.append(httpx.Client(http2=True, verify=False, trust_env=trustEnv, proxy=proxy))
        return
    
    def __DealHeaders(self, request, token):

        if not request.isUseHttps:
            request.url = request.url.replace("https://", "http://")

        if request.proxyUrl:
            host = ToolUtil.GetUrlHost(request.url)
            request.url = request.url.replace(host, request.proxyUrl+"/"+host)

    def Send(self, request, token="", backParam="", isASync=True, index=0):
        self.__DealHeaders(request, token)
        if isinstance(request, req.SpeedTestReq):
            if isASync:
                return self._downloadQueue.put(Task(request, backParam))
            else:
                return self._Download(Task(request, backParam), index)
        else:
            if isASync:
                return self._inQueue.put(Task(request, backParam))
            else:
                return self._Send(Task(request, backParam), index)

    def _Send(self, task, index):
        try:
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                data = {"st": Status.OfflineModel, "data": ""}
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
                return

            if task.req.method.lower() == "post":
                self.Post(task, index)
            elif task.req.method.lower() == "post2":
                self.Post2(task)
            elif task.req.method.lower() == "get":
                self.Get(task, index)
            elif task.req.method.lower() == "get2":
                self.Get2(task)
            elif task.req.method.lower() == "put":
                self.Put(task, index)
            else:
                return
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(f"error:{task.req.url}")
            Log.Error(es)
        finally:
            Log.Info("response-> backId:{}, {}, st:{}, {}".format(task.backParam, task.req.__class__.__name__, task.status, task.res))
        try:
            self.handler.get(task.req.__class__.__name__)(task)
            # if isinstance(task.res.raw, requests2.Response):
            #     task.res.raw.close()
        except Exception as es:
            task.status = Status.NetError
            # Log.Error(es)
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            return task.res

    def Post(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        session = self.threadSession[index]
        task.res = res.BaseRes("", False)
        if task.req.cookies:
            r = session.post(request.url, follow_redirects=True, headers=request.headers, timeout=task.timeout, extensions=request.extend, cookies=task.req.cookies, data=request.params)
        else:
            r = session.post(request.url, follow_redirects=True, headers=request.headers, timeout=task.timeout, extensions=request.extend, data=request.params)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Post2(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        if task.req.cookies:
            r = self.session2.post(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, data=request.params,
                                  timeout=task.timeout, verify=False, cookies=task.req.cookies)
        else:
            r = self.session2.post(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, data=request.params,
                                  timeout=task.timeout, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Put(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        session = self.threadSession[index]
        r = session.put(request.url, follow_redirects=True, headers=request.headers, data=request.params, timeout=15, extensions=request.extend)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task, index=0):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        session = self.threadSession[index]
        if task.req.cookies:
            r = session.get(request.url, follow_redirects=True, headers=request.headers, timeout=task.timeout, extensions=request.extend, cookies=task.req.cookies)
        else:
            r = session.get(request.url, follow_redirects=True, headers=request.headers, timeout=task.timeout, extensions=request.extend)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get2(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}
        task.res = res.BaseRes("", False)

        if task.req.cookies:
            r = self.session2.get(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, timeout=task.timeout, cookies=task.req.cookies)
        else:
            r = self.session2.get(request.url, proxies=request.proxy, impersonate="chrome110", headers=request.headers, timeout=task.timeout)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Download(self, request, token="", backParams="", cacheAndLoadPath="", loadPath= "", isASync=True):
        self.__DealHeaders(request, token)
        task = Task(request, backParams, cacheAndLoadPath, loadPath)
        if isASync:
            self._downloadQueue.put(task)
        else:
            self._Download(task, 0)

    def ReDownload(self, task):
        task.res = ""
        task.status = Status.Ok
        self._downloadQueue.put(task)

    def _Download(self, task, index):
        try:
            task.req.resetCnt -= 1
            if not task.req.isReload:
                if not isinstance(task.req, req.SpeedTestReq) and not task.req.savePath:
                    for cachePath in [task.req.loadPath, task.req.cachePath]:
                        if cachePath and task.bakParam:
                            data = ToolUtil.LoadCachePicture(cachePath)
                            if data:
                                TaskBase.taskObj.downloadBack.emit(task.bakParam, 0, len(data), b"")
                                TaskBase.taskObj.downloadBack.emit(task.bakParam, 0, 0, data)
                                Log.Info("request cache -> backId:{}, {}".format(task.bakParam, task.req))
                                return

            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                self.handler.get(task.req.__class__.__name__)(task)
                return

            request = task.req
            if request.params == None:
                request.params = {}

            if request.headers == None:
                request.headers = {}
            if not request.isReset:
                Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            else:
                Log.Info("request reset:{} -> backId:{}, {}".format(task.req.resetCnt, task.bakParam, task.req))
            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = None
            task.index = index
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            if (task.req.resetCnt > 0):
                task.req.isReset = True
                self.ReDownload(task)
                return
        self.handler.get(task.req.__class__.__name__)(task)
        if task.res:
            task.res.close()

    def TestSpeed(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        self._inQueue.put(task)
