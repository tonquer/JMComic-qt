import os
from enum import Enum
from functools import partial

from config import config
from config.setting import Setting
from tools.book import BookMgr, BookInfo, BookEps
from tools.log import Log
from task.qt_task import TaskBase, QtDownloadTask, QtTaskBase
from tools.status import Status


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
            self.HandlerDownload({"st": Status.Ok}, v)

    def DownloadBook(self, bookId, epsId, index, statusBack=None, downloadCallBack=None, completeCallBack=None,
                    backParam=None, isSaveCache=True, cleanFlag=None, isSaveFile=False, filePath=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.statusBack = statusBack
        data.backParam = backParam
        data.bookId = bookId
        data.epsId = epsId
        data.index = index
        data.isSaveCache = isSaveCache
        data.isSaveFile = isSaveFile
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        # if isSaveCache:
        #     path = "{}/{}/{}".format(data.site, bookId, index+1)
        #     data.cacheAndLoadPath = path

        if filePath:
            data.loadPath = filePath

        Log.Debug("add download info, cachePath:{}, loadPath:{}".format(data.cacheAndLoadPath, data.loadPath))
        self._inQueue.put(self.taskId)
        # from server.server import Server
        # from server import req
        # Server().Download(req.DownloadBookReq(url, path, isSaveCache), backParams=self.taskId, cacheAndLoadPath=data.cacheAndLoadPath, loadPath=data.loadPath)
        return self.taskId

    def HandlerDownload(self, data, taskId):
        task = self.tasks.get(taskId)
        if not task:
            return
        status = Status.WaitLoad
        backData = {}
        from server import req, ToolUtil
        try:
            assert isinstance(task, QtDownloadTask)

            if data["st"] != Status.Ok:
                task.resetCnt += 1

                # 失败了
                if task.resetCnt >= 5:
                    TaskBase.taskObj.downloadBack.emit(task.backParam, -1, b"")
                status = task.Error
                self.SetTaskStatus(taskId, task, backData, status)
                return

            info = BookMgr().GetBook(task.bookId)
            if not info:
                self.AddHttpTask(req.GetBookInfoReq(task.bookId), self.HandlerDownload, taskId)
                status = task.Reading
                self.SetTaskStatus(taskId, task, backData, status)
                return
            if task.epsId not in info.pageInfo.epsInfo:
                status = task.Error
                self.SetTaskStatus(taskId, task, backData, status)
                return

            epsInfo = info.pageInfo.epsInfo.get(task.epsId)
            assert isinstance(epsInfo, BookEps)
            if not epsInfo.pictureUrl:
                self.AddHttpTask(req.GetBookImgUrl(task.bookId, task.epsId), self.HandlerDownload, taskId)
                status = task.Reading
                self.SetTaskStatus(taskId, task, backData, status)
                return

            assert isinstance(info, BookInfo)
            backData["maxPic"] = len(epsInfo.pictureUrl)

            # 如果有缓存则不需要以下步骤了
            task.cacheAndLoadPath = "{}/{}/{}".format(task.bookId, task.epsId + 1, task.index + 1)
            filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), task.cacheAndLoadPath) + ".jpg"
            for cachePath in [filePath2, task.loadPath]:
                if cachePath:
                    imgData = ToolUtil.LoadCachePicture(cachePath)
                    if imgData:
                        self.SetTaskStatus(taskId, task, backData, status)
                        TaskBase.taskObj.downloadBack.emit(taskId, len(imgData), imgData)
                        TaskBase.taskObj.downloadBack.emit(taskId, 0, b"")
                        return

            imgUrl = epsInfo.pictureUrl.get(task.index)
            # 如果不存在url
            if not imgUrl:
                status = task.Error
                self.SetTaskStatus(taskId, task, backData, status)
                return
            else:
                from server.server import Server
                status = task.Downloading
                self.SetTaskStatus(taskId, task, backData, status)
                self.AddDownloadTask(imgUrl, task.cacheAndLoadPath, task.downloadCallBack, task.downloadCompleteBack, task.backParam, task.isSaveCache,task.isSaveFile,
                                     task.loadPath)
        except Exception as es:
            Log.Error(es)
        return

    def SetTaskStatus(self, taskId, task, backData, status):
        backData["st"] = status
        task.cacheCallBack = partial(self.CallBookBack, dict(backData))
        if status == task.Downloading or Status == task.Error:
            TaskBase.taskObj.downloadStBack.emit(taskId, "-1")
        else:
            TaskBase.taskObj.downloadStBack.emit(taskId, "")
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

    def DownloadTask(self, url, path, downloadCallBack=None, completeCallBack=None, backParam=None, isSaveCache=True, cleanFlag=None, isSaveFile=False, filePath=""):
        self.taskId += 1
        data = QtDownloadTask(self.taskId)
        data.downloadCallBack = downloadCallBack
        data.downloadCompleteBack = completeCallBack
        data.backParam = backParam
        self.tasks[self.taskId] = data
        if cleanFlag:
            data.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        if isSaveCache and path and Setting.SavePath.value:
            filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), path)
            data.cacheAndLoadPath = filePath2
        if filePath:
            data.loadPath = filePath

        Log.Debug("add download info, cachePath:{}, loadPath:{}".format(data.cacheAndLoadPath, data.loadPath))
        from src.server import Server
        from src.server import req
        if isSaveFile:
            savePath = filePath
        else:
            savePath = ""

        Server().Download(req.DownloadBookReq(url, isSaveCache, savePath), backParams=self.taskId, cacheAndLoadPath=data.cacheAndLoadPath, loadPath=data.loadPath)
        return self.taskId

    def HandlerTask(self, downloadId, laveFileSize, data, isCallBack=True):
        info = self.tasks.get(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)
        if laveFileSize < 0 and data == b"":
            try:
                if laveFileSize == -111:
                    if info.cacheCallBack:
                        info.cacheCallBack(info)
                    return
                if info.downloadCompleteBack:
                    if info.backParam is not None:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), laveFileSize, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), laveFileSize)
            except Exception as es:
                Log.Error(es)
            self.ClearDownloadTask(downloadId)
            return

        info.saveData += data

        if info.downloadCallBack:
            try:
                if info.backParam is not None:
                    info.downloadCallBack(data, laveFileSize, info.backParam)
                else:
                    info.downloadCallBack(data, laveFileSize)
            except Exception as es:
                Log.Error(es)
        if laveFileSize == 0 and data == b"":
            if info.downloadCompleteBack:
                try:
                    if info.cleanFlag:
                        taskIds = self.flagToIds.get(info.cleanFlag, set())
                        taskIds.discard(info.downloadId)
                    if info.backParam is not None:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), Status.Ok, info.backParam)
                    else:
                        info.downloadCompleteBack(self.GetDownloadData(downloadId), Status.Ok)
                except Exception as es:
                    Log.Error(es)
            self.ClearDownloadTask(downloadId)

    def HandlerTaskSt(self, downloadId, data):
        info = self.tasks.get(downloadId)
        if not info:
            return
        assert isinstance(info, QtDownloadTask)
        try:
            info.cacheCallBack(info)
            if data == "-1":
                self.ClearDownloadTask(downloadId)
        except Exception as es:
            Log.Error(es)

    def ClearDownloadTask(self, downloadId):
        info = self.tasks.get(downloadId)
        if not info:
            return
        del info.saveData
        info.cacheCallBack = None
        del self.tasks[downloadId]

    def GetDownloadData(self, downloadId):
        if downloadId not in self.tasks:
            return b""
        return self.tasks[downloadId].saveData
