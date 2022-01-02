from PySide6 import QtWidgets

from interface.ui_user_manager_widget import Ui_UserManagerWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class UserManagerWidget(QtWidgets.QWidget, Ui_UserManagerWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_UserManagerWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.verfyButton.clicked.connect(self.RegisterVerifyEmail)
        self.resetButton.clicked.connect(self.ResetPassword)
        self.sendButton.clicked.connect(self.VerifyEmail)

    def Init(self):
        return

    def RegisterVerifyEmail(self):
        email = self.verfyEdit.text()
        if not email:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.RegisterVerifyMailReq(email), self._Back)

    def ResetPassword(self):
        email = self.resetEdit.text()
        if not email:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.ResetPasswordReq(email), self._Back)

    def VerifyEmail(self):
        link = self.sendEdit.text()
        if not link:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.VerifyMailReq(link), self._Back)

    def _Back(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg)
        else:
            # QtWidgets.QMessageBox.information(self, '注册失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().ShowError(msg if msg else Str.GetStr(st))