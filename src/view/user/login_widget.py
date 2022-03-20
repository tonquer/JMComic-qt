import base64
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Signal

from config.setting import Setting, SettingValue
from interface.ui_login_widget import Ui_LoginWidget
from qt_owner import QtOwner
from server import req, Status, config
from task.qt_task import QtTaskBase
from tools.str import Str
from tools.user import User


class LoginWidget(QtWidgets.QWidget, Ui_LoginWidget, QtTaskBase):
    ShowLoading = Signal()
    CloseLoading = Signal()

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.autoBox.setChecked(bool(Setting.AutoLogin.value))
        self.saveBox.setChecked(bool(Setting.SavePassword.value))
        self.autoBox.clicked.connect(partial(self.CheckButtonEvent, Setting.AutoLogin, self.autoBox))
        self.saveBox.clicked.connect(partial(self.CheckButtonEvent, Setting.SavePassword, self.saveBox))
        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        return

    def Init(self):
        # self.userEdit_2.setText()
        # request = req.InitReq()
        # request.proxy = {}
        # self.AddHttpTask(request, self.InitBack)
        return

    def ClickButton(self):
        self.Login()

    def Login(self):
        self.ShowLoading.emit()
        userId = self.userEdit_2.text()
        passwd = self.passwdEdit_2.text()
        self.AddHttpTask(req.LoginReq2(userId, passwd), self.LoginBack)

    # def LoginPreBack(self, raw):
    #     userId = self.userEdit_2.text()
    #     passwd = self.passwdEdit_2.text()
    #     self.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

        # self.close()
        # self.owner().show()

    def LoginBack(self, raw):
        self.CloseLoading.emit()
        st = raw["st"]
        if st == Status.Ok:
            user = raw.get("user")
            Setting.UserId.SetValue(self.userEdit_2.text())
            if Setting.SavePassword.value:
                Setting.Password.SetValue(base64.b64encode(self.passwdEdit_2.text().encode("utf-8")))
            else:
                Setting.Password.SetValue("")
            QtOwner().SetUser(user)
            QtOwner().SetLogin()
            self.parent().parent().parent().parent().close()
        QtOwner().CheckShowMsg(raw)

