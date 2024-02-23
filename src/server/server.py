import json
import pickle
import threading
from queue import Queue

# import cloudscraper
import requests

from curl_cffi import requests as requests2, CurlOpt

import urllib3
from curl_cffi._wrapper import lib
from urllib3.util.ssl_ import is_ipaddress

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

urllib3.disable_warnings()


from urllib3.util import connection
_orig_create_connection = connection.create_connection

host_table = {}


def _dns_resolver(host):
    if host in host_table:
        address = host_table[host]
        Log.Info("dns parse, host:{}->{}".format(host, address))
        return address
    else:
        return host


def patched_create_connection(address, *args, **kwargs):
    host, port = address
    hostname = _dns_resolver(host)
    return _orig_create_connection((hostname, port), *args, **kwargs)


connection.create_connection = patched_create_connection


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
        self.session = requests.session()
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

        for i in range(self.threadNum):
            thread = threading.Thread(target=self.Run)
            thread.setName("HTTP-"+str(i))
            thread.setDaemon(True)
            thread.start()

        for i in range(self.downloadNum):
            thread = threading.Thread(target=self.RunDownload)
            thread.setName("Download-" + str(i))
            thread.setDaemon(True)
            thread.start()

    def Run(self):
        while True:
            task = self._inQueue.get(True)
            self._inQueue.task_done()
            try:
                if task == "":
                    break
                self._Send(task)
            except Exception as es:
                Log.Error(es)
        pass

    def Stop(self):
        for i in range(self.threadNum):
            self._inQueue.put("")
        for i in range(self.downloadNum):
            self._downloadQueue.put("")

    def RunDownload(self):
        while True:
            task = self._downloadQueue.get(True)
            self._downloadQueue.task_done()
            try:
                if task == "":
                    break
                self._Download(task)
            except Exception as es:
                Log.Error(es)
        pass

    def UpdateDns(self, address, imageAddress, loginProxy=""):
        for domain in GlobalConfig.Url2List.value:
            domain = ToolUtil.GetUrlHost(domain)
            if is_ipaddress(address):
                host_table[domain] = address
            elif not address and domain in host_table:
                host_table.pop(domain)

        for domain in GlobalConfig.PicUrlList.value:
            domain = ToolUtil.GetUrlHost(domain)
            if is_ipaddress(imageAddress):
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
        self.session = requests.session()
        return

    def ClearDns(self):
        host_table.clear()

    def __DealHeaders(self, request, token):
        host = ToolUtil.GetUrlHost(request.url)

        if not request.isUseHttps:
            request.url = request.url.replace("https://", "http://")

        if request.proxyUrl:
            request.url = request.url.replace(host, request.proxyUrl+"/"+host)

    def Send(self, request, token="", backParam="", isASync=True):
        self.__DealHeaders(request, token)
        if isinstance(request, req.SpeedTestReq):
            if isASync:
                return self._downloadQueue.put(Task(request, backParam))
            else:
                return self._Download(Task(request, backParam))
        else:
            if isASync:
                return self._inQueue.put(Task(request, backParam))
            else:
                return self._Send(Task(request, backParam))

    def _Send(self, task):
        try:
            Log.Info("request-> backId:{}, {}".format(task.bakParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                data = {"st": Status.OfflineModel, "data": ""}
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
                return

            if task.req.method.lower() == "post":
                self.Post(task)
            elif task.req.method.lower() == "post2":
                self.Post2(task)
            elif task.req.method.lower() == "get":
                self.Get(task)
            elif task.req.method.lower() == "get2":
                self.Get2(task)
            elif task.req.method.lower() == "put":
                self.Put(task)
            else:
                return
        except Exception as es:
            task.status = Status.NetError
            # Log.Error(es)
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            Log.Info("response-> backId:{}, {}, st:{}, {}".format(task.backParam, task.req.__class__.__name__, task.status, task.res))
        try:
            self.handler.get(task.req.__class__.__name__)(task)
            if isinstance(task.res.raw, requests.Response):
                task.res.raw.close()
        except Exception as es:
            if isinstance(es, requests.exceptions.ConnectTimeout):
                task.status = Status.ConnectErr
            elif isinstance(es, requests.exceptions.ReadTimeout):
                task.status = Status.TimeOut
            elif isinstance(es, requests.exceptions.SSLError):
                if "WSAECONNRESET" in es.__repr__():
                    task.status = Status.ResetErr
                else:
                    task.status = Status.SSLErr
            elif isinstance(es, requests.exceptions.ProxyError):
                task.status = Status.ProxyError
            elif isinstance(es, ConnectionResetError):
                task.status = Status.ResetErr
            else:
                task.status = Status.NetError
            # Log.Error(es)
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            return task.res

    def Post(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        if task.req.cookies:
            r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params,
                                  timeout=task.timeout, verify=False, cookies=task.req.cookies)
        else:
            r = self.session.post(request.url, proxies=request.proxy, headers=request.headers, data=request.params,
                                  timeout=task.timeout, verify=False)
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

    def Put(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        r = self.session.put(request.url, proxies=request.proxy, headers=request.headers, data=request.params, timeout=60, verify=False)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    def Get(self, task):
        request = task.req
        if request.params == None:
            request.params = {}

        if request.headers == None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        if task.req.cookies:
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout,
                                 verify=False, cookies=task.req.cookies)
        else:
            r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout,
                                 verify=False)
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
            self._Download(task)

    def ReDownload(self, task):
        task.res = ""
        task.status = Status.Ok
        self._downloadQueue.put(task)

    def _Download(self, task):
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

            history = []
            for i in range(10):
                r = self.session.get(request.url, proxies=request.proxy, headers=request.headers, timeout=task.timeout,
                                     verify=False, allow_redirects=False, stream=True)
                if r.status_code == 302 or r.status_code == 301:
                    next = r.headers.get('Location')
                    if ToolUtil.GetUrlHost(next) == "":
                        next = "https://" + ToolUtil.GetUrlHost(request.url) + next
                    request.url = next
                    if not request.isReset:
                        Log.Info("request 301 -> backId:{}, {}".format(task.bakParam, task.req))
                    else:
                        Log.Info("request 301 reset:{} -> backId:{}, {}".format(task.req.resetCnt, task.bakParam, task.req))

                    history.append(r)
                    self.__DealHeaders(request, "")
                else:
                    break
            r.history = history
            # task.res = res.BaseRes(r)
            # print(r.elapsed.total_seconds())
            task.res = r
        except Exception as es:
            if isinstance(es, requests.exceptions.ConnectTimeout):
                task.status = Status.ConnectErr
            elif isinstance(es, requests.exceptions.ReadTimeout):
                task.status = Status.TimeOut
            elif isinstance(es, requests.exceptions.SSLError):
                if "WSAECONNRESET" in es.__repr__():
                    task.status = Status.ResetErr
                else:
                    task.status = Status.SSLErr
            elif isinstance(es, requests.exceptions.ProxyError):
                task.status = Status.ProxyError
            elif isinstance(es, ConnectionResetError):
                task.status = Status.ResetErr
            else:
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
        task.timeout = 2
        self._downloadQueue.put(task)

    def TestSpeedPing(self, request, bakParams=""):
        self.__DealHeaders(request, "")
        task = Task(request, bakParams)
        task.timeout = 2
        self._inQueue.put(task)
