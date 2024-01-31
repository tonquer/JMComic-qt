import hashlib
import os
from functools import partial

from config import config
from config.setting import Setting
from task.qt_task import TaskBase, QtTaskBase
from tools.book import BookMgr, BookEps
from tools.log import Log
from tools.status import Status
from tools.str import Str


class QtDownloadTask(object):
    Waiting = Str.Waiting
    Reading = Str.Reading
    ReadingEps = Str.ReadingEps
    ReadingPicture = Str.ReadingPicture
    Downloading = Str.Downloading
    Success = Str.Success
    Error = Str.Error
    Cache = Str.Cache

    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status
        self.statusBack = None
        self.fileSize = 0
        self.url = ""
        self.path = ""
        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.isInit = False
        self.isReload = False
        self.lastLaveSize = 0
        self.isLoadTask = False

        self.loadPath = ""    # 只加载
        self.cachePath = ""   # 缓存路径
        self.savePath = ""    # 下载保存路径
        self.saveParam = ""    # 下载保存路径

        self.bookId = ""      # 下载的bookId
        self.epsIndex = 0        # 下载的章节
        self.index = 0        # 下载的索引
        self.resetCnt = 0     # 重试次数
        self.isLocal = True
        self.status = self.Waiting


class TaskDownload(TaskBase, QtTaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        self.taskObj.downloadBack.connect(self.HandlerTask)
        self.taskObj.downloadStBack.connect(self.HandlerTaskSt)
        self.thread.start()

    def Run(self):
        while True:
            v = self._inQueue.get(True)
            self._inQueue.task_done()
            if v == "":
                break
            self.HandlerDownload({"st": Status.Ok}, (v, QtDownloadTask.Waiting))

    def DownloadTask(self, url, downloadCallBack=None, completeCallBack=None, downloadStCallBack=None, backParam=None, loadPath="", cachePath="", savePath="", saveParam="", cleanFlag="", isReload=False, resetCnt=1):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.statusBack = downloadStCallBack
        data.backParam = backParam
        data.isReload = isReload
        data.url = url
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        data.saveParam = saveParam
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        Log.Debug("add download info, cachePath:{}, loadPath:{}, savePath:{}".format(data.cachePath, data.loadPath, data.savePath))
        from server.server import Server
        from server import req
        Server().Download(req.DownloadBookReq(url,  data.loadPath, data.cachePath, data.savePath, data.saveParam, data.isReload, resetCnt), backParams=self.taskId)
        return self.taskId

    def DownloadCache(self, filePath, completeCallBack=None, backParam = 0, cleanFlag=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCompleteBack = completeCallBack
        data.loadPath = filePath
        data.backParam = backParam
        data.isLoadTask = True
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        self.tasks[self.taskId] = data
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerTask(self, downloadId, addSize, laveFileSize, data, isCallBack=True):
        info = self.tasks.get(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)

        # 表示保存失败了
        if laveFileSize == -2:
            v = {"st": Status.SaveError}
            self.CallBookBack(v, info)
            return
        # 表示成功但是没有图片
        st = Str.Error
        if laveFileSize < -2:
            st = - laveFileSize

        if laveFileSize < 0 and data == b"":
            try:
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(b"", st, info.backParam)
                    else:
                        info.downloadCompleteBack(b"", st)
            except Exception as es:
                Log.Error(es)
            self.ClearDownloadTask(downloadId)
            return

        if info.lastLaveSize <= 0:
            info.lastLaveSize = laveFileSize

        if info.downloadCallBack:
            try:
                if info.backParam is not None:
                    info.downloadCallBack(addSize, laveFileSize, info.backParam)
                else:
                    info.downloadCallBack(addSize, laveFileSize)
            except Exception as es:
                Log.Error(es)
            info.lastLaveSize = laveFileSize

        if laveFileSize == 0 and data != b"":
            if info.downloadCompleteBack:
                try:
                    if info.cleanFlag:
                        taskIds = self.flagToIds.get(info.cleanFlag, set())
                        taskIds.discard(info.downloadId)
                    if info.backParam is not None:
                        info.downloadCompleteBack(data, Status.Ok, info.backParam)
                    else:
                        info.downloadCompleteBack(data, Status.Ok)
                except Exception as es:
                    Log.Error(es)
            self.ClearDownloadTask(downloadId)

    def DownloadBook(self, bookId, epsIndex, index, statusBack=None, downloadCallBack=None, completeCallBack=None,
                    backParam=None, loadPath="", cachePath="", savePath="", cleanFlag=None, isInit=False):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.statusBack = statusBack
        data.backParam = backParam
        data.bookId = bookId
        data.epsIndex = epsIndex
        data.index = index
        data.loadPath = loadPath
        data.cachePath = cachePath
        data.savePath = savePath
        data.isInit = isInit
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)
        Log.Debug("add download info, savePath:{}, loadPath:{}".format(data.savePath, data.loadPath))
        self._inQueue.put(self.taskId)
        return self.taskId

    def HandlerDownload(self, data, v):
        (taskId, newStatus) = v
        task = self.tasks.get(taskId)
        if not task:
            return
        backData = {}
        from server import req, ToolUtil
        try:
            assert isinstance(task, QtDownloadTask)
            if task.isLoadTask:
                imgData = ToolUtil.LoadCachePicture(task.loadPath)
                if imgData:
                    TaskBase.taskObj.downloadBack.emit(taskId, 0, len(imgData), b"")
                    TaskBase.taskObj.downloadBack.emit(taskId, 0, 0, imgData)
                else:
                    TaskBase.taskObj.downloadBack.emit(taskId, 0, -Status.FileError, b"")
                return

            isReset = False
            if data["st"] != Status.Ok:
                task.resetCnt += 1

                # 失败了
                if task.resetCnt >= 5:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return

                isReset = True
            else:
                task.status = newStatus
            info = BookMgr().GetBook(task.bookId)
            if task.status == task.Waiting:
                isReset or self.SetTaskStatus(taskId, backData, task.Reading)
                if not info:
                    self.AddHttpTask(req.GetBookInfoReq2(task.bookId), self.HandlerDownload, (taskId, task.Reading))
                    return

                task.status = task.Reading
            if task.status == task.Reading:
                isReset or self.SetTaskStatus(taskId, backData, task.ReadingEps)

                epsInfo = info.pageInfo.epsInfo.get(task.epsIndex)
                if info.pageInfo.epsInfo  and not epsInfo:
                    self.SetTaskStatus(taskId, backData, Str.SpaceEps)
                    return

                if not epsInfo.pictureUrl:
                    self.AddHttpTask(req.GetBookEpsInfoReq2(task.bookId, epsInfo.epsId), self.HandlerDownload, (taskId, task.ReadingEps))
                    return

                assert isinstance(epsInfo, BookEps)
                task.status = task.ReadingEps
            if task.status == task.ReadingEps:
                isReset or self.SetTaskStatus(taskId, backData, task.ReadingPicture)

                epsInfo = info.pageInfo.epsInfo.get(task.epsIndex)
                assert isinstance(epsInfo, BookEps)
                if not epsInfo.scrambleId:
                    self.AddHttpTask(req.GetBookEpsScrambleReq2(task.bookId, epsInfo.index, epsInfo.epsId), self.HandlerDownload, (taskId, task.ReadingPicture))
                    return

                task.status = task.ReadingPicture
            if task.status == task.ReadingPicture:
                epsInfo = info.pageInfo.epsInfo.get(task.epsIndex)
                assert isinstance(epsInfo, BookEps)
                backData["maxPic"] = len(epsInfo.pictureUrl)
                backData["bookName"] = info.baseInfo.title
                backData["title"] = epsInfo.title
                backData["maxEps"] = len(info.pageInfo.epsInfo)
                backData["author"] = "&".join(info.baseInfo.authorList)
                isReset or self.SetTaskStatus(taskId, backData, task.Downloading)

                if task.isInit:
                    self.SetTaskStatus(taskId, backData, task.Success)
                    return

                pitureName = epsInfo.pictureName.get(task.index)
                task.saveParam = (epsInfo.epsId, epsInfo.scrambleId, pitureName)
                if task.savePath:
                    if ToolUtil.IsHaveFile(task.savePath):
                        self.SetTaskStatus(taskId, backData, task.Cache)
                        return
                else:
                    path = ToolUtil.GetRealPath(task.index+1, "book/{}/{}".format(task.bookId, task.epsIndex+1))
                    cachePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), path)
                    checkPaths = [task.loadPath]

                    if Setting.SavePath.value:
                        checkPaths.append(cachePath2)
                        task.cachePath = cachePath2

                    for cachePath in checkPaths:
                        if cachePath:
                            imgData = ToolUtil.LoadCachePicture(cachePath)
                            if imgData:
                                TaskBase.taskObj.downloadBack.emit(taskId, 0, len(imgData), b"")
                                TaskBase.taskObj.downloadBack.emit(taskId, 0, 0, imgData)
                                return

                imgUrl = epsInfo.pictureUrl.get(task.index)
                if not imgUrl:
                    self.SetTaskStatus(taskId, backData, task.Error)
                    return
                resetCnt = 3
                self.AddDownloadTask(imgUrl, "", task.downloadCallBack, task.downloadCompleteBack, task.statusBack,
                    task.backParam, task.loadPath, task.cachePath, task.savePath, task.saveParam, task.cleanFlag, resetCnt=resetCnt)
        except Exception as es:
            self.SetTaskStatus(taskId, backData, task.Error)
            Log.Error(es)
        return

    def SetTaskStatus(self, taskId, backData, status):
        backData["st"] = status
        self.taskObj.downloadStBack.emit(taskId, dict(backData))
        return

    def CallBookBack(self, data, task):
        try:
            if not task.statusBack:
                return
            if task.backParam is not None:
                task.statusBack(data, task.backParam)
            else:
                task.statusBack(data)
        except Exception as es:
            Log.Error(es)

    def HandlerTaskSt(self, downloadId, data):
        task = self.tasks.get(downloadId)
        if not task:
            return
        assert isinstance(task, QtDownloadTask)
        try:
            self.CallBookBack(data, task)
            status = task.status
            if status == task.Downloading or status == task.Error or status == task.Cache:
                self.ClearDownloadTask(downloadId)
        except Exception as es:
            Log.Error(es)

    def ClearDownloadTask(self, downloadId):
        info = self.tasks.get(downloadId)
        if not info:
            return
        del self.tasks[downloadId]