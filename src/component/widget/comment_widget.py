import json

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from interface.ui_comment import Ui_Comment
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str
from tools.user import User


class CommentWidget(QtWidgets.QWidget, Ui_Comment, QtTaskBase):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Comment.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)
        self.listWidget.LoadCallBack = self.LoadNextPage

        self.bookId = ""
        self.pushButton.clicked.connect(self.SendComment)
        self.skipButton.clicked.connect(self.JumpPage)
        self.cid = ""

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId", "")
        refresh = kwargs.get("refresh")
        if not bookId and refresh:
            self.pushButton.hide()
            self.commentLine.hide()
            self.bookId = ""
            self.ClearCommentList()
            self.listWidget.UpdatePage(1, 1)
            self.LoadComment()
            return

        if not bookId:
            return
        self.pushButton.setVisible(True)
        self.commentLine.setVisible(True)
        self.bookId = bookId
        self.ClearCommentList()
        self.listWidget.UpdatePage(1, 1)
        self.LoadComment()
        pass

    def ClearCommentList(self):
        self.listWidget.SetWheelStatus(True)
        self.listWidget.clear()
        self.listWidget.UpdatePage(1, 1)
        self.listWidget.UpdateState()
        self.spinBox.setValue(1)
        self.nums.setText(self.listWidget.GetPageText())
        self.ClearTask()

    def JumpPage(self):
        try:
            page = int(self.spinBox.text())
            if page > self.listWidget.pages:
                return
            self.listWidget.SetWheelStatus(True)
            self.listWidget.page = page
            self.listWidget.clear()
            self.LoadComment()
        except Exception as es:
            Log.Error(es)

    def LoadComment(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetCommentReq2(self.bookId, self.listWidget.page), self.GetCommentBack, self.listWidget.page)
        return

    def LoadNextPage(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetCommentReq2(self.bookId, self.listWidget.page + 1), self.GetCommentBack, self.listWidget.page+1)
        return

    # 加载评论
    def GetCommentBack(self, raw, page):
        QtOwner().CloseLoading()
        st = raw["st"]
        try:
            self.listWidget.UpdateState()
            if st == Status.Ok:

                comments = raw["commentList"]
                if page == 1:
                    total = raw["total"]
                    num = len(comments)
                    maxPages = (total - 1) // max(1, num) + 1
                    self.listWidget.UpdateMaxPage(maxPages)
                    self.spinBox.setMaximum(maxPages)
                self.spinBox.setValue(page)
                self.listWidget.UpdatePage(page)
                self.nums.setText(self.listWidget.GetPageText())

                for index, info in enumerate(comments):
                    self.listWidget.AddUserItem(info, "")
            else:
                QtOwner().ShowError(Str.GetStr(st))
            return
        except Exception as es:
            QtOwner().CheckShowMsg(raw)
            Log.Error(es)

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        self.commentLine.setText("")
        QtOwner().ShowLoading()
        self.AddHttpTask(req.SendCommentReq2(self.bookId, data, self.cid), callBack=self.SendCommentBack)

    def SendCommentBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            if st == Status.Ok:
                self.ClearCommentList()
                self.commentLine.setText("")
                self.listWidget.UpdatePage(1, 1)
                self.LoadComment()
                QtOwner().CheckShowMsg(raw)
            else:
                QtOwner().CheckShowMsg(raw)

        except Exception as es:
            QtOwner().CloseLoading()
            Log.Error(es)
