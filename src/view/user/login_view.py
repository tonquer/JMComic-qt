import base64

from PySide6.QtCore import Signal, Qt, QTimer

from component.dialog.base_mask_dialog import BaseMaskDialog
from component.label.gif_label import GifLabel
from config.setting import Setting
from interface.ui_login import Ui_Login
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str


class LoginView(BaseMaskDialog, Ui_Login, QtTaskBase):
    CloseLogin = Signal()

    def __init__(self, parent=None, isAutoLogin=0):
        BaseMaskDialog.__init__(self, parent)
        Ui_Login.__init__(self)
        QtTaskBase.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.loadingDialog = GifLabel(self)
        self.loadingDialog.Init(QtOwner().GetFileData(":/png/icon/loading_gif.gif"), 256)
        self.loadingDialog.setAlignment(Qt.AlignCenter)
        self.loadingDialog.close()

        self.tabWidget.currentChanged.connect(self._SwitchWidget)
        self.loginButton.clicked.connect(self._ClickButton)
        self.closeButton.clicked.connect(self.close)
        userId = Setting.UserId.value
        if userId and isinstance(userId, str):
            self.loginWidget.userEdit_2.setText(userId)

        passwd = Setting.Password.value
        passwd = base64.b64decode(passwd).decode("utf-8") if passwd else ""
        if passwd and isinstance(passwd, str):
            self.loginWidget.passwdEdit_2.setText(passwd)

        self.tabWidget.setCurrentIndex(0)
        self.loginWidget.ShowLoading.connect(self.ShowLoading)
        self.registerWidget.ShowLoading.connect(self.ShowLoading)
        self.userWidget.ShowLoading.connect(self.ShowLoading)

        self.loginWidget.CloseLoading.connect(self.CloseLoading)
        self.registerWidget.CloseLoading.connect(self.CloseLoading)
        self.userWidget.CloseLoading.connect(self.CloseLoading)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._AutoLogin)
        if isAutoLogin:
            self.timer.start()

    def ShowLoading(self):
        self.loadingDialog.Show()

    def CloseLoading(self):
        self.loadingDialog.close()

    @property
    def loginWidget(self):
        return self.tabWidget.widget(0)

    @property
    def registerWidget(self):
        return self.tabWidget.widget(1)

    @property
    def userWidget(self):
        return self.tabWidget.widget(2)

    @property
    def proxyWidget(self):
        return self.tabWidget.widget(3)

    def _AutoLogin(self):
        self.timer.stop()
        self.loginWidget.ClickButton()
        return

    def _SwitchWidget(self, index):
        # self.tabWidget.widget(index).adjustSize()
        # print(self.tabWidget.widget(index).size())
        # self.tabWidget.resize(self.tabWidget.widget(index).size())
        if self.tabWidget.widget(index) == self.loginWidget:
            self.loginButton.setVisible(True)
            self.loginButton.setText(Str.GetStr(Str.Login))
        elif self.tabWidget.widget(index) == self.registerWidget:
            self.loginButton.setVisible(True)
            self.loginButton.setText(Str.GetStr(Str.Register))
        elif self.tabWidget.widget(index) == self.userWidget:
            self.loginButton.setVisible(False)
        elif self.tabWidget.widget(index) == self.proxyWidget:
            self.loginButton.setVisible(True)
            self.loginButton.setText(Str.GetStr(Str.Save))
        self.tabWidget.widget(index).Init()

    def _ClickButton(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.widget(index).ClickButton()

    # def event(self, event) -> bool:
    #     return BaseMaskDialog.event(event)