from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class RegisterWidget(QtWidgets.QWidget, Ui_RegisterWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_RegisterWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        # validator = QRegularExpressionValidator(reg, self.userEdit)
        # self.userEdit.setValidator(validator)

    def Init(self):
        return

    def ClickButton(self):
        self.Register()

    def Register(self):
        email = self.userEdit.text()
        userName = self.nameEdit.text()
        passwd = self.passwd.text()
        sex = self.buttonGroup.checkedButton().objectName().replace("gender_", "")
        for v in [email, userName, passwd]:
            if not v:
                QtOwner().ShowError(Str.GetStr(Str.NotSpace))
                return

        QtOwner().ShowLoading()
        self.AddHttpTask(req.RegisterReq(userName, email, passwd, passwd, sex), self.RegisterBack)
        return

    def RegisterBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg if msg else Str.GetStr(Str.RegisterSuc))
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
