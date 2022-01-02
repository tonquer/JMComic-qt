import json

from PySide6.QtWidgets import QWidget, QVBoxLayout

from component.list.comic_list_widget import ComicListWidget
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
        self.isInitNew = False
        self.bookWidgetList = []
        self.tabWidget.currentChanged.connect(self.SwitchCheck)
        self.newIndex = 0

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh and not self.isInit:
            self.Init()
        pass

    def Init(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetIndexInfoReq2(), self.InitBack)

    def InitBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            if st == Status.Ok:
                self.isInit = True
                bookInfo = raw["bookInfo"]
                for key, bookList in bookInfo.items():
                    w = self.AddTab(key)
                    self.newIndex += 1
                    for v in bookList:
                        w.AddBookItemByBook(v)
                self.tabWidget.setCurrentIndex(0)
            else:
                QtOwner().CheckShowMsg( raw)
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def AddTab(self, name):
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        newListWidget = ComicListWidget(tab)
        verticalLayout.addWidget(newListWidget)
        self.bookWidgetList.append(newListWidget)
        self.tabWidget.insertTab(0, tab, name)
        return newListWidget

    def SwitchCheck(self, index):
        if self.tabWidget.currentIndex() == self.newIndex and not self.isInitNew:
            QtOwner().ShowLoading()
            self.AddHttpTask(req.GetLatestInfoReq2(), self.GetLatestInfoBack)
        return

    def GetLatestInfoBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.isInitNew = True
            bookList = raw["bookList"]
            for v in bookList:
                self.newListWidget.AddBookItemByBook(v)
        else:
            QtOwner().CheckShowMsg( raw)
