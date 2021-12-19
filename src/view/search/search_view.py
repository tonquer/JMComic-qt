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
        self.dayCombox.currentIndexChanged.connect(self.ChangeSort)
        self.categoryBox.currentTextChanged.connect(self.ChangeCategoryBox)
        self.subCategoryBox.currentIndexChanged.connect(self.ChangeSubCategoryBox)
        self.searchButton.clicked.connect(self.lineEdit.Search)
        self.subCategoryBox.hide()

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
                maxPages = raw["maxPages"]
                self.bookList.UpdatePage(page, maxPages)
                self.spinBox.setValue(page)
                self.spinBox.setMaximum(maxPages)
                pageText = Str.GetStr(Str.Page) + ": " + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                bookList = raw["bookList"]
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
        sortDayList = ["a", "t", "w", "m"]

        sort = sortList[self.sortCombox.currentIndex()]
        sortDay = sortDayList[self.dayCombox.currentIndex()]

        data = {"全部":"", "其他漫画":"another", "同人志": "doujin", "汉化":"chinese", "日语": "japanese", "CG": "CG", "cosplay":"cosplay",
                "韩漫": "hanman", "美漫":"meiman", "短片":"short", "单本": "single", "请选择":""}
        category = data.get(Converter('zh-hans').convert(self.categoryBox.currentText()))
        subCategory = data.get(Converter('zh-hans').convert(self.subCategoryBox.currentText()))

        self.AddHttpTask(req.GetSearchReq(self.text, page, category, subCategory, sort=sort, sortDay=sortDay), self.SendSearchBack, page)

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

    def ChangeCategoryBox(self, text):
        # 其他漫画，another
        # 同人志, doujin, [汉化：chinese, 日语：japanese， CG:CG, cosplay:cosplay]
        # 韩漫  hanman
        # 美漫  meiman
        # 短片 short, [汉化：chinese, 日语：japanese]
        # 单本 single, [汉化：chinese, 日语：japanese]
        # data = {"全部":"", "其他漫画":"another", "同人志": "doujin", "汉化":"chinese", "日语": "japanese", "CG": "CG", "cosplay":"cosplay",
        #         "韩漫": "hanman", "美漫":"meiman", "短片":"short", "单本": "single"}
        self.subCategoryBox.setVisible(False)
        text = Converter('zh-hans').convert(text)
        self.subCategoryBox.clear()
        if text == "同人志":
            self.subCategoryBox.addItems(["请选择", "汉化", "日语", "CG", "cosplay"])
            self.subCategoryBox.setCurrentIndex(0)
        elif text == "短片" or text == "单本":
            self.subCategoryBox.setVisible(True)
            self.subCategoryBox.addItems(["请选择", "汉化", "日语"])
            self.subCategoryBox.setCurrentIndex(0)
        else:
            self.ChangeSort(text)
        return

    def ChangeSubCategoryBox(self, index):
        if index != 0:
            self.ChangeSort(index)
        return