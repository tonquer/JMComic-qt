import pickle
from types import FunctionType

from task.qt_task import TaskBase
from tools.log import Log


class QtHttpTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""
        self.requestGen = 0


class TaskHttp(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.taskBack.connect(self.HandlerTask)

    def AddHttpTask(self, req, callBack=None, backParam=None, cleanFlag=None):
        info = QtHttpTask(0)
        info.callBack = callBack
        info.backParam = backParam
        # 记录入队时的请求代次；登出后代次变化，回调会被丢弃
        from qt_owner import QtOwner
        info.requestGen = QtOwner().requestGeneration

        taskId = self._RegisterTask(info, cleanFlag)
        try:
            if isinstance(req, FunctionType):
                req(taskId)
            else:
                from server.server import Server
                Server().Send(req, backParam=taskId)
        except Exception:
            self._TakeTask(taskId)
            raise
        return

    def HandlerTask(self, taskId, data):
        try:
            info = self._TakeTask(taskId)
            if not info:
                return
            data = pickle.loads(data)
            assert isinstance(info, QtHttpTask)
            if info.callBack:
                from qt_owner import QtOwner
                if info.requestGen != QtOwner().requestGeneration:
                    # 会话已切换（登出）：请求发出后的返回值不能再交给界面，
                    # 否则旧账号的数据会重新填回收藏/历史等列表
                    Log.Info("[Task] drop stale callback after session switch, taskId:{}".format(taskId))
                elif info.backParam is None:
                    info.callBack(data)
                else:
                    info.callBack(data, info.backParam)
        except Exception as es:
            Log.Error(es)
