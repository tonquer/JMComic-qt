import hashlib
import os
import sqlite3
import time
from datetime import datetime, timedelta

from cachetools import LRUCache, TLRUCache

from config.setting import Setting
from task.qt_task import TaskBase, QtTaskBase
from tools.log import Log
from tools.status import Status
from tools.tool import ToolUtil, time_me


class LRUDiskCache(TLRUCache):
    def __init__(self, maxsize, ttu, getsizeof=None, timer=datetime.now, onEvict=None):
        super().__init__(maxsize=maxsize, ttu=ttu, getsizeof=getsizeof, timer=timer)
        self._onEvict = onEvict

    def popitem(self):
        key, value = super().popitem()
        if self._onEvict:
            self._onEvict(value.key, value.path)
        return key, value

    def expire(self, time=None):
        items = super().expire(time)
        for key, val in items:
            assert isinstance(val, FilePicCache)
            if self._onEvict:
                self._onEvict(val.key, val.path)
        return items


class FilePicCache(object):
    def __init__(self):
        # self.downloadTaskId = 0
        self.data = b""
        self.key = ""
        self.path = ""
        self.size = 0
        self.tick = 0
        self.ttl = 0
        self.bookId = ""

    @staticmethod
    def GetSize(self):
        return self.size

    @staticmethod
    def GetTTU(key, value, now):
        assert isinstance(value, FilePicCache)
        return now + timedelta(seconds=value.ttl)


class DiskCacheDB(object):
    def __init__(self):
        self.db = None
        self.cur = None

    def Init(self):
        if self.db:
            return False
        self.db = sqlite3.connect(os.path.join(Setting.GetStatePath(), "disk_cache.db"),
                                  check_same_thread=False)
        self.cur = self.db.cursor()
        sql1 = """\
            create table if not exists cache_path(\
            key varchar primary key,\
            path varchar, \
            tick INTEGER, \
            size INTEGER
            )\
            """
        sql2 = """\
            create table if not exists cache_sys(\
            key varchar primary key,\
            cache_path varchar, \
            last_tick INTEGER
            )\
            """
        try:
            self.cur.execute(sql1)
            self.cur.execute(sql2)
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)
        return True

    def Close(self):
        if self.db:
            try:
                self.db.close()
            except Exception as es:
                Log.Error(es)
            finally:
                self.db = None
                self.cur = None

    def GetLastTick(self):
        if not self.db:
            return 0
        try:
            self.cur.execute(
                """
                select last_tick from cache_sys where key=?
                """,
                ("sys",),
            )
            row = self.cur.fetchone()
            if row and row[0] is not None:
                return int(row[0])
        except Exception as es:
            Log.Error(es)
        return 0

    def LoadAll(self):
        if not self.db:
            return []
        allFile = []
        try:
            self.cur.execute(
                """
                select key, path, tick, size from cache_path order by tick asc
                """
            )
            for query in self.cur.fetchall():
                file = FilePicCache()
                file.size = int(query[3])
                file.key = query[0]
                file.path = query[1]
                file.tick = int(query[2])
                allFile.append(file)
        except Exception as es:
            Log.Error(es)
        return allFile

    def DelAll(self):
        if not self.db:
            return
        try:
            self.cur.execute("delete from cache_path")
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)

    def DelByKey(self, key):
        if not self.db:
            return
        try:
            self.cur.execute("delete from cache_path where key=?", (key,))
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)

    def DelByKeys(self, keys):
        if not self.db or not keys:
            return
        try:
            self.cur.executemany("delete from cache_path where key=?", [(k,) for k in keys])
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)

    def Add(self, file):
        if not self.db:
            return
        try:
            self.__Add(file)
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)

    def AddAll(self, files):
        if not self.db or not files:
            return
        try:
            for file in files:
                self.__Add(file)
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)

    def __Add(self, file):
        assert isinstance(file, FilePicCache)
        if not self.db:
            return
        self.cur.execute(
            "INSERT INTO cache_path(key, path, size, tick) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET path=excluded.path, size=excluded.size, tick=excluded.tick",
            (file.key, file.path, file.size, file.tick),
        )
        return

    def UpdateInfo(self):
        if not self.db:
            return
        try:
            self.cur.execute(
                "INSERT INTO cache_sys(key, last_tick) "
                "VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET last_tick=excluded.last_tick",
                ("sys", int(time.time())),
            )
            self.db.commit()
        except Exception as es:
            self.db.rollback()
            Log.Error(es)
        return


class TaskCache(TaskBase, QtTaskBase):
    MB = 1024 * 1024
    DAY = 24 * 3600

    DefaultMem = 128         # 内存cache默认128M
    DefaultDisk = 1024       # 磁盘cache默认1024M
    DefaultTick = DAY

    TypeInitDiskDB = 0          # 初始化磁盘缓存DB
    TypeInitDiskCache = 1       # 扫描初始化磁盘缓存
    TypeAddDiskCache = 2        # 添加磁盘缓存
    TypeRemoveDiskCache = 3     # 删除磁盘缓存
    TypeUpdateDiskSetting = 4   # 更新磁盘缓存设置
    TypeRemoveDiskPrefix = 5    # 按目录前缀移除磁盘缓存索引

    def __init__(self):
        TaskBase.__init__(self)
        QtTaskBase.__init__(self)
        self.isOpenMem = False
        self.isOpenDisk = False
        self.isInitDisk = False
        self._diskSizeBytes = 0
        self._pendingInitDiskCache = False
        self.__diskDB = DiskCacheDB()
        self.diskSaveSecond = self.DAY * 30
        self.memeryCache = LRUCache(maxsize=self.DefaultMem * self.MB, getsizeof=FilePicCache.GetSize)

        # 该结构仅由本线程修改，通过 _SyncDiskSize 同步快照供主线程安全读取
        self.diskCache = self._CreateDiskCache(self.DefaultDisk * self.MB)

        self.thread.start()

    def _CreateDiskCache(self, maxsize):
        return LRUDiskCache(
            maxsize=maxsize,
            ttu=FilePicCache.GetTTU,
            getsizeof=FilePicCache.GetSize,
            timer=datetime.now,
            onEvict=self._EvictDiskEntry,
        )

    def _SyncDiskSize(self):
        with self._taskLock:
            self._diskSizeBytes = self.diskCache.currsize

    def _EvictDiskEntry(self, key, path):
        self.__diskDB.DelByKey(key)
        if path and os.path.isfile(path):
            try:
                os.remove(path)
                Log.Debug(f"remove cache disk, path: {path}")
            except OSError as es:
                Log.Warn(f"remove cache disk failed, path: {path}, err: {es}")

    def Init(self):
        from qt_owner import QtOwner
        self.taskObj.diskCacheRefresh.connect(QtOwner().settingView.UpdateCacheLabe)

        self.UpdateSetting()
        if not self.isOpenDisk:
            self._inQueue.put((self.TypeInitDiskDB, ()))
        return

    def UpdateSetting(self):
        if not Setting.SavePath.value or not Setting.IsInitSave.value:
            return
        self.isOpenMem = bool(Setting.IsOpenMemCache.value)
        self.isOpenDisk = bool(Setting.IsOpenDiskCache.value)
        with self._taskLock:
            if not self.isOpenMem:
                self.memeryCache.clear()
            if Setting.MemCacheSize.value > 0:
                newMax = Setting.MemCacheSize.value * self.MB
                if self.memeryCache.maxsize != newMax:
                    newCache = LRUCache(maxsize=newMax, getsizeof=FilePicCache.GetSize)
                    for k, v in self.memeryCache.items():
                        if v.size <= newMax:
                            newCache[k] = v
                    self.memeryCache = newCache
        diskMax = Setting.DiskCacheSize.value * self.MB if Setting.DiskCacheSize.value > 0 else 0
        diskSaveSecond = Setting.DiskCacheDay.value * self.DAY if Setting.DiskCacheDay.value > 0 else 0
        self._inQueue.put((self.TypeUpdateDiskSetting, (self.isOpenDisk, diskMax, diskSaveSecond)))
        return

    ## 需要在download前初始化
    def InitDownload(self):
        self.taskObj.downloadBack.connect(self.DownloadSuc)

    ## 需要在waifu2x前初始化
    def InitWaifu2x(self):
        self.taskObj.convertBack.connect(self.ConvertSuc)

    def GetMemSize(self):
        with self._taskLock:
            return round(self.memeryCache.currsize / 1024 / 1024, 2)

    def GetDiskSize(self):
        with self._taskLock:
            if not self.isInitDisk:
                return -1
            return round(self._diskSizeBytes / 1024 / 1024, 2)

    def Run(self):
        try:
            while True:
                v = self._inQueue.get(True)
                try:
                    if v == "":
                        break
                    cacheType, params = v
                    if cacheType == self.TypeInitDiskDB:
                        self.__InitDiskDB()
                    elif cacheType == self.TypeInitDiskCache:
                        self.__InitDiskCache()
                    elif cacheType == self.TypeAddDiskCache:
                        self.__AddCacheDiskPath(*params)
                    elif cacheType == self.TypeRemoveDiskCache:
                        self.__RemoveCacheDiskPath(params)
                    elif cacheType == self.TypeUpdateDiskSetting:
                        self.__UpdateDiskSetting(*params)
                    elif cacheType == self.TypeRemoveDiskPrefix:
                        self.__RemoveCacheDiskByPrefixes(params)
                except Exception as es:
                    Log.Error(es)
                finally:
                    self._inQueue.task_done()
        finally:
            self.__diskDB.Close()

    def GetMemDataByKey(self, key):
        with self._taskLock:
            file = self.memeryCache.get(key)
            if file:
                return file.data
        return None

    def ClearMemData(self, bookId):
        with self._taskLock:
            delKey = []
            for k, file in self.memeryCache.items():
                if file.bookId == bookId:
                    delKey.append(k)
            for k in delKey:
                if k in self.memeryCache:
                    self.memeryCache.pop(k)
        return

    def AddDownloadFromCache(self, data, resetCnt):
        from task.task_download import QtDownloadTask
        assert isinstance(data, QtDownloadTask)
        taskId = data.downloadId
        from server.server import Server
        from server import req
        if data.memCacheKey and not data.isReload and self.isOpenMem:
            key = data.memCacheKey
            with self._taskLock:
                file = self.memeryCache.get(key)
            if file:
                data.isCacheFetch = True
                from task.task_async import TaskAsync
                TaskAsync().AddAsyncCall("downloadBack", (data.downloadId, file.size, file.size, b""))
                TaskAsync().AddAsyncCall("downloadBack", (data.downloadId, 0, file.size, file.data))
                Log.Debug("fetch cache info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, key, data.path, len(file.data)))
                return

        Server().Download(req.DownloadBookReq(data.url, data.loadPath, data.cachePath, data.savePath, data.saveParam, data.isReload,
                                              resetCnt=resetCnt), backParams=taskId)

    @time_me
    def AddConvertFromCache(self, data):
        from task.task_waifu2x import QConvertTask
        assert isinstance(data, QConvertTask)
        taskId = data.taskId
        if data.path and self.isOpenMem:
            key = self.GetPathCacheKey(self.GetModelCachePath(data.path, data.model))
            with self._taskLock:
                file = self.memeryCache.get(key)
            if file:
                data.saveData = file.data
                data.isCacheFetch = True
                from task.task_async import TaskAsync
                TaskAsync().AddAsyncCall("convertBack", (taskId,))

                Log.Debug("fetch cache waifu2x info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, key, data.path, len(file.data)))
                return True
        return False

    def ConvertSuc(self, taskId):
        if not self.isOpenMem:
            return
        from task.task_waifu2x import QConvertTask, TaskWaifu2x
        task = TaskWaifu2x()._GetTask(taskId)
        if not task or not task.path:
            return
        if task.isCacheFetch or task.noSaveCache:
            return
        if task.status != Status.Ok:
            return
        if not task.saveData:
            return
        assert isinstance(task, QConvertTask)
        file = FilePicCache()
        file.data = task.saveData
        file.path = self.GetModelCachePath(task.path, task.model)
        file.key = self.GetPathCacheKey(file.path)
        file.size = len(file.data)
        file.bookId = task.bookId
        Log.Debug("add cache waifu2x info, taskId:{}, key:{}, path:{}, size:{}".format(taskId, file.key, file.path, len(file.data)))
        with self._taskLock:
            if file.size <= self.memeryCache.maxsize:
                self.memeryCache[file.key] = file
        return

    def DownloadSuc(self, downloadId, addSize, fileSize, data):
        if not self.isOpenMem:
            return
        if addSize < 0 or not data:
            return
        from task.task_download import TaskDownload
        task = TaskDownload()._GetTask(downloadId)
        if not task or not task.memCacheKey:
            return
        if task.isCacheFetch:
            return
        file = FilePicCache()
        file.data = data
        file.key = task.memCacheKey
        file.path = task.path
        file.size = len(data)
        file.bookId = task.bookId
        Log.Debug("add cache info, taskId:{}, key:{}, path:{}, size:{}".format(downloadId, file.key, file.path, len(data)))
        with self._taskLock:
            if file.size <= self.memeryCache.maxsize:
                self.memeryCache[file.key] = file

    def LoadDataSuc(self, path, data, bookId):
        if not path or not data:
            return
        if not self.isOpenMem:
            return
        file = FilePicCache()
        file.data = data
        file.path = path
        file.key = self.GetPathCacheKey(file.path)
        file.size = len(file.data)
        file.bookId = bookId
        Log.Debug("add cache data info, key:{}, path:{}, size:{}".format(file.key, file.path, len(file.data)))
        with self._taskLock:
            if file.size <= self.memeryCache.maxsize:
                self.memeryCache[file.key] = file
        return

    def __InitDiskDB(self):
        self.__diskDB.Init()
        lastTick = self.__diskDB.GetLastTick()
        Log.Info(f"init disk db, last_tick:{lastTick}")
        if not Setting.SavePath.value or not Setting.IsInitSave.value:
            return
        if not self.isOpenDisk:
            return
        if lastTick > 0:
            now = int(time.time())
            files = self.__diskDB.LoadAll()
            self.diskCache.clear()
            for file in files:
                file.ttl = (file.tick + self.diskSaveSecond) - now
                if file.ttl <= 0 or file.size > self.diskCache.maxsize:
                    self._EvictDiskEntry(file.key, file.path)
                    continue
                self.diskCache[file.key] = file

            with self._taskLock:
                self._diskSizeBytes = self.diskCache.currsize
                self.isInitDisk = True
            TaskBase.taskObj.diskCacheRefresh.emit()
            return
        self.InitDiskCache()
        return

    def __UpdateDiskSetting(self, isOpenDisk, diskMax, diskSaveSecond):
        ttlChanged = False
        if diskSaveSecond > 0 and self.diskSaveSecond != diskSaveSecond:
            self.diskSaveSecond = diskSaveSecond
            ttlChanged = True
        changed = False
        if (diskMax > 0 and self.diskCache.maxsize != diskMax) or ttlChanged:
            targetMax = diskMax if diskMax > 0 else self.diskCache.maxsize
            newCache = self._CreateDiskCache(targetMax)
            now = int(time.time())
            for k, v in list(self.diskCache.items()):
                v.ttl = (v.tick + self.diskSaveSecond) - now
                if v.ttl <= 0 or v.size > targetMax:
                    self._EvictDiskEntry(v.key, v.path)
                    continue
                newCache[k] = v
            self.diskCache = newCache
            self._SyncDiskSize()
            changed = True
        if isOpenDisk and not self.isInitDisk:
            self.__InitDiskDB()
        elif changed and self.isInitDisk:
            TaskBase.taskObj.diskCacheRefresh.emit()
        return

    def InitDiskCache(self):
        with self._taskLock:
            if self._pendingInitDiskCache:
                return
            self._pendingInitDiskCache = True
            self.isInitDisk = False
        self._inQueue.put((self.TypeInitDiskCache, ()))

    # init
    def __InitDiskCache(self):
        with self._taskLock:
            self._pendingInitDiskCache = False
        # 遍历cache目录文件，计算缓存时长
        try:
            if not Setting.SavePath.value:
                return
            cachePath = Setting.GetCachePath()
            if not cachePath:
                return
            self.__diskDB.Init()
            self.diskCache.clear()
            self.__diskDB.DelAll()
            now = int(time.time())
            formatSet = {ext.lower() for ext in ToolUtil.AllUseFormat}
            pathList = ["book", "book_new", "category", "cover", "game", "user", "waifu2x"]
            scannedFiles = []
            for path in pathList:
                for root, dirs, files in os.walk(os.path.join(cachePath, path)):
                    for fileName in files:
                        ext = os.path.splitext(fileName)[1].lower()
                        if ext in formatSet:
                            full_path = os.path.join(root, fileName)
                            try:
                                mtime = int(os.path.getmtime(full_path))
                                size = os.path.getsize(full_path)
                            except OSError:
                                continue
                            key = self.GetPathCacheKey(full_path)
                            file = FilePicCache()
                            # 不需要存data
                            file.size = size
                            file.key = key
                            file.path = full_path
                            file.tick = mtime
                            file.ttl = (file.tick + self.diskSaveSecond) - now
                            if file.ttl <= 0 or file.size > self.diskCache.maxsize:
                                self._EvictDiskEntry(file.key, file.path)
                                continue
                            scannedFiles.append(file)
            scannedFiles.sort(key=lambda f: f.tick)
            for file in scannedFiles:
                self.diskCache[file.key] = file
            allFiles = list(self.diskCache.values())
            self.__diskDB.AddAll(allFiles)
            self.__diskDB.UpdateInfo()
            with self._taskLock:
                self._diskSizeBytes = self.diskCache.currsize
                self.isInitDisk = True
            totalSize = sum(v.size for v in allFiles)
            Log.Debug(f"init disk cache info, len:{len(allFiles)}, size:{totalSize}")
        finally:
            self._SyncDiskSize()
            TaskBase.taskObj.diskCacheRefresh.emit()
        return

    def AddCacheDiskPath(self, path, data):
        if not self.isOpenDisk:
            return
        self._inQueue.put((self.TypeAddDiskCache, (path, data)))

    def __AddCacheDiskPath(self, path, data):
        if not self.isOpenDisk:
            return
        if not path or not data:
            return
        size = len(data)
        if size > self.diskCache.maxsize:
            return
        path = ToolUtil.GetPictureName(path, "jpg")
        key = self.GetPathCacheKey(path)

        # 先清理过期条目并移除同 key 旧记录，防止写盘后触发淘汰误删刚写入的新文件
        self.diskCache.expire()
        if key in self.diskCache:
            del self.diskCache[key]

        # 先写盘成功，再更新内存索引和数据库，避免写盘失败留下脏记录
        ToolUtil.SavePicture(data, path, "jpg")

        if not self.__diskDB.db:
            self.__diskDB.Init()
        file = FilePicCache()
        # 不需要存data
        file.size = size
        file.key = key
        file.path = path
        file.tick = int(time.time())
        file.ttl = self.diskSaveSecond
        self.diskCache[file.key] = file
        self.__diskDB.Add(file)
        self._SyncDiskSize()
        Log.Debug("add cache disk, key:{}, size:{}".format(file.key, size))
        return

    def RemoveCacheDiskPath(self, key, path):
        self._inQueue.put((self.TypeRemoveDiskCache, (key, path)))
        return

    def __RemoveCacheDiskPath(self, v):
        key, path = v
        if key in self.diskCache:
            del self.diskCache[key]
        self._EvictDiskEntry(key, path)
        self._SyncDiskSize()
        return

    def RemoveCacheDiskByPrefixes(self, prefixes):
        if not prefixes:
            return
        self._inQueue.put((self.TypeRemoveDiskPrefix, tuple(prefixes)))

    def __RemoveCacheDiskByPrefixes(self, prefixes):
        normPrefixes = []
        for p in prefixes:
            if not p:
                continue
            norm = os.path.normcase(os.path.normpath(p))
            normPrefixes.append((norm, norm + os.sep))
        if not normPrefixes:
            return
        removedKeys = []
        for key, file in list(self.diskCache.items()):
            normPath = os.path.normcase(os.path.normpath(file.path))
            if any(normPath == base or normPath.startswith(prefix) for base, prefix in normPrefixes):
                removedKeys.append(key)
        if not removedKeys:
            return
        for key in removedKeys:
            if key in self.diskCache:
                del self.diskCache[key]
        self.__diskDB.DelByKeys(removedKeys)
        self._SyncDiskSize()
        TaskBase.taskObj.diskCacheRefresh.emit()

    def GetPathCacheKey(self, path):
        path = os.path.normpath(path).replace("/", "\\")
        return hashlib.md5(path.encode("utf-8")).hexdigest()

    def GetModelCachePath(self, path, model: dict):
        return path + "/" + f"model/{model.get('model', 0)}/scale/{model.get('scale', 0)}"

    def GetUrlCacheKey(self, url):
        return hashlib.md5(url.encode("utf-8")).hexdigest()

    def Stop(self):
        self._inQueue.put("")
