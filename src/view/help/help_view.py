import base64
import pickle

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QMessageBox

from config import config
from config.setting import Setting
from interface.ui_help import Ui_Help
from server import req
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str


class HelpView(QWidget, Ui_Help, QtTaskBase):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Help.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.dbUpdateUrl = [config.DatabaseUpdate2, config.DatabaseUpdate]
        # self.dbUpdateDbUrl = [config.DatabaseDownload2, config.DatabaseDownload]
        self.curIndex = 0
        self.curSubVersion = 0
        self.curUpdateTick = 0
        self.pushButton.clicked.connect(self.OpenUrl)
        self.version.setText(config.UpdateVersion)
        self.isCheckUp = False
        self.logButton.clicked.connect(self.OpenLogDir)

        self.verCheck.clicked.connect(self.InitUpdate)

        self.updateUrl = [config.UpdateUrl, config.UpdateUrl2]
        self.checkUpdateIndex = 0

    def retranslateUi(self, Help):
        Ui_Help.retranslateUi(self, Help)
        self.timeLabel.setText(config.VersionTime)
        self.version.setText(config.RealVersion)
        self.waifu2x.setText(config.Waifu2xVersion)

    def Init(self):
        pass
        # self.UpdateDbInfo()

    def InitUpdate(self):
        self.checkUpdateIndex = 0
        self.UpdateText(self.verCheck, Str.CheckUp, "#7fb80e", False)
        self.StartUpdate()

    def StartUpdate(self):
        if self.checkUpdateIndex > len(self.updateUrl) -1:
            self.UpdateText(self.verCheck, Str.AlreadyUpdate, "#ff4081", True)
            return
        self.AddHttpTask(req.CheckUpdateReq(self.updateUrl[self.checkUpdateIndex]), self.InitUpdateBack)

    def InitUpdateBack(self, raw):
        try:
            data = raw
            if not data:
                self.checkUpdateIndex += 1
                self.StartUpdate()

                return
            r = QMessageBox.information(self, Str.GetStr(Str.Update), Str.GetStr(Str.CurVersion) + config.UpdateVersion + ", "+ Str.GetStr(Str.CheckUpdateAndUp) + "\n" + data,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(self.updateUrl[self.checkUpdateIndex]))
            self.UpdateText(self.verCheck, Str.HaveUpdate, "#d71345", True)
        except Exception as es:
            Log.Error(es)

    def SwitchCurrent(self, **kwargs):
        return

    def UpdateText(self, label, text, color, enable):
        label.setStyleSheet("background-color:transparent;color:{}".format(color))
        label.setText("{}".format(Str.GetStr(text)))
        label.setEnabled(enable)
        if enable:
            label.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            label.setCursor(Qt.ArrowCursor)
        return

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.Issues))

    def OpenLogDir(self):
        path = Setting.GetLogPath()
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        return