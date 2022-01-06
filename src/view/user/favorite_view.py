import json

from PySide6 import QtWidgets

from config import config
from interface.ui_favorite import Ui_Favorite
from qt_owner import QtOwner
from server import req, Log
from task.qt_task import QtTaskBase
from tools.book import FavoriteInfo
from tools.status import Status
from tools.str import Str


class FavoriteView(QtWidgets.QWidget, Ui_Favorite, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Favorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)

        self.dealCount = 0
        self.dirty = False

        # self.bookList.InitBook(self.LoadNextPage)

        self.sortList = ["mr", "mp"]
        # self.bookList.InstallDel()

        self.sortId = 1
        # self.reupdateBookIds = set()
        # self.allFavoriteIds = dict()
        # self.maxSortId = 0
        self.bookList.isDelMenu = True
        self.bookList.isMoveMenu = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.MoveCallBack = self.MoveCallBack
        self.bookList.DelCallBack = self.DelCallBack
        self.resetCnt = 5
        self.sortCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.folderBox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.folderDict = {}

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    # def UpdatePageNum(self):
    #     maxFovorite = len(self.allFavoriteIds)
    #     self.bookList.pages = max(0, (maxFovorite-1)) // 20 + 1
    #     self.pages.setText("{}/{}".format(self.bookList.page, self.bookList.pages) + Str.GetStr(Str.Page))
    #     self.nums.setText(Str.GetStr(Str.FavoriteNum) + ": {}".format(maxFovorite))
    #     self.spinBox.setValue(self.bookList.page)
    #     self.spinBox.setMaximum(self.bookList.pages)
    #     self.bookList.UpdateState()

    def RefreshDataFocus(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def DelCallBack(self, bookId):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.AddAndDelFavoritesReq2(bookId), self.DelAndFavoritesBack, bookId)
        pass

    def MoveCallBack(self, bookId):
        name = self.folderBox.currentText()
        fid = self.folderDict.get(name, "")
        QtOwner().OpenFavoriteFold(bookId, fid, self.MoveOkBack, self.FoldChangeBack)
        return

    def MoveOkBack(self):
        self.RefreshDataFocus()
        return

    def FoldChangeBack(self):
        self.RefreshDataFocus()
        return

    def DelAndFavoritesBack(self, raw, bookId):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.RefreshDataFocus()
        QtOwner().CheckShowMsg(raw)

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData()

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self):
        QtOwner().ShowLoading()
        sort = self.sortList[self.sortCombox.currentIndex()]
        name = self.folderBox.currentText()
        index = max(0, self.folderBox.currentIndex())
        fid = self.folderDict.get(name, "")
        self.AddHttpTask(req.GetFavoritesReq2(self.bookList.page, sort, fid), self.SearchBack, (self.bookList.page, index))

    def SearchBack(self, raw, v):
        page, index = v
        QtOwner().CloseLoading()
        try:
            st = raw["st"]
            if st == Status.Ok:
                f = raw["favorite"]
                assert isinstance(f, FavoriteInfo)
                total = f.total
                count = f.count
                bookList = f.bookList
                self.bookList.UpdateState()
                if page == 1:
                    maxPage = (total - 1) // max(1, count) + 1
                    self.bookList.UpdatePage(page, maxPage)
                    self.spinBox.setMaximum(maxPage)
                    if not self.folderDict:
                        self.folderDict = f.fold.copy()
                        self.InitFolder(index)

                self.nums.setText(Str.GetStr(Str.FavoriteNum) + ":{}/{}".format(page, self.bookList.pages))
                for book in bookList:
                    self.bookList.AddBookItemByBook(book)
            else:
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)

    def InitFolder(self, index):
        self.ClearFolder()
        items = list(self.folderDict.keys())
        items.insert(0, "全部")
        self.folderBox.addItems(items)
        self.folderBox.setCurrentIndex(index)
        return

    def ClearFolder(self):
        self.folderBox.clear()
        return