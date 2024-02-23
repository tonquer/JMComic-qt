import os
import threading
from queue import Queue

from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from tools.singleton import Singleton
from tools.str import Str


class QtTaskQObject(QObject):
    taskBack = Signal(int, bytes)
    downloadBack = Signal(int, int, int, bytes)
    downloadStBack = Signal(int, dict)
    convertBack = Signal(int)
    imageBack = Signal(int, QImage)
    localBack = Signal(int, int, list)
    localReadBack = Signal(int, int, bytes)

    def __init__(self):
        super(self.__class__, self).__init__()


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""


class QtTaskBase:
    Id = 1

    def __init__(self):
        self.__taskFlagId = QtTaskBase.Id
        QtTaskBase.Id += 1

    @property
    def req(self):
        return

    @property
    def cleanFlag(self):
        return self.__taskFlagId

    # callBack(data)
    # callBack(data, backParam)
    def AddHttpTask(self, req, callBack=None, backParam=None):
        from tools.qt_domain import QtDomainMgr
        from task.task_http import TaskHttp
        # if not Setting.IsOpenDoh.value:
        return TaskHttp().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)
        # else:
        #     return QtDomainMgr().AddHttpTask(req, callBack, backParam, cleanFlag=self.__taskFlagId)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadBook(self, bookId, epsId, index, statusBack=None, downloadCallBack=None, completeCallBack=None, backParam=None, loadPath="", cachePath="", savePath="", cleanFlag="", isInit=False):
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskDownload().DownloadBook(bookId, epsId, index, statusBack, downloadCallBack, completeCallBack, backParam, loadPath, cachePath, savePath, cleanFlag, isInit)

    def AddDownloadBookCache(self, loadPath, completeCallBack=None, backParam=0, cleanFlag=""):
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskDownload().DownloadCache(loadPath, completeCallBack, backParam, cleanFlag)

    # downloadCallBack(data, laveFileSize, backParam)
    # downloadCallBack(data, laveFileSize)
    # downloadCompleteBack(data, st)
    # downloadCompleteBack(data, st, backParam)
    def AddDownloadTask(self, url, path="", downloadCallBack=None, completeCallBack=None, downloadStCallBack=None, backParam=None, loadPath="", cachePath="", savePath="",  saveParam="", cleanFlag="", isReload=False, resetCnt=1):
        from tools.qt_domain import QtDomainMgr
        from task.task_download import TaskDownload
        if not cleanFlag:
            cleanFlag = self.__taskFlagId

        if "https://" not in url and "http://" not in url:
            url = GlobalConfig.PicUrl2.value + url

        if not cachePath and not savePath:
            if Setting.SavePath.value and path:
                filePath2 = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), path)
                cachePath = filePath2

        # if not Setting.IsOpenDohPicture.value:
        return TaskDownload().DownloadTask(url, downloadCallBack, completeCallBack, downloadStCallBack, backParam, loadPath,
                                               cachePath, savePath, saveParam, cleanFlag, isReload, resetCnt)
        # else:
        #     return QtDomainMgr().AddDownloadTask(url, downloadCallBack, completeCallBack, downloadStCallBack, backParam, loadPath,
        #                                        cachePath, savePath, saveParam, cleanFlag, isReload)

    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTask(self, path, imgData, model, completeCallBack, backParam=None, preDownPath=None, noSaveCache=False, saveParams=None, cleanFlag=""):
        from task.task_waifu2x import TaskWaifu2x
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskWaifu2x().AddConvertTaskByData(path, imgData, model, completeCallBack, backParam, preDownPath, noSaveCache, saveParams, cleanFlag)

    # completeCallBack
    # completeCallBack(saveData, taskId, backParam, tick)
    def AddConvertTaskByPath(self, loadPath, savePath, completeCallBack, backParam=None, cleanFlag=""):
        from task.task_waifu2x import TaskWaifu2x
        if not cleanFlag:
            cleanFlag = self.__taskFlagId
        return TaskWaifu2x().AddConvertTaskByPath(loadPath, savePath, completeCallBack, backParam, cleanFlag)

    def AddQImageTask(self, data, radio, toW, toH, model, saveParams, callBack=None, backParam=None):
        from task.task_qimage import TaskQImage
        return TaskQImage().AddQImageTask(data, radio, toW, toH, model, saveParams, callBack, backParam, cleanFlag=self.__taskFlagId)

    def AddLocalTaskLoad(self, type, dir, backparam=None, callBack=None):
        from task.task_local import TaskLocal
        return TaskLocal().AddLoadRead(type, dir, backparam, callBack, cleanFlag=self.__taskFlagId)

    def AddLocalTaskLoadPicture(self, v, index, backparam=None, callBack=None):
        from task.task_local import TaskLocal
        return TaskLocal().AddLoadReadPicture(v, index, backparam, callBack, cleanFlag=self.__taskFlagId)

    def ClearQImageTaskById(self, taskId):
        from task.task_qimage import TaskQImage
        return TaskQImage().ClearQImageTaskById(taskId)

    def ClearTask(self):
        from task.task_http import TaskHttp
        return TaskHttp().Cancel(self.__taskFlagId)

    def ClearDownload(self):
        from task.task_download import TaskDownload
        return TaskDownload().Cancel(self.__taskFlagId)

    def ClearConvert(self):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().Cancel(self.__taskFlagId)

    def ClearWaitConvertIds(self, taskIds):
        from task.task_waifu2x import TaskWaifu2x
        return TaskWaifu2x().ClearWaitConvertIds(taskIds)

    def ClearQImageTask(self):
        from task.task_qimage import TaskQImage
        return TaskQImage().Cancel(self.__taskFlagId)


class QtDownloadTask(object):
    Waiting = Str.Waiting
    Reading = Str.Reading
    ReadingPicture = Str.ReadingPicture
    Downloading = Str.Downloading
    Success = Str.Success
    Error = Str.Error

    def __init__(self, downloadId=0):
        self.downloadId = downloadId
        self.downloadCallBack = None       # addData, laveSize
        self.downloadCompleteBack = None   # data, status

        self.status = self.Waiting
        self.statusBack = None             # data, status
        self.fileSize = 0
        self.saveData = b""
        self.bookId = ""
        self.epsId = ""
        self.index = ""
        self.isSaveCache = ""
        self.isSaveFile = False
        self.resetCnt = 0
        self.cacheCallBack = ""   # ��ʱ����һ��callback����Ϊ

        self.originalName = ""
        self.backParam = None
        self.cleanFlag = ""
        self.tick = 0
        self.cacheAndLoadPath = ""   # ����ͼ���
        self.loadPath = ""           # ֻ����

        self.imgData = b""
        self.scale = 0
        self.noise = 0
        self.model = {
            "model": 1,
            "scale": 2,
            "toH": 100,
            "toW": 100,
        }


class TaskBase(Singleton):
    taskId = 0
    taskObj = QtTaskQObject()

    def __init__(self):
        Singleton.__init__(self)
        self.thread = threading.Thread(target=self.Run)
        self.thread.setName("Task-" + str(self.__class__.__name__))
        self.thread.setDaemon(True)
        self._inQueue = Queue()
        self.tasks = {}
        self.flagToIds = {}

    def Stop(self):
        self._inQueue.put("")
        return

    def Run(self):
        return

    def Cancel(self, cleanFlag):
        taskIds = self.flagToIds.get(cleanFlag, set())
        if not taskIds:
            return
        for taskId in taskIds:
            if taskId in self.tasks:
                del self.tasks[taskId]
        self.flagToIds.pop(cleanFlag)
