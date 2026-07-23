from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QDesktopServices

from interface.ui_user_manager_widget import Ui_UserManagerWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class UserManagerNewWidget:


    def __init__(self, owner):
        self.owner = owner
        self.owner.verfyButton.clicked.connect(self.RegisterVerifyEmail)
        self.owner.resetButton.clicked.connect(self.ResetPassword)
        self.owner.sendButton.clicked.connect(self.VerifyEmail)
        self.owner.commandLinkButton.clicked.connect(self.OpenUrl)
        self.owner.commandLinkButton2.clicked.connect(self.OpenUrl2)

    def Init(self):
        return

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl("https://discord.com/invite/V74p7HM"))

    def OpenUrl2(self):
        QDesktopServices.openUrl(QUrl("https://t.me/hcomic18"))

    def RegisterVerifyEmail(self):
        email = self.owner.verfyEdit.text()
        password = self.owner.verfyPsEdit.text()
        if not email or not password:
            return
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.RegisterVerifyMailReq(email, password), self._Back)

    def ResetPassword(self):
        email = self.owner.resetEdit.text()
        if not email:
            return
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.ResetPasswordReq(email), self._Back)

    def VerifyEmail(self):
        link = self.owner.sendEdit.text()
        if not link:
            return
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.VerifyMailReq(link), self._Back)

    def _Back(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg)
        else:
            # QtWidgets.QMessageBox.information(self, '注册失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(msg if msg else Str.GetStr(st))