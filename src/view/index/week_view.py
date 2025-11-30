import json

from PySide6.QtWidgets import QWidget, QVBoxLayout

from component.list.comic_list_widget import ComicListWidget
from interface.ui_index import Ui_Index
from interface.ui_week import Ui_Week
from qt_owner import QtOwner
from server import req, Log, Status, ToolUtil
from task.qt_task import QtTaskBase
from tools.str import Str


class WeekView(QWidget, Ui_Week, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Week.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.isInitNew = False
        self.bookWidgetList = []
        self.tabWidget.currentChanged.connect(self.SwitchCheck)
        self.newIndex = 0

        self.comboIndexDict = {}
        self.typeIndexDict = {
            0: "manga",
            1: "hanman",
            2: "another"
        }

    def SwitchCurrent(self, **kwargs):
        self.update()
        refresh = kwargs.get("refresh")
        if refresh and not self.isInit:
            self.Init()
        pass

    def Init(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetWeekCategoriesReq2(), self.InitBack)

    def InitBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            data =raw.get('data')
            if st == Status.Ok:
                self.isInit = True
                width = 200
                maxSize = 1
                for i, v in enumerate(data.get('categories')):
                    index = v.get("id")
                    self.comboIndexDict[i] = index
                    title = v.get('time') + " - " + v.get("title")
                    if len(title) > maxSize:
                        maxSize = len(title)
                    self.comboBox.addItem(title)
                maxSize = min(800, maxSize * 20*0.8)
                self.comboBox.setFixedWidth(maxSize)
                self.comboBox.currentIndexChanged.connect(self.SwitchCheck)
            else:
                QtOwner().CheckShowMsg(raw)
            self.GetWeekFilterInfo()
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def SwitchCheck(self):
        self.GetWeekFilterInfo()

    def GetWeekFilterInfo(self):
        QtOwner().ShowLoading()
        id = self.comboIndexDict.get(self.comboBox.currentIndex())
        type = self.typeIndexDict.get(self.tabWidget.currentIndex())
        self.AddHttpTask(req.GetWeekFilterReq2(id, type), self.GetWeekFilterBack, self.tabWidget.currentIndex())

    def GetWeekFilterBack(self, raw, index):
        QtOwner().CloseLoading()
        st = raw["st"]
        if index == 0:
            widget = self.mangaWidget
        elif index == 1:
            widget = self.hanmanWidget
        elif index == 2:
            widget = self.anotherWidget
        else:
            return
        widget.clear()
        if st == Status.Ok:
            self.isInitNew = True
            for v in raw.get("data").get("list"):
                v2 = ToolUtil.ParseBookInfo(v)
                widget.AddBookItemByBook(v2)
        else:
            QtOwner().CheckShowMsg(raw)
