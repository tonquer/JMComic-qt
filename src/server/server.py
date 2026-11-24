import asyncio
import inspect
import pickle

from curl_cffi import CurlInfo

import server.req as req
import server.res as res
from config import config
from config.global_config import GlobalConfig
from qt_owner import QtOwner
from server.async_loop import AsyncLoopRunner, CreateDefaultEventLoop
from server.error import ClassifyRequestError
from server.session_pool import AsyncSessionPool, CURL_INFOS
from task.qt_task import TaskBase
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status
from tools.tool import ToolUtil

host_table = {}

_SPEED_REQ_TYPES = (req.SpeedTestReq, req.SpeedTestPingReq, req.SpeedTestPing2Req)


def handler(request):
    def generator(handlerCls):
        Server().handler[request.__name__] = handlerCls()
        return handlerCls

    return generator


class Task(object):
    def __init__(self, request, backParam="", cacheAndLoadPath="", loadPath=""):
        self.req = request
        self.res = None
        self.localParam = None
        self._session = None
        self.timeout = request.timeout
        self.backParam = backParam
        self.status = Status.Ok
        self.cacheAndLoadPath = cacheAndLoadPath
        self.loadPath = loadPath
        self.index = 0

    @property
    def session(self):
        if self._session is not None:
            return self._session
        if self.localParam is not None:
            return self.localParam.session
        return None

    @property
    def bakParam(self):
        return self.backParam

    def GetText(self):
        if not self.res:
            return ""
        if hasattr(self.res, "raw"):
            return getattr(self.res.raw, "text", "")
        return ""


def _ApplyProxyUrl(request: req.ServerReq):
    proxyHost = ToolUtil.GetUrlHost(request.proxyUrl)
    host = ToolUtil.GetUrlHost(request.url)
    if host and host != proxyHost:
        request.url = request.url.replace(host, request.proxyUrl + "/" + host, 1)

    if not request.resetUrl:
        return
    newResetUrl = []
    for resetUrl in request.resetUrl:
        rHost = ToolUtil.GetUrlHost(resetUrl)
        if rHost and rHost != proxyHost:
            resetUrl = resetUrl.replace(rHost, request.proxyUrl + "/" + rHost, 1)
        newResetUrl.append(resetUrl)
    request.resetUrl = newResetUrl


def _AttachFallbackUrls(request: req.ServerReq):
    if request.ipList or isinstance(request, _SPEED_REQ_TYPES):
        return

    host = ToolUtil.GetUrlHost(request.url)
    if request.isApi and not request.resetUrl:
        # 为 API 请求准备备用域名，单条线路不可用时自动切换重试
        for url in GlobalConfig.Url2List.value:
            altHost = ToolUtil.GetUrlHost(url)
            if altHost != host:
                request.resetUrl.append(request.url.replace(host, altHost))
        if request.resetUrl:
            request.resetCnt = min(len(request.resetUrl), 3)
    elif request.isImg and len(request.resetUrl) <= 1:
        # 为图片请求准备备用 CDN 域名，下载失败时自动切换重试
        for domain in GlobalConfig.ImgAutoUrl.value:
            if domain == host:
                continue
            altUrl = request.url.replace(host, domain)
            if altUrl not in request.resetUrl:
                request.resetUrl.append(altUrl)
        if request.resetUrl:
            request.resetCnt = max(request.resetCnt, min(len(request.resetUrl), 3))


class Server(Singleton):
    def __init__(self) -> None:
        Singleton.__init__(self)
        self.handler = {}
        self.address = ""
        self.imageServer = ""

        self.token = ""
        self.threadHandler = 0
        self.threadNum = config.SpeedThreadNum
        self.speedThreadNum = 8

        from config.setting import Setting
        self.downloadNum = max(1, Setting.MultiNum.value)

        self._httpPool = None
        self._downloadPool = None
        self._speedPool = None
        self._runner = AsyncLoopRunner(
            threadName="AsyncIO-Server",
            loopFactory=lambda: self._CreateEventLoop(),
        )

    def _CreateEventLoop(self):
        return CreateDefaultEventLoop()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def Init(self):
        self._runner.Configure(
            queueSpecs=[
                ("in", "HTTP", self.threadNum, self._HandleHttpTask),
                ("download", "Download", self.downloadNum, self._HandleDownloadTask),
                ("speed", "Speed", self.speedThreadNum, self._HandleSpeedTask),
            ],
            onStartup=self._InitPools,
            onShutdown=self._ClosePools,
        )
        self._runner.Start()

    def Stop(self):
        self._runner.Stop(timeout=3.0)

    async def _InitPools(self):
        self._httpPool = AsyncSessionPool("HTTP", impersonate=None, maxClients=self.threadNum, maxSessions=6)
        self._downloadPool = AsyncSessionPool("Download", impersonate="chrome110", maxClients=self.downloadNum, maxSessions=6)
        # 测速池禁用 session 复用，保证每次测速都是独立冷连接与独立 RESOLVE
        self._speedPool = AsyncSessionPool("Speed", impersonate=None, maxClients=1, maxSessions=1, reuseSession=False)

    async def _ClosePools(self):
        for pool in (self._httpPool, self._downloadPool, self._speedPool):
            if pool is not None:
                await pool.CloseAll()

    async def _HandleHttpTask(self, task: Task, index: int):
        await self._Send(task, index, self._httpPool)

    async def _HandleSpeedTask(self, task: Task, index: int):
        await self._Send(task, index, self._speedPool)

    async def _HandleDownloadTask(self, task: Task, index: int):
        await self._Download(task, index, self._downloadPool)

    # ------------------------------------------------------------------
    # Public API (thread-safe, synchronous entry points)
    # ------------------------------------------------------------------

    def _PrepareRequest(self, request: req.ServerReq):
        if request.proxyUrl:
            _ApplyProxyUrl(request)
        else:
            _AttachFallbackUrls(request)

    def Send(self, request, token="", backParam="", isASync=True, index=0):
        self._PrepareRequest(request)
        task = Task(request, backParam)

        if isinstance(request, req.SpeedTestReq):
            if isASync:
                return self._runner.Enqueue("download", task)
            return self._runner.RunSync(self._DownloadSync(task, index))

        queueName = "speed" if isinstance(request, (req.SpeedTestPingReq, req.SpeedTestPing2Req)) else "in"
        if isASync:
            return self._runner.Enqueue(queueName, task)
        return self._runner.RunSync(self._SendSync(task, index))

    def Download(self, request, token="", backParams="", cacheAndLoadPath="", loadPath="", isASync=True):
        self._PrepareRequest(request)
        task = Task(request, backParams, cacheAndLoadPath, loadPath)
        if isASync:
            self._runner.Enqueue("download", task)
        else:
            self._runner.RunSync(self._DownloadSync(task, 0))

    def ReDownload(self, task: Task):
        task.localParam = None
        task._session = None
        newTask = Task(task.req, task.backParam, task.cacheAndLoadPath, task.loadPath)
        self._runner.Enqueue("download", newTask)

    def TestSpeed(self, request, bakParams=""):
        self._PrepareRequest(request)
        self._runner.Enqueue("download", Task(request, bakParams))

    def TestSpeedPing(self, request, bakParams=""):
        self._PrepareRequest(request)
        self._runner.Enqueue("in", Task(request, bakParams))

    # ------------------------------------------------------------------
    # Sync Compatibility Helpers
    # ------------------------------------------------------------------

    async def _SendSync(self, task: Task, index: int, impersonate=None):
        pool = AsyncSessionPool("Sync", impersonate=impersonate, maxClients=1, maxSessions=1)
        try:
            return await self._Send(task, index, pool)
        finally:
            await pool.CloseAll()

    async def _DownloadSync(self, task: Task, index: int):
        pool = AsyncSessionPool("SyncDownload", impersonate="chrome110", maxClients=1, maxSessions=1)
        try:
            return await self._Download(task, index, pool)
        finally:
            await pool.CloseAll()

    # ------------------------------------------------------------------
    # Core Async Execution
    # ------------------------------------------------------------------

    async def _InvokeHandler(self, task: Task):
        handlerObj = self.handler.get(task.req.__class__.__name__)
        if handlerObj is None:
            return
        ret = handlerObj(task)
        if inspect.isawaitable(ret):
            await ret

    async def _Send(self, task: Task, index: int, sessionPool: AsyncSessionPool):
        while True:
            # 每次尝试独立记录结果，避免重试成功仍残留上次失败状态
            task.status = Status.Ok
            task.res = res.BaseRes("", False)

            entry = await sessionPool.Acquire(task.req)
            try:
                task._session = entry.session
                await self._SendAttempt(task, index)
                if task.status == Status.TimeOut:
                    await sessionPool.RetireEntry(entry, reason="timeout")
            finally:
                task._session = None
                await sessionPool.Release(entry)

            if task.status == Status.OfflineModel:
                return task.res
            if task.status == Status.Ok or task.req.resetCnt < 0:
                break
            task.req.ResetToSwitchNextUrl()

        response = None
        try:
            await self._InvokeHandler(task)
        except asyncio.CancelledError:
            raise
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            response = task.res
            task.res = None
            task._session = None
            task.localParam = None
        return response

    async def _SendAttempt(self, task: Task, index: int):
        ttfbTime = 0
        addSize = 0
        try:
            task.req.resetCnt -= 1
            Log.Info("request{}-> backId:{}, {}".format(index, task.bakParam, task.req))
            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                if task.bakParam:
                    data = {"st": Status.OfflineModel, "data": ""}
                    TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
                return

            method = task.req.method.lower()
            if method in ("post", "post2"):
                await self.Post(task, index)
            elif method in ("get", "get2"):
                await self.Get(task, index)
            elif method == "put":
                await self.Put(task, index)
            else:
                return

            ttfbTime = task.res.raw.infos.get(CurlInfo.STARTTRANSFER_TIME)
            addSize = len(task.res.raw.content)
        except asyncio.CancelledError:
            raise
        except Exception as es:
            task.status = ClassifyRequestError(es)
            Log.Warn(f"error:{task.req.GetPri()}")
            Log.Error(es)
        finally:
            if task.req.isApi and not isinstance(task.req, _SPEED_REQ_TYPES):
                statusCode = task.res.raw.status_code if task.res.raw else 0
                if isinstance(ttfbTime, (int, float)):
                    TaskBase.taskObj.statuApiBack.emit(ttfbTime, task.status, statusCode, addSize)

            Log.Info(
                "response{}-> backId:{}, {}, st:{}, {}".format(
                    index, task.backParam, task.req.__class__.__name__, task.status, task.res
                )
            )

    async def _Request(self, task: Task, method: str):
        request = task.req
        if request.params is None:
            request.params = {}
        if request.headers is None:
            request.headers = {}

        task.res = res.BaseRes("", False)
        kwargs = {
            "proxies": request.proxy,
            "headers": request.headers,
            "timeout": task.timeout,
        }
        if method == "post":
            kwargs["data"] = request.params
        if method in ("get", "post") and request.cookies:
            kwargs["cookies"] = request.cookies

        r = await getattr(task.session, method)(request.url, **kwargs)
        task.res = res.BaseRes(r, request.isParseRes)
        return task

    async def Post(self, task: Task, index=0):
        return await self._Request(task, "post")

    async def Put(self, task: Task, index=0):
        return await self._Request(task, "put")

    async def Get(self, task: Task, index=0):
        return await self._Request(task, "get")

    async def _TryLoadCache(self, task: Task, index: int) -> bool:
        if task.req.isReload or isinstance(task.req, req.SpeedTestReq) or task.req.savePath:
            return False
        for cachePath in (task.req.loadPath, task.req.cachePath):
            if not cachePath or not task.bakParam:
                continue
            data = await asyncio.to_thread(ToolUtil.LoadCachePicture, cachePath)
            if data:
                TaskBase.taskObj.downloadBack.emit(task.bakParam, len(data), len(data), b"")
                TaskBase.taskObj.downloadBack.emit(task.bakParam, 0, len(data), data)
                Log.Info("request{} cache -> backId:{}, {}".format(index, task.bakParam, task.req))
                return True
        return False

    async def _Download(self, task: Task, index: int, sessionPool: AsyncSessionPool):
        entry = None
        try:
            task.req.resetCnt -= 1
            if await self._TryLoadCache(task, index):
                return

            if QtOwner().isOfflineModel:
                task.status = Status.OfflineModel
                await self._InvokeHandler(task)
                return

            if not isinstance(task.req, req.SpeedTestReq):
                entry = await sessionPool.Acquire(task.req)
                task._session = entry.session

            request = task.req
            if request.params is None:
                request.params = {}
            if request.headers is None:
                request.headers = {}

            if not request.isReset:
                Log.Info("request{}-> backId:{}, {}".format(index, task.bakParam, task.req))
            else:
                Log.Info(
                    "request{} reset:{} -> backId:{}, {}".format(
                        index, task.req.resetCnt, task.bakParam, task.req
                    )
                )
            task.res = None
            task.index = index
        except asyncio.CancelledError:
            if entry is not None:
                task._session = None
                await sessionPool.Release(entry)
            raise
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())

        try:
            await self._InvokeHandler(task)
        except asyncio.CancelledError:
            raise
        except Exception as es:
            task.status = Status.NetError
            Log.Warn(task.req.url + " " + es.__repr__())
            Log.Debug(es)
        finally:
            if entry is not None and task.status == Status.TimeOut:
                await sessionPool.RetireEntry(entry, reason="timeout")
            task.res = None
            task._session = None
            task.localParam = None
            if entry is not None:
                await sessionPool.Release(entry)
