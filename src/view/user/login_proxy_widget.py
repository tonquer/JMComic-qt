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
        self.buttonGroup.setId(self.radioButton_1, 1)
        self.buttonGroup.setId(self.radioButton_2, 2)
        self.buttonGroup.setId(self.radioButton_3, 3)
        self.buttonGroup.setId(self.radioButton_4, 4)
        self.testSpeedButton.clicked.connect(self.SpeedTest)

        self.buttonGroup_2.setId(self.proxy_0, 0)
        self.buttonGroup_2.setId(self.proxy_1, 1)
        self.buttonGroup_2.setId(self.proxy_2, 2)
        self.LoadSetting()
        self.UpdateServer()

    def Init(self):
        self.LoadSetting()

    def ClickButton(self):
        self.SaveSetting()

    def SetEnabled(self, enabled):
        self.testSpeedButton.setEnabled(enabled)
        self.dohBox.setEnabled(enabled)
        self.dohEdit.setEnabled(enabled)
        self.proxy_0.setEnabled(enabled)
        self.proxy_1.setEnabled(enabled)
        self.proxy_2.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.sockEdit.setEnabled(enabled)
        self.radioButton_1.setEnabled(enabled)
        self.radioButton_2.setEnabled(enabled)
        self.radioButton_3.setEnabled(enabled)
        self.radioButton_4.setEnabled(enabled)

    def LoadSetting(self):
        self.dohBox.setChecked(Setting.IsOpenDoh.value)
        self.dohEdit.setText(Setting.DohAddress.value)
        self.httpLine.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)
        button = getattr(self, "radioButton_{}".format(Setting.ProxySelectIndex.value))
        button.setChecked(True)
        button = getattr(self, "proxy_{}".format(int(Setting.IsHttpProxy.value)))
        button.setChecked(True)

    def SaveSetting(self):
        Setting.IsHttpProxy.SetValue(int(self.buttonGroup_2.checkedId()))
        Setting.Sock5Proxy.SetValue(self.sockEdit.text())
        Setting.HttpProxy.SetValue(self.httpLine.text())
        Setting.ProxySelectIndex.SetValue(self.buttonGroup.checkedId())
        Setting.DohAddress.SetValue(self.dohEdit.text())
        Setting.IsOpenDoh.SetValue(int(self.dohBox.isChecked()))
        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def UpdateServer(self):
        index = Setting.ProxySelectIndex.value-1
        if index < 0 or index >= len(config.Url2List):
            index = 0
        config.Url2 = config.Url2List[index]
        config.PicUrl2 = config.PicUrlList[index]
        QtOwner().settingView.SetSock5Proxy()
        Log.Info("update proxy, setId:{}".format(Setting.ProxySelectIndex.value))

    def SpeedTest(self):
        self.speedIndex = 0
        self.speedPingNum = 0
        self.speedTest = []

        for i in range(1, 9):
            label = getattr(self, "label" + str(i))
            label.setText("")

        i = 1
        for index, address in enumerate(config.Url2List):
            imageUrl = config.PicUrlList[index]
            self.speedTest.append((address, imageUrl, False, i))
            i += 1
            self.speedTest.append((address, imageUrl, True, i))
            i += 1

        self.SetEnabled(False)
        self.StartSpeedPing()

    def StartSpeedPing(self):
        if len(self.speedTest) <= self.speedPingNum:
            self.StartSpeedTest()
            return
        address, _, isHttpProxy, i = self.speedTest[self.speedPingNum]
        httpProxy = self.httpLine.text()
        if isHttpProxy and (self.buttonGroup_2.checkedId() == 0 or
                            (self.buttonGroup_2.checkedId() == 1 and not self.httpLine.text()) or
                            (self.buttonGroup_2.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label"+str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedPingNum += 1
            self.StartSpeedPing()
            return

        request = req.SpeedTestPingReq()
        if isHttpProxy and self.buttonGroup_2.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""

        if isHttpProxy and self.buttonGroup_2.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)
        request.timeout = 2
        request.url = request.url.replace(config.Url2, address)
        self.AddHttpTask(request, self.SpeedTestPingBack, i)
        return

    def SpeedTestPingBack(self, raw, i):
        data = raw["data"]
        label = getattr(self, "label" + str(i))
        if float(data) > 0.0:
            label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data)*500)) + "ms") + "/")
        else:
            label.setText("<font color=#d71345>{}</font>".format("fail") + "/")
        self.speedPingNum += 1
        self.StartSpeedPing()
        return

    def StartSpeedTest(self):
        if len(self.speedTest) <= self.speedIndex:
            self.UpdateServer()
            self.SetEnabled(True)
            return

        _, imgUrl, isHttpProxy, i = self.speedTest[self.speedIndex]
        httpProxy = self.httpLine.text()
        if isHttpProxy and (self.buttonGroup_2.checkedId() == 0 or
                            (self.buttonGroup_2.checkedId() == 1 and not self.httpLine.text()) or
                            (self.buttonGroup_2.checkedId() == 2 and not self.sockEdit.text())):
            label = getattr(self, "label" + str(i))
            label.setText(Str.GetStr(Str.NoProxy))
            self.speedIndex += 1
            self.StartSpeedTest()
            return

        request = req.SpeedTestReq()
        if isHttpProxy and self.buttonGroup_2.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        else:
            request.proxy = ""

        if isHttpProxy and self.buttonGroup_2.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)
        request.timeout = 2
        request.url = request.url.replace(config.PicUrl2, imgUrl)
        self.AddHttpTask(request, self.SpeedTestBack, i)
        return

    def SpeedTestBack(self, raw, i):
        data = raw["data"]
        if not data:
            data = "<font color=#d71345>fail</font>"
        else:
            data = "<font color=#7fb80e>{}</font>".format(data)
        label = getattr(self, "label" + str(i))
        label.setText(label.text()+data)
        self.speedIndex += 1
        self.StartSpeedTest()
        return

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