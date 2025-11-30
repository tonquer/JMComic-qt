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
        self.widget.setVisible(True)
        self.newListWidget.LoadCallBack = self.LoadNextPage
        self.jumpButton.clicked.connect(self.JumpPage)

    def SwitchCurrent(self, **kwargs):
        self.update()
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
                    for v in bookList:
                        w.AddBookItemByBook(v)
                self.tabWidget.setCurrentIndex(0)
            else:
                QtOwner().CheckShowMsg( raw)
            self.GetLatestInfo()
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def AddTab(self, name):
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        newListWidget = ComicListWidget(tab)
        verticalLayout.addWidget(newListWidget)
        self.bookWidgetList.append(newListWidget)
        self.tabWidget.addTab(tab, name)
        return newListWidget

    def SwitchCheck(self, index):
        if self.tabWidget.currentIndex() == self.newIndex:
            QtOwner().ShowLoading()
            self.widget.setVisible(True)
            self.newListWidget.clear()
            self.GetLatestInfo()
        else:
            self.widget.setVisible(False)
        return

    def JumpPage(self):
        self.newListWidget.clear()
        self.GetLatestInfo(self.spinBox.value())

    def GetLatestInfo(self, page=1):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetLatestInfoReq2(page-1), self.GetLatestInfoBack, page)

    def GetLatestInfoBack(self, raw, page):
        QtOwner().CloseLoading()
        st = raw["st"]
        self.newListWidget.UpdateState()
        if st == Status.Ok:
            self.isInitNew = True
            bookList = raw["bookList"]
            for v in bookList:
                self.newListWidget.AddBookItemByBook(v)
            self.spinBox.setValue(page)
            self.spinBox.setMaximum(999)
            self.newListWidget.UpdatePage(page, 999)
        else:
            QtOwner().CheckShowMsg(raw)

    def LoadNextPage(self):
        self.GetLatestInfo(self.newListWidget.page + 1)