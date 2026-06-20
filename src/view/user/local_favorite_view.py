import json

from PySide6 import QtWidgets

from config.setting import Setting
from interface.ui_local_favorite import Ui_LocalFavorite
from qt_owner import QtOwner
from server import req, Log, config
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
        self.bookList.isMoveMenu = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.bookList.MoveCallBack = self.MoveCallBack
        self.resetCnt = 5
        self.sortIdCombox.currentIndexChanged.connect(self.RefreshDataFocus)
        self.sortKeyCombox.currentIndexChanged.connect(self.RefreshDataFocus)

        # TODO 判断是否使用本地
        # self.widget.hide()
        self.lineEdit.textChanged.connect(self.SearchTextChange)
        self.searchText = ""
        self.db = LocalFavoriteDb()
        bookList = self.db.SearchFavorite(-1, 0, 0, 0, "")
        self.allBookIds = set(bookList.keys())
        self.allDownButton.clicked.connect(self.OpenSomeBook)
        self.importButton.clicked.connect(self.ImportFavorite)
        self.loadPage = 1
        self.maxPage = 1
        self.loadFidNum = 0
        self.loadFid = []
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.folderBox.currentIndexChanged.connect(self.RefreshDataFocus)

    def GetFidByName(self, name):
        for k, v in self.folderDict.items():
            if v == name:
                return k
        return 0

    def OpenSomeBook(self):
        name = self.folderBox.currentText()
        fid = self.GetFidByName(name)
        if fid > 0:
            books = list(self.fidBookList.get(fid, []))
        else:
            books = list(self.allBookIds)
        QtOwner().OpenSomeDownload(books)
        return

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh or self.bookList.count() <= 0:
            self.InitFolder()
            self.RefreshDataFocus()

    def ImportFavorite(self):
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        QtOwner().ShowLoading()
        sort = "mr"
        fid = ""
        self.loadPage = 1
        self.maxPage = 1
        self.loadFidNum = 0
        self.loadFid = []
        self.AddHttpTask(req.GetFavoritesReq2(self.loadPage, sort, fid), self.ImportFavoriteBack, (self.loadPage, ""))
        return

    def ImportFavoriteBack(self, raw, v):
        (page, fidName) = v
        try:
            st = raw["st"]
            if st == Status.Ok:
                f = raw["favorite"]
                total = f.total
                count = f.count
                bookList = f.bookList
                if page == 1:
                    self.maxPage = (total - 1) // max(1, count) + 1
                    if not self.loadFid:
                        self.loadFid = [(k, v) for k,v in f.fold.items()]
                        self.loadFid.insert(0, ("", ""))
                        for name, _ in self.loadFid:
                            self.AddFidByName(name)

                for book in bookList:
                    self.AddFavoritesAndFidName(book, fidName)
            else:
                QtOwner().CloseLoading()
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)
        finally:
            self.ImportNextFidFavorite()

    def ImportNextFidFavorite(self):
        if self.loadPage >= self.maxPage:
            if self.loadFidNum >= len(self.loadFid)-1:
                QtOwner().CloseLoading()
                QtOwner().ShowMsg(Str.GetStr(Str.Ok))
                self.RefreshData()
                return
            else:
                sort = "mr"
                self.loadPage = 1
                self.maxPage = 1
                self.loadFidNum += 1
                name, fid = self.loadFid[self.loadFidNum]
                self.AddHttpTask(req.GetFavoritesReq2(self.loadPage, sort, fid), self.ImportFavoriteBack, (self.loadPage, name))
                return
        else:
            sort = "mr"
            self.loadPage += 1
            name, fid = self.loadFid[self.loadFidNum]
            self.AddHttpTask(req.GetFavoritesReq2(self.loadPage, sort, fid), self.ImportFavoriteBack, (self.loadPage, name))

    def SearchTextChange(self, text):
        self.searchText = text
        self.bookList.clear()
        self.LoadBookList()

    def LoadBookList(self):
        sortId = self.sortIdCombox.currentIndex()
        sortKey = self.sortKeyCombox.currentIndex()
        name = self.folderBox.currentText()
        fid = self.GetFidByName(name)
        bookList = self.db.SearchFavorite(self.bookList.page, sortKey, sortId, fid, self.searchText)
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
        self.bookList.DelBookID(bookId)
        # self.RefreshDataFocus()
        pass

    def IsHave(self, bookId):
        return str(bookId) in self.allBookIds

    def AddFavorites(self, bookInfo):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.baseInfo.id))

    def AddFavoritesAndFidName(self, bookInfo, fidName):
        self.db.AddBookToDB(bookInfo)
        self.allBookIds.add(str(bookInfo.baseInfo.id))
        fid = self.GetFidByName(fidName)
        self.db.AddBookFavoriteFid(str(bookInfo.baseInfo.id), fid)
        self.fidBookList = self.db.LoadBookFold()

    def DelFavorites(self, bookId):
        self.db.DelFavoriteDB(bookId)
        self.allBookIds.discard(str(bookId))
        self.fidBookList = self.db.LoadBookFold()

    def AddFidByName(self, name):
        if not name:
            return False
        fid = 0
        for k, v in self.folderDict.items():
            if v == name:
                fid = k
                break
        if (fid > 0):
            return False
        isSuc = self.db.AddFavoriteFid(name)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.InitFolder()
        return isSuc

    def DelFidByName(self, name):
        fid = 0
        for k, v in self.folderDict.items():
            if v == name:
                fid = k
                break
        if not fid:
            return False
        isSuc = self.db.DelFavoriteFid(fid)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()
        self.InitFolder()
        return isSuc

    def UpdateBookFid(self, bookId, fids):
        isSuc = self.db.UpdateBookFavoriteFid(bookId, fids)
        self.folderDict = self.db.LoadFold()
        self.fidBookList = self.db.LoadBookFold()

        return isSuc

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

    def InitFolder(self):
        self.ClearFolder()
        items = list(self.folderDict.values())
        self.folderBox.addItems(items)
        return

    def ClearFolder(self):
        self.folderBox.currentIndexChanged.disconnect()
        self.folderBox.clear()
        self.folderBox.addItem(Str.GetStr(Str.All))
        self.folderBox.setCurrentIndex(0)
        self.folderBox.currentIndexChanged.connect(self.RefreshDataFocus)
        return


    def MoveCallBack(self, bookId):
        QtOwner().OpenLocalFavoriteFold(bookId, self.MoveOkBack, self.FoldChangeBack)
        return

    def MoveOkBack(self):
        self.RefreshDataFocus()
        return

    def FoldChangeBack(self):
        self.RefreshDataFocus()
        return