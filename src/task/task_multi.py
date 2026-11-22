from multiprocessing import Process, Queue
import  multiprocessing
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
        try:
            (taskType, args) = item
            if taskType == TaskMulti.MultiTaskSegment:
                result = ToolUtil.SegmentationPicture(*args)
            elif taskType == TaskMulti.MultiTaskSegmentToDisk:
                result = ToolUtil.SegmentationPictureToDisk(*args)
            else:
                result = None
            finishQue.put(result)
        except Exception as es:
            print("error, es:{}".format(es))
            finishQue.put(None)

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

    def Start(self):
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
        for queue in self.queueList:
            queue.put(None)
            self._inQueue.put(-1)
        # for process in self.multi_list:
        #     process.stop()
        return

    def GetJmPicResultsResult(self, imgData, saveParam1, saveParam2, saveParam3):
        index = self._inQueue.get()
        if index < 0:
            return None
        try:
            while not self.queueFinishList[index].empty():
                try:
                    self.queueFinishList[index].get_nowait()
                except Exception:
                    break
            self.queueList[index].put((TaskMulti.MultiTaskSegment, (imgData, saveParam1, saveParam2, saveParam3)))
            return self.queueFinishList[index].get(timeout=30)
        except Exception as es:
            Log.Error(es)
            return None
        finally:
            self._inQueue.put(index)

    # def SaveJmPicResultsResult(self, imgData, saveParam1, saveParam2, saveParam3, path, format):
    #     index = self._inQueue.get()
    #     if index < 0:
    #         return None
    #     self.queueList[index].put((TaskMulti.MultiTaskSegmentToDisk, (imgData, saveParam1, saveParam2, saveParam3, path, format)))
    #     result = self.queueFinishList[index].get()
    #     self._inQueue.put(index)
    #     return result
