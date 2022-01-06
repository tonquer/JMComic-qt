from PySide6.QtWidgets import QWidget, QVBoxLayout

from component.list.comic_list_widget import ComicListWidget
from interface.ui_category import Ui_Category
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from tools.book import Category


class CategoryView(QWidget, Ui_Category, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Category.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.isInitNew = False
        self.bookWidgetList = []
        self.newIndex = 0
        self.indexCategory = {}
        self.tabWidget.currentChanged.connect(self.SwitchTab)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if refresh and not self.isInit:
            self.Init()
        pass

    def Init(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetCategoryReq2(), self.InitBack)

    def InitBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            if st == Status.Ok:
                self.isInit = True
                categoryList = raw["categoryList"]
                for category in categoryList:
                    assert isinstance(category, Category)
                    w = self.AddTab(category.name)
                    self.indexCategory[self.newIndex] = category
                    self.newIndex += 1
                self.tabWidget.setCurrentIndex(0)
            else:
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def AddTab(self, name):
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        newListWidget = ComicListWidget(tab)
        tab.bookWidget = newListWidget
        verticalLayout.addWidget(newListWidget)
        self.bookWidgetList.append(newListWidget)
        self.tabWidget.addTab(tab, name)
        return newListWidget

    def SwitchTab(self, index):
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        if not isinstance(bookWidget, ComicListWidget):
            return
        category = self.indexCategory.get(index)
        assert isinstance(category, Category)
        QtOwner().ShowLoading()
        bookWidget.clear()
        self.AddHttpTask(req.GetSearchCategoryReq2(category.name), self._SearchCategoryBack, (1, index))

    def _SearchCategoryBack(self, raw, v):
        page, index = v
        QtOwner().CloseLoading()
        if raw["st"] == Status.Ok:
            w = self.tabWidget.widget(index)
            bookWidget = getattr(w, "bookWidget", "")
            assert isinstance(bookWidget, ComicListWidget)
            bookList = raw["bookList"]
            total = raw["total"]
            if page == 1:
                maxPages = (total - 1) // max(1, len(bookList)) + 1
                bookWidget.UpdatePage(page, maxPages)
                # self.spinBox.setMaximum(maxPages)
            for v in bookList:
                bookWidget.AddBookItemByBook(v)
        else:
            QtOwner().CheckShowMsg(raw)

    def LoadNextPage(self, index):
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        if not isinstance(bookWidget, ComicListWidget):
            return
        QtOwner().ShowLoading()
        category = self.indexCategory.get(index)
        assert isinstance(category, Category)
        self.AddHttpTask(req.GetSearchCategoryReq2(category.name, bookWidget.page + 1), self._SearchCategoryBack, (bookWidget.page + 1, index))
        return