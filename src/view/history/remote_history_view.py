from PySide6.QtWidgets import QWidget

from config import config
from interface.ui_history import Ui_History
from qt_owner import QtOwner
from server import req, Status, Log
from task.qt_task import QtTaskBase
from tools.str import Str


class RemoteHistoryView(QWidget, Ui_History, QtTaskBase):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_History.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.LoadCallBack = self.LoadNextPage

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        if refresh or self.bookList.count() <= 0:
            self.RefreshDataFocus()

    def RefreshDataFocus(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.bookList.clear()
        self.RefreshData()

    def RefreshData(self, page=1):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetHistoryReq2(page), self.SearchBack, page)

    def SearchBack(self, raw, v):
        page= v
        QtOwner().CloseLoading()
        self.bookList.UpdateState()
        try:
            st = raw["st"]
            if st == Status.Ok:
                bookList = raw["bookList"]
                total = raw["total"]
                if page == 1:
                    maxPage = (total - 1) // max(1, len(bookList)) + 1
                    self.bookList.UpdateMaxPage(maxPage)
                    self.spinBox.setMaximum(maxPage)
                self.bookList.UpdatePage(page, self.bookList.pages)
                self.nums.setText(self.bookList.GetPageStr())
                for book in bookList:
                    self.bookList.AddBookItemByBook(book)
            else:
                QtOwner().CheckShowMsg(raw)
        except Exception as es:
            Log.Error(es)

    def LoadNextPage(self):
        self.RefreshData(self.bookList.page + 1)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.clear()
        self.RefreshData(self.bookList.page)