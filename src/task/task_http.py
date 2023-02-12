import pickle
from types import FunctionType

from tools.log import Log
from task.qt_task import QtTaskQObject, TaskBase, QtHttpTask


class TaskHttp(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.taskBack.connect(self.HandlerTask)

    def AddHttpTask(self, req, callBack=None, backParam=None, cleanFlag=None):
        self.taskId += 1
        info = QtHttpTask(self.taskId)
        info.callBack = callBack
        info.backParam = backParam
        self.tasks[self.taskId] = info
        if cleanFlag:
            info.cleanFlag = cleanFlag
            taskIds = self.flagToIds.setdefault(cleanFlag, set())
            taskIds.add(self.taskId)

        from server.server import Server
        if isinstance(req, FunctionType):
            req(self.taskId)
        else:
            from server.server import Server
            Server().Send(req, backParam=self.taskId)
        return

    def HandlerTask(self, taskId, data):
        try:
            info = self.tasks.get(taskId)
            data = pickle.loads(data)
            if not info:
                Log.Warn("[Task] not find taskId:{}, {}".format(taskId, data))
                return
            assert isinstance(info, QtHttpTask)
            if info.cleanFlag:
                taskIds = self.flagToIds.get(info.cleanFlag, set())
                taskIds.discard(info.taskId)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(data)
                else:
                    info.callBack(data, info.backParam)
            del info.callBack
            del self.tasks[taskId]
        except Exception as es:
            Log.Error(es)