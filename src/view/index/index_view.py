import datetime
import json

from PySide6.QtWidgets import QWidget, QVBoxLayout

from component.list.comic_list_widget import ComicListWidget
from interface.ui_index import Ui_Index
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.book import IndexInfo
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
        self.bookWidgetList.append(self.newListWidget)
        self.tabWidget.currentChanged.connect(self.SwitchCheck)
        self.newIndex = 0
        self.widget.setVisible(True)
        self.weekBox.setVisible(False)
        self.categoryBox.setVisible(False)
        self.newListWidget.LoadCallBack = self.LoadNextPage
        self.jumpButton.clicked.connect(self.JumpPage)
        self.filterTypes = ['novels', 'library']
        self.allIndex = {}
        self.weekIndex = 0
        now = datetime.datetime.now()
        self.weekBox.setCurrentIndex(now.weekday())
        self.categoryBox.currentIndexChanged.connect(self.LoadSerializationInfo)
        self.weekBox.currentIndexChanged.connect(self.LoadSerializationInfo)

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
                infos = raw["infos"]
                index = 1
                for info in infos:
                    assert isinstance(info, IndexInfo)
                    if info.type in self.filterTypes:
                        continue
                    self.allIndex[index] = info
                    w = self.AddTab(info.title)
                    if index == 1:
                        self.weekIndex = index
                        self.bookWidgetList[self.weekIndex].LoadCallBack = self.LoadNextPage
                    for v in info.bookList:
                        w.AddBookItemByBook(v)
                    index += 1
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
            self.weekBox.setVisible(False)
            self.categoryBox.setVisible(False)
            self.spinBox.setValue(1)
            self.newListWidget.clear()
            self.GetLatestInfo()
        elif self.tabWidget.currentIndex() == self.weekIndex:
            self.widget.setVisible(True)
            self.weekBox.setVisible(True)
            self.categoryBox.setVisible(True)
            self.bookWidgetList[self.weekIndex].clear()
            self.spinBox.setValue(1)
            self.GetSerializationInfo()
        else:
            self.widget.setVisible(False)
            self.weekBox.setVisible(False)
            self.categoryBox.setVisible(False)
        return

    def JumpPage(self):
        if self.tabWidget.currentIndex() == self.newIndex:
            self.newListWidget.clear()
            self.GetLatestInfo(self.spinBox.value())
        elif self.tabWidget.currentIndex() == self.weekIndex:
            self.bookWidgetList[self.weekIndex].clear()
            self.GetSerializationInfo()

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

    def LoadSerializationInfo(self):
        self.bookWidgetList[self.weekIndex].clear()
        self.GetSerializationInfo()

    def GetSerializationInfo(self, page=1):
        QtOwner().ShowLoading()
        day = self.weekBox.currentIndex() + 1
        if day > 7:
            day = 0
        typeIndex = ["all", "manga", "hanman"]
        type = typeIndex[self.categoryBox.currentIndex()]
        self.AddHttpTask(req.GetSerializationReq2(day, type, page), self.GetSerializationBack, page)

    def GetSerializationBack(self, raw, page):
        QtOwner().CloseLoading()
        st = raw["st"]
        self.bookWidgetList[self.weekIndex].UpdateState()
        if st == Status.Ok:
            bookList = raw["bookList"]
            for v in bookList:
                self.bookWidgetList[self.weekIndex].AddBookItemByBook(v)
            self.spinBox.setValue(page)
            self.spinBox.setMaximum(999)
            self.bookWidgetList[self.weekIndex].UpdatePage(page, 999)
        else:
            QtOwner().CheckShowMsg(raw)

    def LoadNextPage(self):
        if self.tabWidget.currentIndex() == self.newIndex:
            self.GetLatestInfo(self.newListWidget.page + 1)
        elif self.tabWidget.currentIndex() == self.weekIndex:
            self.GetSerializationInfo(self.bookWidgetList[self.weekIndex].page + 1)