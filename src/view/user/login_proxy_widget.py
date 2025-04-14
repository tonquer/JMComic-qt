import urllib
from copy import deepcopy
import random

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from interface.ui_login_proxy_widget import Ui_LoginProxyWidget
from qt_owner import QtOwner
from server import req, Log, ToolUtil
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str
from view.user.ua import UALIST


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
        self.radioApiGroup.setId(self.radioButton_6, 6)

        self.radioImgGroup.setId(self.radio_img_1, 1)
        self.radioImgGroup.setId(self.radio_img_2, 2)
        self.radioImgGroup.setId(self.radio_img_3, 3)
        self.radioImgGroup.setId(self.radio_img_4, 4)
        self.radioImgGroup.setId(self.radio_img_5, 5)
        self.radioImgGroup.setId(self.radio_img_6, 6)
        # self.buttonGroup.setId(self.radioButton_5, 5)

        self.radioProxyGroup.setId(self.proxy_0, 0)
        self.radioProxyGroup.setId(self.proxy_1, 1)
        self.radioProxyGroup.setId(self.proxy_2, 2)
        self.radioProxyGroup.setId(self.proxy_3, 3)
        self.LoadSetting()
        self.UpdateServer()
        self.commandLinkButton.clicked.connect(self.OpenUrl)
        self.maxNum = 7
        self.loginProxy.hide()
        self.uaRandom.clicked.connect(self.RandomUa)
        self.lastResult = {}
        self.LoadHistory()

    def Init(self):
        self.LoadSetting()
        proxy = urllib.request.getproxies()
        if isinstance(proxy, dict) and proxy.get("http"):
            self.proxyLabel.setText(proxy.get("http", ""))
            self.checkLabel.setVisible(False)
        else:
            self.checkLabel.setVisible(True)

    def LoadHistory(self):
        if not Setting.LastProxyResult.value:
            return
        try:
            for k, v in Setting.LastProxyResult.value.items():
                if hasattr(self, k):
                    getattr(self, k).setText(str(v))
        except Exception as es:
            Log.Error(es)

    def SaveHistory(self):
        Setting.LastProxyResult.SetValue(dict(self.lastResult))

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
        self.radioButton_6.setEnabled(enabled)
        self.radio_img_1.setEnabled(enabled)
        self.radio_img_2.setEnabled(enabled)
        self.radio_img_3.setEnabled(enabled)
        self.radio_img_4.setEnabled(enabled)
        self.radio_img_5.setEnabled(enabled)
        self.radio_img_6.setEnabled(enabled)
        # self.radioButton_5.setEnabled(enabled)

    def RandomUa(self):
        # str1 = random.sample('qwertyuiopasdfghjklzxcvbnm1234567890', 7)
        # ua = "Mozilla/5.0 (Linux; Android 7.1.2; {} Build/N2G47O; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36".format(str1)
        ua = random.choice(UALIST)
        self.uaEdit.setText(ua)
        return

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
        self.uaEdit.setText(Setting.UerAgent.value)
        self.loginProxy.setChecked(bool(Setting.IsLoginProxy.value))
        self.apiTimeout.setCurrentIndex(Setting.ApiTimeOut.value)
        self.imgTimeout.setCurrentIndex(Setting.ImgTimeOut.value)

    def SaveSetting(self):
        Setting.IsHttpProxy.SetValue(int(self.radioProxyGroup.checkedId()))
        Setting.Sock5Proxy.SetValue(self.sockEdit.text())
        Setting.HttpProxy.SetValue(self.httpLine.text())
        Setting.ProxySelectIndex.SetValue(self.radioApiGroup.checkedId())
        Setting.ProxyImgSelectIndex.SetValue(self.radioImgGroup.checkedId())
        Setting.IsLoginProxy.SetValue(int(self.loginProxy.isChecked()))
        Setting.PreferCDNIPImg.SetValue(self.cdn_img_ip.text())
        Setting.PreferCDNIP.SetValue(self.cdn_api_ip.text())
        Setting.UerAgent.SetValue(self.uaEdit.text())
        Setting.ApiTimeOut.SetValue(self.apiTimeout.currentIndex())
        Setting.ImgTimeOut.SetValue(self.imgTimeout.currentIndex())
        # Setting.DohAddress.SetValue(self.dohEdit.text())
        # Setting.IsOpenDoh.SetValue(int(self.dohBox.isChecked()))
        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def UpdateServer(self):
        index = Setting.ProxySelectIndex.value-1
        index2 = Setting.ProxyImgSelectIndex.value-1
        # if index < 0 or index >= len(GlobalConfig.Url2List.value):
        #     index = 0
        # if index2 < 0 or index2 >= len(GlobalConfig.PicUrlList.value):
        #     index2 = 0

        # GlobalConfig.Url2.value = GlobalConfig.Url2List.value[index]
        # GlobalConfig.PicUrl2.value = GlobalConfig.PicUrlList.value[index2]
        if Setting.ProxyImgSelectIndex.value == 5:
            imageServer = Setting.PreferCDNIPImg.value
        else:
            imageServer = ""
        if Setting.ProxySelectIndex.value == 5:
            address = Setting.PreferCDNIP.value
        else:
            address = ""
        if Setting.IsLoginProxy.value:
            Server().UpdateDns(address, imageServer)
        else:
            Server().UpdateDns(address, imageServer)
        Server().UpdateProxy2()
        # QtOwner().settingView.SetSock5Proxy()
        Log.Warn("update proxy, ver:{}, setId:{}:{}, address:{}, img:{}".format(config.UpdateVersion, Setting.ProxySelectIndex.value, Setting.ProxyImgSelectIndex.value, address, imageServer))

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
        for index, address in enumerate(GlobalConfig.Url2List.value):
            imageUrl = GlobalConfig.PicUrlList.value[index]
            self.speedTest.append((address, imageUrl, False, False, ("", ""), i))
            i += 1

        PreferCDNIP = self.cdn_api_ip.text()
        imgCDNIP = self.cdn_img_ip.text()
        if PreferCDNIP or imgCDNIP:
            self.speedTest.append((GlobalConfig.CdnApiUrl.value, GlobalConfig.CdnImgUrl.value, False, False, (PreferCDNIP, imgCDNIP), i))
            i += 1
        else:
            i += 1

        self.speedTest.append((GlobalConfig.ProxyApiUrl.value, GlobalConfig.ProxyImgUrl.value, False, True, (GlobalConfig.ProxyApiDomain2.value, GlobalConfig.ProxyImgDomain2.value), i))
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
            request.proxyUrl = GlobalConfig.ProxyApiDomain2.value
        else:
            request.proxyUrl = ""

        # if self.radioProxyGroup.checkedId() == 2:
        #     self.SetSock5Proxy(True)
        # else:
        #     self.SetSock5Proxy(False)

        Server().UpdateDns(dnslist[0], dnslist[1])
        Server().UpdateProxy2(self.radioProxyGroup.checkedId(), self.httpLine.text(), self.sockEdit.text())
        
        host = ToolUtil.GetUrlHost(request.url)
        host2 = ToolUtil.GetUrlHost(address)
        request.url = request.url.replace(host, host2)
        self.pingBackNumCnt[i] = 0
        self.pingBackNumDict[i] = [0, 0, 0]
        
        request.timeout = 2
        request1 = deepcopy(request)
        request1.timeout = 2
        request2 = deepcopy(request)
        request2.timeout = 5
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request, x), self.SpeedTestPingBack, (i, 0))
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request1, x), self.SpeedTestPingBack, (i, 1))
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request2, x), self.SpeedTestPingBack, (i, 2))
        self.needBackNum += 1
        return

    def SpeedTestPingBack(self, raw, v):
        i, backNum = v
        data = raw["data"]
        st = raw["st"]
        objectName = "label_api_" + str(i)
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
                text = "<font color=#7fb80e>{}</font>".format(str(int(float(sumData / sumCnt))) + "ms")
                label.setText(text)
            else:
                text = "<font color=#d71345>{}</font>".format(Str.GetStr(int(sumSt)))
                label.setText(text)

            self.speedPingNum += 1
            self.lastResult[objectName] = text
            self.StartSpeedPing()
            return

    def StartSpeedTest(self):
        if len(self.speedTest) <= self.speedIndex:
            self.UpdateServer()
            self.SetEnabled(True)
            self.SaveHistory()
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
            request.proxyUrl = GlobalConfig.ProxyImgDomain2.value
        else:
            request.proxyUrl = ""

        # if self.radioProxyGroup.checkedId() == 2:
        #     self.SetSock5Proxy(True)
        # else:
        #     self.SetSock5Proxy(False)
        Server().UpdateDns(dnslist[0], dnslist[1])
        Server().UpdateProxy2(self.radioProxyGroup.checkedId(), self.httpLine.text(), self.sockEdit.text())
        
        host = ToolUtil.GetUrlHost(request.url)
        host2 = ToolUtil.GetUrlHost(imgUrl)
        request.url = request.url.replace(host, host2)
        request.timeout = 5
        self.AddHttpTask(lambda x: Server().TestSpeed(request, x), self.SpeedTestBack, i)
        return

    def SpeedTestBack(self, raw, i):
        data = raw["data"]
        st = raw["st"]
        if not data:
            data = "<font color=#d71345>{}</font>".format(Str.GetStr(st))
        else:
            data = "<font color=#7fb80e>{}</font>".format(data)
        objectName = "label_img_" + str(i)
        label = getattr(self, "label_img_" + str(i))
        label.setText(data)
        self.speedIndex += 1
        self.lastResult[objectName] = data
        self.StartSpeedTest()
        return

    def OpenUrl(self):
        QtOwner().owner.helpView.OpenProxyUrl()

    # def SetSock5Proxy(self, isProxy):
    #     import socket
    #     import socks
    #     if not QtOwner().backSock:
    #         QtOwner().backSock = socket.socket
    #     if isProxy:
    #         data = self.sockEdit.text().replace("http://", "").replace("https://", "").replace("sock5://", "")
    #         data = data.split(":")
    #         if len(data) == 2:
    #             host = data[0]
    #             port = data[1]
    #             socks.set_default_proxy(socks.SOCKS5, host, int(port))
    #             socket.socket = socks.socksocket
    #     else:
    #         socks.set_default_proxy()
    #         socket.socket = QtOwner().backSock