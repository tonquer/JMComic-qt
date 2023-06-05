from functools import partial

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from component.layout.flow_layout import FlowLayout
from component.list.comic_list_widget import ComicListWidget
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
from interface.ui_category import Ui_Category
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from tools.book import Category
from tools.str import Str


class CategoryView(QWidget, Ui_Category, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Category.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.isInitNew = False
        self.bookWidgetList = []
        self.newIndex = 1
        self.indexCategory = {}
        self.tabWidget.currentChanged.connect(self.SwitchTab)
        self.jumpPage.clicked.connect(self._JumpPage)
        self.sortCombox.currentIndexChanged.connect(self._JumpPage)
        self.sortList = ["mr", "mv", "mv_m", "mv_w", "mv_t", "mp", "tf"]

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
                categoryTitle = raw["categoryTitle"]
                self.AddTitleTab(categoryTitle)
                for category in categoryList:
                    assert isinstance(category, Category)
                    self.indexCategory[self.newIndex] = category
                    w = self.AddTab(category.name)
                    self.newIndex += 1
                self.tabWidget.setCurrentIndex(0)

            else:
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)
            self.isInit = False

    def AddTitleTab(self, categoryTitle):
        scroll = SmoothScrollArea()
        scroll.setWidgetResizable(True)
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        for title, contentList in categoryTitle.items():
            verticalLayout.addWidget(QLabel(title))
            layout = FlowLayout()
            for text in contentList:
                box = QPushButton(text)
                box.clicked.connect(partial(self.SearchTitle, text))
                box.setMinimumWidth(160)
                layout.addWidget(box)
            verticalLayout.addLayout(layout)
        scroll.setWidget(tab)
        self.tabWidget.addTab(scroll, Str.GetStr(Str.Classify))
        return

    def SearchTitle(self, text):
        QtOwner().OpenSearch(text)

    def AddTab(self, name):
        tab = QWidget()
        verticalLayout = QVBoxLayout(tab)
        newListWidget = ComicListWidget(tab)
        newListWidget.LoadCallBack = self.LoadNextPage
        tab.bookWidget = newListWidget
        verticalLayout.addWidget(newListWidget)
        self.bookWidgetList.append(newListWidget)
        self.tabWidget.addTab(tab, name)
        return newListWidget

    def SwitchTab(self, index, page=1, isForce=False):
        if index == 0:
            self.spinBox.setVisible(False)
            self.label.setVisible(False)
            self.jumpPage.setVisible(False)
            self.sortCombox.setVisible(False)
            return
        else:
            self.spinBox.setVisible(True)
            self.label.setVisible(True)
            self.jumpPage.setVisible(True)
            self.sortCombox.setVisible(True)
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        if not isinstance(bookWidget, ComicListWidget):
            return
        category = self.indexCategory.get(index)
        if not category:
            return
        assert isinstance(category, Category)
        self.spinBox.setMaximum(bookWidget.pages)
        self.spinBox.setValue(bookWidget.page)
        self.label.setText(bookWidget.GetPageStr())

        if bookWidget.count() > 0 and not isForce:
            return

        QtOwner().ShowLoading()
        bookWidget.clear()
        sortId = self.sortList[self.sortCombox.currentIndex()]
        self.AddHttpTask(req.GetSearchCategoryReq2(category.slug, page=page, sort=sortId), self._SearchCategoryBack, (page, index))

    def _JumpPage(self):
        index = self.tabWidget.currentIndex()
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        if not isinstance(bookWidget, ComicListWidget):
            return
        category = self.indexCategory.get(index)
        if not category:
            return
        page = int(self.spinBox.text())
        if page > bookWidget.pages:
            return

        self.SwitchTab(index, page, True)

    def _SearchCategoryBack(self, raw, v):
        page, index = v
        QtOwner().CloseLoading()
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        assert isinstance(bookWidget, ComicListWidget)
        category = self.indexCategory.get(index)
        bookWidget.UpdateState()

        if raw["st"] == Status.Ok:
            bookList = raw["bookList"]
            total = raw["total"]
            if page == 1:
                maxPages = (total - 1) // max(1, len(bookList)) + 1
                bookWidget.UpdateMaxPage(maxPages)
                self.spinBox.setMaximum(maxPages)
            bookWidget.UpdatePage(page, bookWidget.pages)
            self.label.setText(bookWidget.GetPageStr())
            for v in bookList:
                bookWidget.AddBookItemByBook(v)
        else:
            QtOwner().CheckShowMsg(raw)

    def LoadNextPage(self):
        index = self.tabWidget.currentIndex()
        w = self.tabWidget.widget(index)
        bookWidget = getattr(w, "bookWidget", "")
        if not isinstance(bookWidget, ComicListWidget):
            return
        QtOwner().ShowLoading()
        category = self.indexCategory.get(index)
        assert isinstance(category, Category)
        sortId = self.sortList[self.sortCombox.currentIndex()]
        self.AddHttpTask(req.GetSearchCategoryReq2(category.name, bookWidget.page + 1, sortId), self._SearchCategoryBack, (bookWidget.page + 1, index))
        return