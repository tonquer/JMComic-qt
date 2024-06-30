import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QHeaderView, QAbstractItemView, QWidget

from component.dialog.base_mask_dialog import BaseMaskDialog
from config import config
from config.setting import Setting
from interface.ui_download_some import Ui_DownloadSome
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str
from server import req, Status
import re
from tools.book import BookMgr
from view.download.download_some_edit_view import DownloadSomeEditView
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem
from PySide6.QtCore import Qt, QTimer, QUrl


class SomeItem:
    def __init__(self) -> None:
        self.bookId = ""
        self.title = ""
        self.rowCount = 0
        self.st = 0
        self.epsLen = 0


class DownloadSomeView(QWidget, Ui_DownloadSome, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_DownloadSome.__init__(self)
        QtTaskBase.__init__(self)

        self.setupUi(self)
        self.inputButton.clicked.connect(self.OpenEdit)
        self.loadInfoButton.clicked.connect(self.Start)
        self.cleanButton.clicked.connect(self.Clean)
        self.downButton.clicked.connect(self.Download)
        self.nasButton.clicked.connect(self.AddNas)
        
        self.allBookInfo = {}  # bookId: SomeItem
        self.loadingBook = []
        self.completeNum = 0
        self.completeBook = []
        self.order = {}
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.tableWidget.setColumnWidth(0, 40)
        print(self.width())
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.customContextMenuRequested.connect(self.SelectMenu)
        self.tableWidget.doubleClicked.connect(self.OpenBookInfo)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.Sort)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        pass

    def SetEnable(self, enable):
        self.inputButton.setEnabled(enable)
        self.loadInfoButton.setEnabled(enable)
        self.downButton.setEnabled(enable)
        self.nasButton.setEnabled(enable)
        self.cleanButton.setEnabled(enable)
    
    def OpenEdit(self):
        view = DownloadSomeEditView(QtOwner().owner)
        view.SaveLogin.connect(self.AddBookInfo)
        view.show()
    
    def UpdateTable(self, bookId):
        if bookId not in self.allBookInfo:
            return
        item = self.allBookInfo.get(bookId)
        rowCount = item.rowCount
        title = item.title
        epsLen = item.epsLen
        st = item.st
        
        self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(bookId)))
        self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(str(title)))
        if not epsLen:
            epsLen = ""
        self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(epsLen)))
        self.tableWidget.setItem(rowCount, 3, QTableWidgetItem(str(Str.GetStr(st))))
        pass
    
    def AddTable(self, bookId):
        if bookId not in self.allBookInfo:
            rowCont = self.tableWidget.rowCount()
            item = SomeItem()
            item.bookId = bookId
            item.rowCount = rowCont
            self.allBookInfo[bookId] = item
            self.tableWidget.insertRow(rowCont)
            self.UpdateTable(bookId)
        else:
            self.UpdateTable(bookId)
            
    def AddBookInfo(self, addBookList):
        for k in list(set(addBookList)):
            self.AddTable(k)
        return
    
    def Start(self):
        self.SetEnable(False)
        self.loadingBook = []
        self.completeBook = []
        self.completeNum = 0
        for v in self.allBookInfo.values():
            if v.epsLen <= 0:
                self.loadingBook.append(v.bookId)
                self.completeNum += 1
        self.StartGetBookInfo()
        self.StartGetBookInfo()
        self.StartGetBookInfo()
        return
    
    def Clean(self):
        for i in range(self.tableWidget.rowCount(), 0, -1):
            self.tableWidget.removeRow(i-1)
        self.allBookInfo.clear()
        self.loadingBook = []
        self.completeBook = []
        pass
    
    def StartGetBookInfo(self):
        if self.completeNum <= 0:
            self.SetEnable(True)
            return
        if not self.loadingBook:
            return

        bookId = self.loadingBook.pop(0)
        info = BookMgr().books.get(bookId)
        item = self.allBookInfo[bookId]
        if info and info.pageInfo.epsInfo:
            item.st = Str.Success
            item.title = info.baseInfo.title
            item.epsLen = len(info.pageInfo.epsInfo)
            self.completeNum -= 1
            self.UpdateTable(bookId)
            self.StartGetBookInfo()
            return
        self.AddHttpTask(req.GetBookInfoReq2(bookId), self.OpenBookBack, bookId)
        pass
    
    def OpenBookBack(self, raw, bookId):
        st = raw["st"]
        item = self.allBookInfo.get(bookId)
        self.completeNum -= 1
        if not item:
            self.StartGetBookInfo()
            return
        if st == Status.Ok:
            info = BookMgr().books.get(bookId)
            if not info:
                item.st = Str.NotFoundBook
                self.UpdateTable(bookId)
                self.StartGetBookInfo()
                return
            if not info.pageInfo.epsInfo:
                item.st = Str.SpaceEps
                self.UpdateTable(bookId)
                self.StartGetBookInfo()
                return
            item.st = Str.Ok
            item.title = info.baseInfo.title
            item.epsLen = len(info.pageInfo.epsInfo)
            
        else:
            item.st = st
        self.UpdateTable(bookId)
        self.StartGetBookInfo()
        return

    def SelectMenu(self, pos):
        pass
    
    def OpenBookInfo(self):
        selected = self.tableWidget.selectedIndexes()
        selectRows = set()
        for index in selected:
            selectRows.add(index.row())
        if len(selectRows) > 1:
            return
        if len(selectRows) <= 0:
            return
        row = list(selectRows)[0]
        col = 0
        bookId = self.tableWidget.item(row, col).text()
        bookName = self.tableWidget.item(row, 1).text()
        if not bookId:
            return
        QtOwner().OpenBookInfo(bookId, bookName)
    
    def Sort(self, col):
        order = self.order.get(col, 1)
        if order == 1:
            self.tableWidget.sortItems(col, Qt.AscendingOrder)
            self.order[col] = 0
        else:
            self.tableWidget.sortItems(col, Qt.DescendingOrder)
            self.order[col] = 1
        self.UpdateTableRow()
            
    def UpdateTableRow(self):
        count = self.tableWidget.rowCount()
        for i in range(count):
            bookId = self.tableWidget.item(i, 0).text()
            info = self.allBookInfo.get(bookId)
            if info:
                info.rowCount = i

    def Download(self):
        pass
    
    
    def AddNas(self):
        pass