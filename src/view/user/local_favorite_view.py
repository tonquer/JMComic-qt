import json

from PySide6 import QtWidgets

from config.setting import Setting
from interface.ui_local_favorite import Ui_LocalFavorite
from qt_owner import QtOwner
from server import req, Log
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.status import Status
from tools.str import Str
from view.user.local_favorite_db import LocalFavoriteDb


class LocalFavoriteView(QtWidgets.QWidget, Ui_LocalFavorite, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LocalFavorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.dealCount = 0
        self.dirty = False

        # self.bookList.InitBook(self.LoadNextPage)

        self.sortList = ["dd", "da"]
        # self.bookList.InstallDel()

        self.sortId = 1
        self.reupdateBookIds = set()
        self.maxSortId = 0
        self.bookList.isDelMenu = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.resetCnt = 5
        self.sortIdCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortKeyCombox.currentIndexChanged.connect(self.RefreshDataFocus)

        # TODO 判断是否使用本地
        # self.widget.hide()
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.searchText = ""
        self.db = LocalFavoriteDb()
        bookList = self.db.SearchFavorite(-1, 0, 0, "")
        self.allBookIds = set(bookList.keys())

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    def SearchTextChange(self, text):
        self.searchText = text
        self.bookList.clear()
        self.LoadBookList()

    def LoadBookList(self):
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        bookList = self.db.SearchFavorite(self.bookList.page, sortKey, sortId, self.searchText)
        self.SearchLocalBack(bookList.values())

    def SearchTextChangeBack(self, bookList):
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        for info in bookList:
            self.bookList.AddBookItemByBook(info, isShowHistory=True)
        self.UpdatePageNum()
        return

    def UpdatePageNum(self):
        maxFovorite = len(self.allBookIds)
        self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
        self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
        self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
        self.spinBox.setValue(self.bookList.page)
        self.spinBox.setMaximum(self.bookList.pages)
        self.bookList.UpdateState()

    def RefreshDataFocus(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookId):
        self.DelFavorites(bookId)
        self.RefreshDataFocus()
        pass

    def IsHave(self, bookId):
        return str(bookId) in self.allBookIds

    def AddFavorites(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.baseInfo.id))

    def DelFavorites(self, bookId):
        self.db.DelFavoriteDB(bookId)
        self.allBookIds.discard(str(bookId))

    def LoadNextPage(self):
        self.bookList.page += 1
        self.LoadBookList()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().ShowLoading()
        self.SearchTextChange(self.searchText)

    def SearchLocalBack(self, bookList):
        QtOwner().CloseLoading()
        for info in bookList:
            self.bookList.AddBookItemByBook(info, isShowHistory=True)
        self.UpdatePageNum()
        return
