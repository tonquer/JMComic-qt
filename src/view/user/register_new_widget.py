from functools import partial
import ipaddress

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRegularExpression, Signal, QUrl, QEvent
from PySide6.QtGui import QRegularExpressionValidator, QPixmap, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QRadioButton, QCommandLinkButton, QSpacerItem, QSizePolicy, QButtonGroup

from component.label.msg_label import MsgLabel
from interface.ui_register_widget import Ui_RegisterWidget
from qt_owner import QtOwner
from server import req, Status, GlobalConfig, Setting
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil


class RegisterNewWidget:
    def __init__(self, owner):
        self.owner = owner
        self.owner.verPicture.setText(Str.GetStr(Str.LoadingPicture))
        self.regGroup = QButtonGroup(self.owner)
        # self.link1.clicked.connect(self.OpenUrl)
        # self.link2.clicked.connect(self.OpenUrl)
        # self.link3.clicked.connect(self.OpenUrl)
        #
        # self.regGroup.setId(self.regButton1, 1)
        # self.regGroup.setId(self.regButton2, 2)
        # self.regGroup.setId(self.regButton3, 3)
        self.regGroup.buttonClicked.connect(self.SwitchButton)
        self.owner.registerButton.clicked.connect(self.ClickButton)
        # reg = QRegularExpression("^[A-Z0-9a-z\\.\\_]{1,16}$")
        # validator = QRegularExpressionValidator(reg, self.userEdit)
        # self.userEdit.setValidator(validator)
        self.owner.verPicture.installEventFilter(self.owner)
        self.isInit = False
        self.jump301Url = ""
        self.jumpRadionId = 0
        self.jumpLinkButton = None
        self.linkButtons = {}
        self.dohQueryGen = 0
        self.pendingDohHosts = set()
        self.lastDohQueryUrl = ""
        self.pendingLoadVer = False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.owner.verPicture:
                    self.LoadVer()
                # elif obj == self.user_name:
                #     QtOwner().owner.searchForm.SearchCreator(self.user_name.text())
                return True
            else:
                return False
        else:
            return QtWidgets.QWidget.eventFilter(self.owner, obj, event)

    def SwitchButton(self):
        Setting.RegisterProsyIndex.SetValue(self.regGroup.checkedId())
        if Setting.RegisterProsyIndex.value > len(GlobalConfig.UrlList.value):
            GlobalConfig.SetSetting("Url", self.jump301Url)
        else:
            GlobalConfig.SetSetting("Url", GlobalConfig.UrlList.value[self.regGroup.checkedId()-1])
        # self.AddHttpTask(req.LoginCheck301Req(), callBack=self.LoginCheckBack)
        if self._NeedWaitDohForCurrentUrl():
            self.InitDohDns(force=False)
            if self._NeedWaitDohForCurrentUrl() and ToolUtil.GetUrlHost(GlobalConfig.Url.value) in self.pendingDohHosts:
                self._WaitDohThenLoadVer()
                return
        self.LoadVer()
        return

    # def LoginCheckBack(self, raw):
    #     self.AddHttpTask(req.LoginPreReq(), callBack=self.LoginPreBack)
    #
    # def LoginPreBack(self, raw):
    #     self.LoadVer()

    def OpenUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

    @staticmethod
    def _IsUseIpRoute():
        return GlobalConfig.IsCdnIndex(Setting.ProxySelectIndex.value)

    @staticmethod
    def _GetDohUrlList():
        dohList = []
        firstDoh = str(Setting.DohAddress.value).strip() if Setting.DohAddress.value else ""
        if firstDoh:
            dohList.append(firstDoh)
        for addr in GlobalConfig.DohUrlList.value:
            addr = str(addr).strip()
            if addr and addr not in dohList:
                dohList.append(addr)
        return dohList

    def _GetRegisterDomains(self, extraUrls=None):
        rawUrls = list(GlobalConfig.UrlList.value)
        if GlobalConfig.Url.value:
            rawUrls.append(GlobalConfig.Url.value)
        if self.jump301Url:
            rawUrls.append(self.jump301Url)
        if extraUrls:
            rawUrls.extend(extraUrls)
        domains = []
        for rawUrl in rawUrls:
            if not rawUrl:
                continue
            host = ToolUtil.GetUrlHost(str(rawUrl).strip())
            if not host or host in domains:
                continue
            try:
                ipaddress.ip_address(host)
                continue
            except ValueError:
                pass
            domains.append(host)
        return domains

    def _NeedWaitDohForCurrentUrl(self):
        if not Setting.EnableDoh.value or self._IsUseIpRoute():
            return False
        curHost = ToolUtil.GetUrlHost(GlobalConfig.Url.value)
        if not curHost:
            return False
        try:
            ipaddress.ip_address(curHost)
            return False
        except ValueError:
            pass
        return not QtOwner().dohIpDict.get(curHost)

    def _WaitDohThenLoadVer(self):
        if not self.pendingLoadVer:
            self.pendingLoadVer = True
            QtOwner().ShowLoading()

    def _CancelPendingLoadVer(self):
        if self.pendingLoadVer:
            self.pendingLoadVer = False
            QtOwner().CloseLoading()

    def InitDohDns(self, force=False, extraUrls=None):
        if not Setting.EnableDoh.value:
            self.dohQueryGen += 1
            self.pendingDohHosts.clear()
            self._CancelPendingLoadVer()
            self.UpdateLinkDohText()
            return False
        dohList = self._GetDohUrlList()
        if not dohList:
            return False
        curDoh = dohList[0]
        if self.lastDohQueryUrl and curDoh != self.lastDohQueryUrl:
            force = True
        self.lastDohQueryUrl = curDoh

        domains = self._GetRegisterDomains(extraUrls=extraUrls)
        if force:
            self.dohQueryGen += 1
            self.pendingDohHosts.clear()
            targetDomains = domains
        else:
            targetDomains = [
                h for h in domains
                if not QtOwner().dohIpDict.get(h) and h not in self.pendingDohHosts
            ]
        if not targetDomains:
            self.UpdateLinkDohText()
            return False

        gen = self.dohQueryGen
        Log.Info(f"start register doh dns query, gen:{gen}, doh:{curDoh}, count:{len(targetDomains)}")
        for host in targetDomains:
            self.pendingDohHosts.add(host)
            request = req.DnsOverHttpsReq(host, dohList)
            self.owner.AddHttpTask(request, self.InitDohDnsBack, backParam=(gen, host))
        return True

    def InitDohDnsBack(self, raw, backParam):
        gen, host = backParam
        if gen != self.dohQueryGen or not Setting.EnableDoh.value:
            return
        self.pendingDohHosts.discard(host)
        st = raw.get("st")
        maxSelectIp = getattr(getattr(self.owner, "proxyWidget", None), "maxSelectIp", 2)
        if st == Str.Ok:
            ips = req.DnsOverHttpsReq.ParseAnswerIps(raw.get("Answer"))
            if ips:
                QtOwner().dohIpDict[host] = ips[:maxSelectIp]
                self.UpdateLinkDohText()
                Log.Info(f"update register doh ip, host:{host}, ips:{ips}")
            else:
                Log.Warn(f"register doh dns empty, host:{host}")
        else:
            Log.Warn(f"register doh dns query fail, host:{host}, st:{st}")

        if self.pendingLoadVer:
            curHost = ToolUtil.GetUrlHost(GlobalConfig.Url.value)
            if host == curHost or curHost not in self.pendingDohHosts:
                self._CancelPendingLoadVer()
                self.LoadVer()

    def UpdateLinkDohText(self):
        isIpRoute = self._IsUseIpRoute()
        enableDoh = bool(Setting.EnableDoh.value)
        proxyIps = req.ServerReq.GetProxyIpList() if isIpRoute else []
        dohIpDict = QtOwner().dohIpDict
        for url, link in list(self.linkButtons.items()):
            if not link:
                continue
            host = ToolUtil.GetUrlHost(url)
            if isIpRoute and proxyIps:
                link.setToolTip(f"{host}: {', '.join(proxyIps)}")
            elif enableDoh and host and dohIpDict.get(host):
                link.setToolTip(f"{host}: {', '.join(dohIpDict[host])}")
            else:
                link.setToolTip("")

    def Init(self):
        if not self.isInit:
            self.isInit = True
            self.InitButton()
            if Setting.EnableDoh.value:
                self.InitDohDns(force=False)
                if self._NeedWaitDohForCurrentUrl() and ToolUtil.GetUrlHost(GlobalConfig.Url.value) in self.pendingDohHosts:
                    self._WaitDohThenLoadVer()
                    return
            self.LoadVer()
        else:
            if Setting.EnableDoh.value:
                self.InitDohDns(force=False)
            self.UpdateLinkDohText()
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

        self.DelLayouAllItem(self.owner.linkLayout)
        self.linkButtons = {}

        index = Setting.RegisterProsyIndex.value -1  if Setting.RegisterProsyIndex.value <= len(GlobalConfig.UrlList.value) else 0
        for i, url in enumerate(GlobalConfig.UrlList.value):
            layout = QHBoxLayout()
            button = QRadioButton(self.owner)
            if i == index:
                GlobalConfig.SetSetting("Url", url)
                button.setChecked(True)
            self.regGroup.addButton(button)
            self.regGroup.setId(button, i+1)
            link = QCommandLinkButton(self.owner)
            link.clicked.connect(partial(self.OpenUrl, url))
            link.setText(url)
            self.linkButtons[url] = link
            horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(button)
            layout.addWidget(link)
            layout.addItem(horizontalSpacer)
            self.owner.linkLayout.addLayout(layout)

        self.UpdateLinkDohText()
        return

    # def LoadSetting(self):
    #     button = getattr(self, "link{}".format(Setting.RegisterProsyIndex.value))
    #     button.setChecked(True)

    def ClickButton(self):
        self.Register()

    def Register(self):
        email = self.owner.userEdit.text()
        userName = self.owner.nameEdit.text()
        passwd = self.owner.passwdEdit.text()
        ver = self.owner.verEdit.text()
        sex = self.owner.sexGroup.checkedButton().objectName().replace("gender_", "")
        for v in [email, userName, passwd, ver]:
            if not v:
                QtOwner().ShowError(Str.GetStr(Str.NotSpace))
                return

        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.RegisterReq(userName, email, passwd, passwd, sex, ver), self.RegisterBack)
        return

    def LoadVer(self):
        self._CancelPendingLoadVer()
        self.owner.verPicture.setPixmap(QPixmap())
        self.owner.verPicture.clear()
        QtOwner().ShowLoading()
        self.owner.AddHttpTask(req.GetCaptchaReq(), self.LoadVerBack)

    def LoadVerBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        msg = raw.get("msg")
        destUrl = raw.get("desUrl")
        if destUrl:
            self.AddUrl(destUrl)

        if st == Status.Ok:
            content = raw["content"]
            p = QPixmap()
            p.loadFromData(content)
            p.setDevicePixelRatio(self.owner.devicePixelRatio())
            self.owner.verPicture.setPixmap(p)
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
            self.owner.verPicture.setText(Str.GetStr(Str.LoadingFail))

    def RegisterBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        msg = raw["msg"]
        if st == Status.Ok:
            QtOwner().ShowError(msg if msg else Str.GetStr(Str.RegisterSuc))
        else:
            QtOwner().ShowError(msg if msg else Str.GetStr(st))
            destUrl = raw.get("desUrl")
            if destUrl:
                self.AddUrl(destUrl)

    def AddUrl(self, url):
        newUrl = "https://" + ToolUtil.GetUrlHost(url)
        if newUrl in GlobalConfig.UrlList.value:
            return
        self.jump301Url = newUrl
        if self.jumpRadionId > 0:
            if self.jumpLinkButton:
                for k, v in list(self.linkButtons.items()):
                    if v is self.jumpLinkButton:
                        self.linkButtons.pop(k, None)
                self.jumpLinkButton.setText(newUrl)
                self.linkButtons[newUrl] = self.jumpLinkButton
            if self.regGroup.checkedId() == self.jumpRadionId:
                GlobalConfig.SetSetting("Url", newUrl)
            if Setting.EnableDoh.value:
                self.InitDohDns(force=False, extraUrls=[newUrl])
            self.UpdateLinkDohText()
            return
        layout = QHBoxLayout()
        button = QRadioButton(self.owner)
        i = len(self.regGroup.buttons())
        self.regGroup.addButton(button)
        self.regGroup.setId(button, i + 1)
        self.jumpRadionId = i + 1
        link = QCommandLinkButton(self.owner)
        link.clicked.connect(partial(self.OpenUrl, newUrl))
        link.setText(newUrl)
        self.jumpLinkButton = link
        self.linkButtons[newUrl] = link
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(button)
        layout.addWidget(link)
        layout.addItem(horizontalSpacer)
        self.owner.linkLayout.addLayout(layout)
        if Setting.EnableDoh.value:
            self.InitDohDns(force=False, extraUrls=[newUrl])
        self.UpdateLinkDohText()
