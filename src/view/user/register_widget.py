from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression, Signal, QUrl, QEvent
from PySide6.QtGui import QRegularExpressionValidator, QPixmap, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QRadioButton, QCommandLinkButton, QSpacerItem, QSizePolicy, QButtonGroup

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status, GlobalConfig, Setting
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
        self.regGroup = QButtonGroup(self)
        # self.link1.clicked.connect(self.OpenUrl)
        # self.link2.clicked.connect(self.OpenUrl)
        # self.link3.clicked.connect(self.OpenUrl)
        #
        # self.regGroup.setId(self.regButton1, 1)
        # self.regGroup.setId(self.regButton2, 2)
        # self.regGroup.setId(self.regButton3, 3)
        self.regGroup.buttonClicked.connect(self.SwitchButton)
        # reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        # validator = QRegularExpressionValidator(reg, self.userEdit)
        # self.userEdit.setValidator(validator)
        self.verPicture.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.verPicture:
                    self.LoadVer()
                # elif obj == self.user_name:
                #     QtOwner().owner.searchForm.SearchCreator(self.user_name.text())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def SwitchButton(self):
        Setting.RegisterProsyIndex.SetValue(self.regGroup.checkedId())
        GlobalConfig.SetSetting("Url", GlobalConfig.UrlList.value[self.regGroup.checkedId()-1])
        self.LoadVer()
        return

    def OpenUrl(self):
        sender = self.sender()
        QDesktopServices.openUrl(QUrl(sender.text()))

    def Init(self):
        self.InitButton()
        self.LoadVer()
        # self.LoadSetting()
        # for i, v in enumerate(GlobalConfig.UrlList.value):
        #     button = getattr(self, "link{}".format(i+1), None)
        #     if button:
        #         button.setText(v)
        return

    def DelLayouAllItem(self, layout):
        while layout.count() > 0:
            c = layout.takeAt(0)
            if not c:
                return
            layout2 = c.layout()
            if layout2:
                self.DelLayouAllItem(layout2)

            if c.widget():
                c.widget().setParent(None)
            del c

    def InitButton(self):
        for i in self.regGroup.buttons():
            self.regGroup.removeButton(i)

        self.DelLayouAllItem(self.linkLayout)

        index = Setting.RegisterProsyIndex.value -1  if Setting.RegisterProsyIndex.value <= len(GlobalConfig.UrlList.value) else 0
        for i, url in enumerate(GlobalConfig.UrlList.value):
            layout = QHBoxLayout()
            button = QRadioButton(self)
            if i == index:
                button.setChecked(True)
            self.regGroup.addButton(button)
            self.regGroup.setId(button, i+1)
            link = QCommandLinkButton(self)
            link.clicked.connect(self.OpenUrl)
            link.setText(url)
            horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(button)
            layout.addWidget(link)
            layout.addItem(horizontalSpacer)
            self.linkLayout.addLayout(layout)

        return

    # def LoadSetting(self):
    #     button = getattr(self, "link{}".format(Setting.RegisterProsyIndex.value))
    #     button.setChecked(True)

    def ClickButton(self):
        self.Register()

    def Register(self):
        email = self.userEdit.text()
        userName = self.nameEdit.text()
        passwd = self.passwdEdit.text()
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
        self.verPicture.clear()
        self.ShowLoading.emit()
        self.AddHttpTask(req.GetCaptchaReq(), self.LoadVerBack)

    def LoadVerBack(self, raw):
        self.CloseLoading.emit()
        st = raw["st"]
        msg = raw.get("msg")
        if st == Status.Ok:
            content = raw["content"]
            p = QPixmap()
            p.loadFromData(content)
            p.setDevicePixelRatio(self.devicePixelRatio())
            self.verPicture.setPixmap(p)
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
            self.verPicture.setText(Str.GetStr(Str.LoadingFail))

    def RegisterBack(self, raw):
        self.CloseLoading.emit()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg if msg else Str.GetStr(Str.RegisterSuc))
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
