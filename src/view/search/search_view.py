import json

from PySide6.QtWidgets import QWidget

from interface.ui_search import Ui_Search
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.langconv import Converter
from tools.str import Str


class SearchView(QWidget, Ui_Search, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Search.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.categories = ""
        self.text = ""
        self.isLocal = True
        self.isTitle = True
        self.isDes = True
        self.isCategory = True
        self.isTag = True
        self.isAuthor = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.sortCombox.currentIndexChanged.connect(self.ChangeSort)
        self.searchButton.clicked.connect(self.lineEdit.Search)

    def InitWord(self):
        self.lineEdit.LoadCacheWord()
        self.lineEdit.SetCacheWord()
        return

    def Stop(self):
        self.lineEdit.SaveCacheWord()

    def SwitchCurrent(self, **kwargs):
        text = kwargs.get("text")
        if text is not None:
            self.text = text
            self.lineEdit.setText(self.text)
            self.bookList.clear()

            self.lineEdit.AddCacheWord(self.text)
            self.SendSearch(1)
        pass

    def SendSearchBack(self, raw, page):
        QtOwner().CloseLoading()
        try:
            self.bookList.UpdateState()
            st = raw["st"]
            if st == Status.Ok:
                total = raw["total"]
                bookList = raw["bookList"]
                if page != 1:
                    maxPages = (total - 1) // max(1, len(bookList)) + 1
                    self.bookList.UpdatePage(page, maxPages)
                    self.spinBox.setMaximum(maxPages)
                self.spinBox.setValue(page)
                pageText = Str.GetStr(Str.Page) + ": " + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for v in bookList:
                    self.bookList.AddBookItemByBook(v)
            else:
                # QtWidgets.QMessageBox.information(self, '未搜索到结果', "未搜索到结果", QtWidgets.QMessageBox.Yes)
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)
        pass

    def SendSearch(self, page):
        QtOwner().ShowLoading()
        sortList = ["mr", "mv", "mp", "tf"]
        sort = sortList[self.sortCombox.currentIndex()]
        self.AddHttpTask(req.GetSearchReq2(self.text, sort, page), self.SendSearchBack, page)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.SendSearch(page)
        return

    def LoadNextPage(self):
        self.SendSearch(self.bookList.page + 1)
        return

    def ChangeSort(self, pos):
        self.bookList.page = 1
        self.bookList.clear()
        self.SendSearch(1)
