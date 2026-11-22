import itertools
import multiprocessing
import time
from multiprocessing import Process, Queue
from queue import Empty

from config.setting import Setting
from task.qt_task import TaskBase
from tools.log import Log
from tools.tool import ToolUtil


# 定义消费者函数
def consumer(num, queue, finishQue):
    print(f"start consumer multiprocess, index:{num}")
    while True:
        item = queue.get()
        if item is None:
            break  # 结束信号
        reqId = None
        try:
            (reqId, taskType, args) = item
            if taskType == TaskMulti.MultiTaskSegment:
                result = ToolUtil.SegmentationPicture(*args)
            elif taskType == TaskMulti.MultiTaskSegmentToDisk:
                result = ToolUtil.SegmentationPictureToDisk(*args)
            else:
                result = None
            finishQue.put((reqId, result))
        except Exception as es:
            print("error, es:{}".format(es))
            finishQue.put((reqId, None))

        # print(f"finish consumer multiprocess, index:{num}")


# 多进程
class TaskMulti(TaskBase):
    MultiTaskSegment = 1
    MultiTaskSegmentToDisk = 2

    def __init__(self) -> None:
        TaskBase.__init__(self)
        self.multi_list = []
        self.startNum = 0
        self.queueList = []
        self.queueFinishList = []
        self.allMultiState = {}
        self._reqIdGen = itertools.count(1)
        self._stopped = False

    def Start(self):
        with self._taskLock:
            self._stopped = False
        for i in range(max(1, Setting.MultiNum.value)):
            queue = Queue()
            queue2 = Queue()
            self.queueList.append(queue)
            self.queueFinishList.append(queue2)
            process = Process(target=consumer, args=(i, queue, queue2), daemon=True)
            process.start()
            self.multi_list.append(process)
            self._inQueue.put(i)

    def Stop(self):
        with self._taskLock:
            if self._stopped:
                return
            self._stopped = True
            queues = list(self.queueList)
        for queue in queues:
            try:
                queue.put(None)
            except Exception:
                pass
            self._inQueue.put(-1)
        # for process in self.multi_list:
        #     process.stop()
        return

    def _RestartWorker(self, index):
        if self._stopped:
            return False
        oldProc = self.multi_list[index]
        try:
            if oldProc is not None and oldProc.is_alive():
                oldProc.terminate()
            if oldProc is not None:
                oldProc.join(timeout=1)
        except Exception as es:
            Log.Error(es)
        for oldQ in (self.queueList[index], self.queueFinishList[index]):
            try:
                oldQ.close()
                oldQ.cancel_join_thread()
            except Exception:
                pass
        queue = Queue()
        queue2 = Queue()
        process = Process(target=consumer, args=(index, queue, queue2), daemon=True)
        process.start()
        with self._taskLock:
            if self._stopped:
                try:
                    queue.put(None)
                except Exception:
                    pass
                return False
            self.queueList[index] = queue
            self.queueFinishList[index] = queue2
            self.multi_list[index] = process
        Log.Warn(f"restarted dead TaskMulti worker process, index:{index}")
        return True

    def GetJmPicResultsResult(self, imgData, saveParam1, saveParam2, saveParam3):
        index = self._inQueue.get()
        if index < 0 or self._stopped:
            return None
        try:
            if not self.multi_list[index].is_alive():
                if not self._RestartWorker(index):
                    return None
            finishQueue = self.queueFinishList[index]
            while True:
                try:
                    finishQueue.get_nowait()
                except Empty:
                    break
                except Exception:
                    break
            with self._taskLock:
                reqId = next(self._reqIdGen)
            self.queueList[index].put((reqId, TaskMulti.MultiTaskSegment, (imgData, saveParam1, saveParam2, saveParam3)))
            deadline = time.monotonic() + 30
            while True:
                if self._stopped:
                    return None
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    Log.Warn(f"TaskMulti timeout waiting for reqId:{reqId}, index:{index}")
                    return None
                if not self.multi_list[index].is_alive():
                    Log.Warn(f"TaskMulti worker died while processing reqId:{reqId}, index:{index}")
                    return None
                waitTime = min(remaining, 1.0)
                try:
                    resp = finishQueue.get(timeout=waitTime)
                except Empty:
                    continue
                if isinstance(resp, tuple) and len(resp) == 2:
                    respId, result = resp
                    if respId == reqId:
                        return result
                    Log.Warn(f"TaskMulti discard stale respId:{respId}, expected reqId:{reqId}, index:{index}")
        except Exception as es:
            Log.Error(es)
            return None
        finally:
            if not self._stopped:
                try:
                    if not self.multi_list[index].is_alive():
                        self._RestartWorker(index)
                except Exception as es:
                    Log.Error(es)
                if not self._stopped:
                    self._inQueue.put(index)

    # def SaveJmPicResultsResult(self, imgData, saveParam1, saveParam2, saveParam3, path, format):
    #     index = self._inQueue.get()
    #     if index < 0:
    #         return None
    #     self.queueList[index].put((TaskMulti.MultiTaskSegmentToDisk, (imgData, saveParam1, saveParam2, saveParam3, path, format)))
    #     result = self.queueFinishList[index].get()
    #     self._inQueue.put(index)
    #     return result
