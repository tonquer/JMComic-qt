import json

from PySide6.QtWidgets import QWidget

from interface.ui_index import Ui_Index
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class IndexView(QWidget, Ui_Index, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Index.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.toolButton.clicked.connect(self.Init)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh:
            self.Init()
        pass

    def Init(self):
        self.isInit = True
        QtOwner().ShowLoading()
        self.bookList.clear()
        self.AddHttpTask(req.GetIndexInfoReq(), self.InitBack)

    def InitBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            if st == Status.Ok:
                boosList = raw["bookList"]
                for v in boosList:
                    self.bookList.AddBookItemByBook(v)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
            self.isInit = False
