from copy import deepcopy

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from config.setting import Setting
from interface.ui_login_proxy_widget import Ui_LoginProxyWidget
from qt_owner import QtOwner
from server import req, Log
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str


class LoginProxyWidget(QtWidgets.QWidget, Ui_LoginProxyWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginProxyWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.speedTest = []
        self.speedIndex = 0
        self.speedPingNum = 0

        self.pingBackNumCnt = {}
        self.pingBackNumDict = {}
        self.needBackNum = 0

        self.radioApiGroup.setId(self.radioButton_1, 1)
        self.radioApiGroup.setId(self.radioButton_2, 2)
        self.radioApiGroup.setId(self.radioButton_3, 3)
        self.radioApiGroup.setId(self.radioButton_4, 4)
        self.radioApiGroup.setId(self.radioButton_5, 5)

        self.radioImgGroup.setId(self.radio_img_1, 1)
        self.radioImgGroup.setId(self.radio_img_2, 2)
        self.radioImgGroup.setId(self.radio_img_3, 3)
        self.radioImgGroup.setId(self.radio_img_4, 4)
        self.radioImgGroup.setId(self.radio_img_5, 5)
        # self.buttonGroup.setId(self.radioButton_5, 5)

        self.radioProxyGroup.setId(self.proxy_0, 0)
        self.radioProxyGroup.setId(self.proxy_1, 1)
        self.radioProxyGroup.setId(self.proxy_2, 2)
        self.radioProxyGroup.setId(self.proxy_3, 3)
        self.LoadSetting()
        self.UpdateServer()
        self.commandLinkButton.clicked.connect(self.OpenUrl)
        self.maxNum = 6
        self.loginProxy.hide()

    def Init(self):
        self.LoadSetting()

    def ClickButton(self):
        self.SaveSetting()

    def SetEnabled(self, enabled):
        self.testSpeedButton.setEnabled(enabled)
        # self.dohBox.setEnabled(enabled)
        # self.dohEdit.setEnabled(enabled)
        self.proxy_0.setEnabled(enabled)
        self.proxy_1.setEnabled(enabled)
        self.proxy_2.setEnabled(enabled)
        self.proxy_3.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.sockEdit.setEnabled(enabled)
        self.cdn_img_ip.setEnabled(enabled)
        self.cdn_api_ip.setEnabled(enabled)
        self.radioButton_1.setEnabled(enabled)
        self.radioButton_2.setEnabled(enabled)
        self.radioButton_3.setEnabled(enabled)
        self.radioButton_4.setEnabled(enabled)
        self.radioButton_5.setEnabled(enabled)
        self.radio_img_1.setEnabled(enabled)
        self.radio_img_2.setEnabled(enabled)
        self.radio_img_3.setEnabled(enabled)
        self.radio_img_4.setEnabled(enabled)
        self.radio_img_5.setEnabled(enabled)
        # self.radioButton_5.setEnabled(enabled)

    def LoadSetting(self):
        # self.dohBox.setChecked(Setting.IsOpenDoh.value)
        # self.dohEdit.setText(Setting.DohAddress.value)
        self.httpLine.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)
        button = getattr(self, "radioButton_{}".format(Setting.ProxySelectIndex.value))
        button.setChecked(True)
        button = getattr(self, "proxy_{}".format(int(Setting.IsHttpProxy.value)))
        button.setChecked(True)
        button = getattr(self, "radio_img_{}".format(int(Setting.ProxyImgSelectIndex.value)))
        button.setChecked(True)
        self.cdn_api_ip.setText(Setting.PreferCDNIP.value)
        self.cdn_img_ip.setText(Setting.PreferCDNIPImg.value)
        self.loginProxy.setChecked(bool(Setting.IsLoginProxy.value))

    def SaveSetting(self):
        Setting.IsHttpProxy.SetValue(int(self.radioProxyGroup.checkedId()))
        Setting.Sock5Proxy.SetValue(self.sockEdit.text())
        Setting.HttpProxy.SetValue(self.httpLine.text())
        Setting.ProxySelectIndex.SetValue(self.radioApiGroup.checkedId())
        Setting.ProxyImgSelectIndex.SetValue(self.radioImgGroup.checkedId())
        Setting.IsLoginProxy.SetValue(int(self.loginProxy.isChecked()))
        Setting.PreferCDNIPImg.SetValue(self.cdn_img_ip.text())
        Setting.PreferCDNIP.SetValue(self.cdn_api_ip.text())
        # Setting.DohAddress.SetValue(self.dohEdit.text())
        # Setting.IsOpenDoh.SetValue(int(self.dohBox.isChecked()))
        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def UpdateServer(self):
        index = Setting.ProxySelectIndex.value-1
        index2 = Setting.ProxyImgSelectIndex.value-1
        if index < 0 or index >= len(config.Url2List):
            index = 0
        if index2 < 0 or index >= len(config.PicUrlList):
            index2 = 0
        config.Url2 = config.Url2List[index]
        config.PicUrl2 = config.PicUrlList[index2]
        if Setting.ProxyImgSelectIndex.value == 5:
            imageServer = Setting.PreferCDNIPImg.value
        else:
            imageServer = ""
        if Setting.ProxySelectIndex.value == 5:
            address = Setting.PreferCDNIP.value
        else:
            address = ""
        if Setting.IsLoginProxy.value:
            Server().UpdateDns(address, imageServer, "47.87.215.162")
        else:
            Server().UpdateDns(address, imageServer)
        QtOwner().settingView.SetSock5Proxy()
        Log.Info("update proxy, setId:{}:{}, address:{}, img:{}".format(Setting.ProxySelectIndex.value, Setting.ProxyImgSelectIndex.value, address, imageServer))

    def SpeedTest(self):
        self.speedIndex = 0
        self.speedPingNum = 0
        self.speedTest = []

        for i in range(1, self.maxNum):
            label = getattr(self, "label_api_" + str(i))
            label.setText("")
            label = getattr(self, "label_img_" + str(i))
            label.setText("")

        i = 1
        for index, address in enumerate(config.Url2List):
            imageUrl = config.PicUrlList[index]
            self.speedTest.append((address, imageUrl, False, False, ("", ""), i))
            i += 1

        PreferCDNIP = self.cdn_api_ip.text()
        imgCDNIP = self.cdn_img_ip.text()
        if PreferCDNIP or imgCDNIP:
            self.speedTest.append((config.Url2List[0], config.PicUrlList[0], False, False, (PreferCDNIP, imgCDNIP), i))
            i += 1
        else:
            i += 1

        self.SetEnabled(False)
        self.needBackNum = 0
        self.speedPingNum = 0
        self.StartSpeedPing()

    def StartSpeedPing(self):
        if len(self.speedTest) <= self.speedPingNum:
            self.StartSpeedTest()
            return
        address, imageProxy, isHttpProxy, isProxyUrl, dnslist, i = self.speedTest[self.speedPingNum]
        httpProxy = self.httpLine.text()
        if ((self.radioProxyGroup.checkedId() == 1 and not self.httpLine.text()) or
                            (self.radioProxyGroup.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label_api_"+str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedPingNum += 1
            self.StartSpeedPing()
            return

        request = req.SpeedTestPingReq()
        if self.radioProxyGroup.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        elif self.radioProxyGroup.checkedId() == 3:
            request.proxy = ""
        else:
            request.proxy = {"http": None, "https": None}

        if isProxyUrl:
            if "user-agent" in request.headers:
                request.headers.pop("user-agent")
            request.proxyUrl = config.ProxyApiDomain
        else:
            request.proxyUrl = ""

        if self.radioProxyGroup.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)

        request.timeout = 2
        Server().UpdateDns(dnslist[0], dnslist[1])
        request.url = request.url.replace(config.Url2, address)
        self.pingBackNumCnt[i] = 0
        self.pingBackNumDict[i] = [0, 0, 0]
        request1 = deepcopy(request)
        request2 = deepcopy(request)
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request, x), self.SpeedTestPingBack, (i, 0))
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request1, x), self.SpeedTestPingBack, (i, 1))
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request2, x), self.SpeedTestPingBack, (i, 2))
        self.needBackNum += 1
        return

    def SpeedTestPingBack(self, raw, v):
        i, backNum = v
        data = raw["data"]
        st = raw["st"]
        label = getattr(self, "label_api_" + str(i))
        if float(data) > 0.0:
            self.pingBackNumDict[i][backNum] = int(float(data))
            label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data))) + "ms"))
        else:
            self.pingBackNumDict[i][backNum] = str(st)
            label.setText("<font color=#d71345>{}</font>".format(Str.GetStr(st)))
        self.pingBackNumCnt[i] += 1

        if self.pingBackNumCnt[i] >= 3:
            sumData = 0
            sumCnt = 0
            sumSt = 0
            for data in self.pingBackNumDict[i]:
                if isinstance(data, int):
                    sumData += data
                    sumCnt += 1
                else:
                    sumSt = data
            if sumCnt >= 1:
                label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(sumData / sumCnt))) + "ms"))
            else:
                label.setText("<font color=#d71345>{}</font>".format(Str.GetStr(int(sumSt))))

            self.speedPingNum += 1
            self.StartSpeedPing()
            return

    def StartSpeedTest(self):
        if len(self.speedTest) <= self.speedIndex:
            self.UpdateServer()
            self.SetEnabled(True)
            return

        address, imgUrl, isHttpProxy, isProxyUrl, dnslist, i = self.speedTest[self.speedIndex]
        httpProxy = self.httpLine.text()
        if ((self.radioProxyGroup.checkedId() == 1 and not self.httpLine.text()) or
                            (self.radioProxyGroup.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label_img_" + str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedIndex += 1
            self.StartSpeedTest()
            return

        request = req.SpeedTestReq()
        request.isUseHttps = self.httpsBox.isChecked()
        if self.radioProxyGroup.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        elif self.radioProxyGroup.checkedId() == 3:
            request.proxy = ""
        else:
            request.proxy = {"http": None, "https": None}

        if isProxyUrl:
            if "user-agent" in request.headers:
                request.headers.pop("user-agent")
            request.proxyUrl = config.ProxyImgDomain
        else:
            request.proxyUrl = ""

        if self.radioProxyGroup.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)
        Server().UpdateDns(dnslist[0], dnslist[1])
        request.url = request.url.replace(config.PicUrl2, imgUrl)
        self.AddHttpTask(lambda x: Server().TestSpeed(request, x), self.SpeedTestBack, i)
        return

    def SpeedTestBack(self, raw, i):
        data = raw["data"]
        st = raw["st"]
        if not data:
            data = "<font color=#d71345>{}</font>".format(Str.GetStr(st))
        else:
            data = "<font color=#7fb80e>{}</font>".format(data)
        label = getattr(self, "label_img_" + str(i))
        label.setText(data)
        self.speedIndex += 1
        self.StartSpeedTest()
        return

    def OpenUrl(self):
        QtOwner().owner.helpView.OpenProxyUrl()

    def SetSock5Proxy(self, isProxy):
        import socket
        import socks
        if not QtOwner().backSock:
            QtOwner().backSock = socket.socket
        if isProxy:
            data = self.sockEdit.text().replace("http://", "").replace("https://", "").replace("sock5://", "")
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                socks.set_default_proxy(socks.SOCKS5, host, int(port))
                socket.socket = socks.socksocket
        else:
            socks.set_default_proxy()
            socket.socket = QtOwner().backSock