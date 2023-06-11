from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator, QPixmap

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.str import Str


class RegisterWidget(QtWidgets.QWidget, Ui_RegisterWidget, QtTaskBase):
    ShowLoading = Signal()
    CloseLoading = Signal()

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_RegisterWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.verPicture.setText(Str.GetStr(Str.LoadingPicture))
        # reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        # validator = QRegularExpressionValidator(reg, self.userEdit)
        # self.userEdit.setValidator(validator)

    def Init(self):
        self.LoadVer()
        return

    def ClickButton(self):
        self.Register()

    def Register(self):
        email = self.userEdit.text()
        userName = self.nameEdit.text()
        passwd = self.passwd.text()
        ver = self.verEdit.text()
        sex = self.buttonGroup.checkedButton().objectName().replace("gender_", "")
        for v in [email, userName, passwd, ver]:
            if not v:
                QtOwner().ShowError(Str.GetStr(Str.NotSpace))
                return

        self.ShowLoading.emit()
        self.AddHttpTask(req.RegisterReq(userName, email, passwd, passwd, sex, ver), self.RegisterBack)
        return

    def LoadVer(self):
        self.verPicture.setPixmap(QPixmap())
        self.ShowLoading.emit()
        self.AddHttpTask(req.GetCaptchaReq(), self.LoadVerBack)

    def LoadVerBack(self, raw):
        self.CloseLoading.emit()
        st = raw["st"]
        if st == Status.Ok:
            content = raw["content"]
            p = QPixmap()
            p.loadFromData(content)
            p.setDevicePixelRatio(self.devicePixelRatio())
            self.verPicture.setPixmap(p)
        else:
            self.verPicture.setText(Str.GetStr(Str.LoadingFail))

    def RegisterBack(self, raw):
        self.CloseLoading.emit()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg if msg else Str.GetStr(Str.RegisterSuc))
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
