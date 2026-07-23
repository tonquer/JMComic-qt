import base64
import pickle

from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QMessageBox

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from interface.ui_help import Ui_Help
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from task.task_thread import ThreadPrintDns
from tools.log import Log
from tools.str import Str
from view.help.help_log_widget import HelpLogWidget


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
        self.configButton.clicked.connect(self.InitUpdateConfig)
        #
        # self.updateUrl = [config.UpdateUrl, config.UpdateUrl2, config.UpdateUrl3]
        # self.updatePreUrl = [config.UpdateUrlApi, config.UpdateUrl2Api, config.UpdateUrl3Api]
        self.updateBackUrl = [config.UpdateUrlBack]
        self.checkUpdateIndex = 0
        self.helpLogWidget = HelpLogWidget()
        if Setting.IsShowCmd.value:
            self.helpLogWidget.show()
        else:
            self.helpLogWidget.hide()
        self.openCmd.clicked.connect(self.helpLogWidget.show)
        self.updateWidget.setVisible(False)
        self.selectUrl = ""
        self.updateButton.clicked.connect(self.OpenUpdateUrl)
        self.preCheckBox.setChecked(bool(Setting.IsPreUpdate.value))
        self.preCheckBox.clicked.connect(self.SwitchCheckPre)
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
        # self.dnsCheck = ThreadPrintDns()
        self.isCheckDns = False
        self.configUrlList = [config.AppUrl, config.AppUrl2, config.AppUrl3]
        self.configUrlIndex = 0
        self.updateUrlIndex = 0
        self.echConfigIndex = 0
        self.dohDomainList = []


    def retranslateUi(self, Help):
        Ui_Help.retranslateUi(self, Help)
        self.upTimeLabel.setText(config.VersionTime)
        if config.CanWaifu2x:
            self.waifu2x.setText(config.Waifu2xVersion)
        else:
            self.waifu2x.setText("")
        self.version.setText(config.RealVersion)
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))

    def Init(self):
        self.InitUpdateConfig()
        # self.UpdateDbInfo()

    def SwitchCheckPre(self):
        Setting.IsPreUpdate.SetValue(int(self.preCheckBox.isChecked()))

    def InitUpdateConfig(self):
        # self.configUrlIndex = 0
        self.UpdateText(self.configButton, Str.CheckUp, "#7fb80e", False)
        self.AddHttpTask(req.CheckUpdateConfigReq(self.configUrlList), self.InitUpdateConfigBack)

    def InitUpdateConfigBack(self, raw):
        try:
            st = raw.get("st")
            if st != Str.Ok:
                self.UpdateText(self.configButton, st, "#d71345", True)
                # self.configUrlIndex += 1
                # if self.configUrlIndex >= len(self.configUrlList):
                    # self.StartCheckDns()
                    # return
                # self.AddHttpTask(req.CheckUpdateConfigReq(self.configUrlList[self.configUrlIndex]), self.InitUpdateConfigBack)
                return
            # self.StartCheckDns()
            data = raw.get("data")
            self.UpdateText(self.configButton, Str.AlreadyUpdate, QtOwner().GetThemeColor(), True)
            if not data:
                return
            GlobalConfig.UpdateSetting(data)
            self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
        except Exception as es:
            Log.Error(es)

    # def StartCheckDns(self):
    #     if self.isCheckDns:
    #         return
        # self.dnsCheck.hostList.append(config.AppUrl)
        # self.dnsCheck.hostList.append(config.AppUrl2)
        # self.dnsCheck.hostList.append(config.AppUrl3)
        # self.dnsCheck.hostList.append(GlobalConfig.ProxyApiDomain2.value)
        # self.dnsCheck.hostList.extend(GlobalConfig.Url2List.value)
        # self.dnsCheck.hostList.extend(GlobalConfig.PicUrlList.value)
        # self.dnsCheck.start()
        # self.isCheckDns = True

    def InitUpdate(self):
        self.checkUpdateIndex = 0
        self.UpdateText(self.verCheck, Str.CheckUp, "#7fb80e", False)
        self.StartUpdate()

    def StartUpdate(self):
        self.updateWidget.setVisible(False)
        # if self.checkUpdateIndex > len(self.updateUrl) -1:
        #     self.UpdateText(self.verCheck, Str.AlreadyUpdate, QtOwner().GetThemeColor(), True)
        #     return
        # self.updateUrlIndex = 0
        self.AddHttpTask(req.CheckUpdateReq(self.configUrlList, Setting.IsPreUpdate.value), self.InitUpdateBack)

    def InitUpdateBack(self, raw):
        try:
            st = raw.get("st")
            if st != Str.Ok:
                self.UpdateText(self.verCheck, st, "#d71345", True)
                # self.updateUrlIndex += 1
                # if self.updateUrlIndex >= len(self.configUrlList):
                #     return
                # self.AddHttpTask(req.CheckUpdateReq(self.configUrlList[self.updateUrlIndex], Setting.IsPreUpdate.value),
                #                  self.InitUpdateBack)
                return
            data = raw.get("data")
            if not data:
                self.UpdateText(self.verCheck, Str.AlreadyUpdate, QtOwner().GetThemeColor(), True)
                return
            if data == "no":
                self.UpdateText(self.verCheck, Str.AlreadyUpdate, QtOwner().GetThemeColor(), True)
                return

            self.AddHttpTask(req.CheckUpdateInfoReq(self.configUrlList, data), self.InitUpdateInfoBack)
            self.UpdateText(self.verCheck, Str.HaveUpdate, "#d71345", True)
        except Exception as es:
            Log.Error(es)

    def InitUpdateInfoBack(self, raw):
        data = raw.get("data")
        self.SetNewUpdate(self.updateBackUrl[self.checkUpdateIndex],
                          Str.GetStr(Str.CurVersion) + config.UpdateVersion + ", " + Str.GetStr(
                              Str.CheckUpdateAndUp) + "\n\n" + data)

    def SwitchCurrent(self, **kwargs):
        self.configVer.setText("{}({})".format(GlobalConfig.Ver.value, GlobalConfig.VerTime.value))
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
        UrlList = [config.Issues1]
        url = UrlList[0] if self.checkUpdateIndex >= len(UrlList) else UrlList[self.checkUpdateIndex]
        QDesktopServices.openUrl(QUrl(url))

    def OpenProxyUrl(self):
        UrlList = [config.ProxyUrl1]
        url = UrlList[0] if self.checkUpdateIndex >= len(UrlList) else UrlList[self.checkUpdateIndex]
        QDesktopServices.openUrl(QUrl(url))

    def OpenLogDir(self):
        path = Setting.GetLogPath()
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        return

    def SetNewUpdate(self, updateUrl, updateLog):
        self.updateWidget.setVisible(True)
        self.selectUrl = updateUrl
        self.updateLabel.setText(updateLog)
        QtOwner().owner.navigationWidget.SetNewUpdate()
        return

    def OpenUpdateUrl(self):
        QDesktopServices.openUrl(QUrl(self.selectUrl))
        return