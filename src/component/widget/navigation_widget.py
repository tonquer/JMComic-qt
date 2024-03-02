import time
from datetime import datetime

from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QFile, QEvent, QSize
from PySide6.QtGui import QPixmap, Qt, QIcon
from PySide6.QtWidgets import QWidget, QScroller, QScrollerProperties, QCalendarWidget

from config import config
from config.setting import Setting
from interface.ui_navigation import Ui_Navigation
from interface.ui_sign_widget import Ui_SignWidget
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from tools.user import User
from view.user.login_view import LoginView
from view.user.sign_view import SignView


class NavigationWidget(QWidget, Ui_Navigation, QtTaskBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.resize(260, 800)
        self.__ani = QPropertyAnimation(self, b"geometry")
        self.__connect = None
        self.pictureData = ""
        f = QFile(u":/png/icon/placeholder_avatar.png")
        f.open(QFile.ReadOnly)
        self.picLabel.SetPicture(f.readAll())
        f.close()
        self.pushButton.clicked.connect(self.OpenLoginView)
        self.picLabel.installEventFilter(self)
        self.picData = None
        self.offlineButton.SetState(False)
        self.offlineButton.Switch.connect(self.SwitchOffline)
        # self.signButton.setEnabled(False)
        self.signId = 0
        self.signMap = {}
        self.signButton.clicked.connect(self.OpenSign)
        self.isDailySign = False

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)

    def OpenSign(self):
        if self.isDailySign:
            signView = SignView(QtOwner().owner, self.signMap)
            signView.show()
        else:
            self.AddHttpTask(req.SignDailyReq2(QtOwner().user.uid, self.signId), self.GetSignBack)
        return

    def SwitchOffline(self, state):
        QtOwner().isOfflineModel = state
        return

    def OpenLoginView(self):
        isAutoLogin = Setting.AutoLogin.value
        if QtOwner().user.isLogin:
            # self.Sign()
            self.Logout()
            isAutoLogin = 0

        loginView = LoginView(QtOwner().owner, isAutoLogin)
        loginView.show()
        loginView.closed.connect(self.LoginSucBack)
        return

    def Logout(self):
        User().Logout()
        self.pushButton.setText(Str.GetStr(Str.Login))
        return

    def LoginSucBack(self):
        self.UpdateProxyName()
        QtOwner().owner.LoginSucBack()
        if not QtOwner().user.isLogin:
            return
        # self.pushButton.hide()
        user = QtOwner().user
        self.levelLabel.setText("LV" + str(user.level) + "(" + str(user.exp) + "/" + str(user.nex_exp) + ")")
        self.favorite.setText("(" + str(user.favorites) + "/" + str(user.canFavorites) + ")")
        self.coins.setText(str(user.coin))
        self.titleLabel.setText(str(user.title))
        self.nameLabel.setText(str(user.name))
        config.LoginUserName = user.name.replace("@", "")
        if user.imgUrl and config.IsLoadingPicture:
            self.AddDownloadTask(user.imgUrl, "", completeCallBack=self.ShowUserImg)

        self.pushButton.setText(Str.GetStr(Str.LoginOut))
        self.AddHttpTask(req.GetDailyReq2(user.uid), self.GetSignDailyBack)
    #     self.AddHttpTask(req.GetUserInfoReq(), self.UpdateUserBack)

    def GetSignDailyBack(self, raw):
        st = raw["st"]
        curDate = datetime.today().day
        if st == Status.Ok:
            data = raw.get("data", {})
            self.signId = data.get("daily_id", 0)
            self.signMap.clear()
            for v in data.get('record', []):
                for v2 in v:
                    signDate = int(v2["date"])
                    self.signMap[signDate] = v2.get('signed')
                    if signDate == curDate:
                        self.isDailySign = v2.get('signed')
        if self.isDailySign:
            self.signButton.setText(Str.GetStr(Str.AlreadySign))
        else:
            self.signButton.setText(Str.GetStr(Str.Sign))
            if Setting.AutoSign.value:
                QtOwner().ShowMsg("已自动打卡")
                self.signButton.click()
        pass

    def GetSignBack(self, raw):
        st = raw.get("st")
        msg = raw.get("data", {}).get("msg", "")
        if st == Status.Ok:
            self.isDailySign = True
            self.signButton.setText(Str.GetStr(Str.AlreadySign))
        QtOwner().ShowError(msg if msg else Str.GetStr(st))


    def UpdateProxyName(self):
        if Setting.ProxySelectIndex.value == 5:
            self.proxyName.setText("CDN_{}".format(str(Setting.PreferCDNIP.value)))
        else:
            self.proxyName.setText("分流{}".format(str(Setting.ProxySelectIndex.value)))

        if Setting.ProxyImgSelectIndex.value == 5:
            self.proxyImgName.setText("CDN_{}".format(str(Setting.PreferCDNIPImg.value)))
        else:
            self.proxyImgName.setText("分流{}".format(str(Setting.ProxyImgSelectIndex.value)))

    # def UpdateUserBack(self, raw):
    #     st = raw["st"]
    #     if st == Status.Ok:
    #         user = raw["user"]
    #         QtOwner().SetUser(raw["user"])
    #         self.levelLabel.setText("LV" + str(user.level))
    #         self.titleLabel.setText(str(user.title))
    #         self.nameLabel.setText(str(user.name))
    #         config.LoginUserName = user.name.replace("@", "")
    #         if user.imgUrl and config.IsLoadingPicture:
    #             self.AddDownloadTask(user.imgUrl, "", completeCallBack=self.ShowUserImg)
    #     else:
    #         QtOwner().ShowError(st)

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            self.picData = data
            self.SetPicture(data)
        return

    def SetPicture(self, data):
        self.pictureData = data
        self.picLabel.SetPicture(data)
        return

    # def UpdatePictureData(self, data):
    #     if not data:
    #         return
    #     self.picLabel.setPixmap(QPixmap())
    #     self.picLabel.setText(Str.GetStr(Str.HeadUpload))
    #     self.AddHttpTask(req.SetAvatarInfoReq(data), self.UpdatePictureDataBack)
    #     return
    #
    # def UpdatePictureDataBack(self, data):
    #     st = data["st"]
    #     if st == Status.Ok:
    #         self.AddHttpTask(req.GetUserInfoReq(), self.UpdateUserBack)
    #     else:
    #         QtOwner().ShowError(Str.GetStr(st))

    def aniShow(self):
        """ 动画显示 """
        super().show()
        self.activateWindow()
        self.__ani.setStartValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEasingCurve(QEasingCurve.InOutQuad)
        self.__ani.setDuration(85)
        self.__ani.start()

    def aniHide(self):
        """ 动画隐藏 """
        self.__ani.setStartValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__connect = self.__ani.finished.connect(self.__hideAniFinishedSlot)
        self.__ani.setDuration(85)
        self.__ani.start()

    def __hideAniFinishedSlot(self):
        """ 隐藏窗体的动画结束 """
        super().hide()
        self.resize(60, self.height())
        if self.__connect:
            self.__ani.finished.disconnect()
            self.__connect = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtOwner().OpenWaifu2xTool(self.picData)
                    return True
                return False
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def SetNewUpdate(self):
        icon2 = QIcon()
        icon2.addFile(u":/png/icon/new.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon2)
        return