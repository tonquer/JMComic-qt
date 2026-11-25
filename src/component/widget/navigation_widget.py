import re
import time
from datetime import datetime

from PySide6.QtCore import Property, QPropertyAnimation, QRect, QEasingCurve, QFile, QEvent, QSize, QTimer
from PySide6.QtGui import QPixmap, Qt, QIcon, QGuiApplication
from PySide6.QtWidgets import QWidget, QScroller, QScrollerProperties, QCalendarWidget

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from interface.ui_navigation import Ui_Navigation
from interface.ui_sign_widget import Ui_SignWidget
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase, TaskBase
from tools.langconv import Converter
from tools.log import Log
from tools.status import Status
from tools.str import Str
from tools.svg_icon import RenderStatefulSvgIcon
from tools.tool import ToolUtil
from view.user.sign_view import SignView


class NavigationWidget(QWidget, Ui_Navigation, QtTaskBase):
    EXPANDED_WIDTH = 252
    COLLAPSED_WIDTH = 58

    def __init__(self, parent=None):
        super().__init__(parent)
        QtTaskBase.__init__(self)
        self.allFilterStr = set()
        self._isCollapsed = False
        self._isUserLoggedIn = False
        self._avatarBytes = None
        self._navIconSpecs = ()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setupUi(self)
        self.setMinimumWidth(self.EXPANDED_WIDTH)
        self.setMaximumWidth(self.EXPANDED_WIDTH)
        self.resize(self.EXPANDED_WIDTH, 800)
        self.timer = QTimer(self)
        # 取余数
        second = 3600 - int(time.time()) % 3600
        self.timer.setInterval(1000*(second+10))
        self.timer.timeout.connect(self.HourTimeOut)
        self.timer.start()

        self.__ani = QPropertyAnimation(self, b"navWidth", self)
        self.__ani.setEasingCurve(QEasingCurve.OutCubic)
        self.__ani.setDuration(160)
        self.__ani.finished.connect(self._OnWidthAniFinished)
        self.__connect = None
        self.pictureData = ""
        f = QFile(u":/png/icon/placeholder_avatar.png")
        f.open(QFile.ReadOnly)
        self._avatarBytes = f.readAll()
        self.picLabel.SetPicture(self._avatarBytes)
        f.close()
        self.picLabel.setCursor(Qt.PointingHandCursor)
        self.titleLabel.setMinimumWidth(0)
        self.pushButton.clicked.connect(self.OpenLoginView)
        self.picLabel.installEventFilter(self)
        self.picData = None
        self.offlineButton.SetState(False)
        self.offlineButton.Switch.connect(self.SwitchOffline)

        # self.signButton.setEnabled(False)
        self.signId = 0
        self.signMap = {}
        self.canResign = False
        self.maxReSignNum = 5
        self.useReSignNum = 0
        self.signButton.clicked.connect(self.OpenSign)
        self.isDailySign = False
        self.resetDailySign = 3
        self.proxyImgName.clicked.connect(self.OpenProxy)
        self.proxyName.clicked.connect(self.OpenProxy)
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.ScrollerGestureType.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.VerticalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.HorizontalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)
        self.hideButton.clicked.connect(self.OpenForbidWords)
        self.tmpSignView = None
        TaskBase.taskObj.statuImgBack.connect(self.StatusImgBack)
        TaskBase.taskObj.statuApiBack.connect(self.StatusApiBack)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.RefreshDisplay)
        self.refresh_timer.start(2000)

        self._hasNewUpdate = False
        self._navIconSpecs = (
            (self.collectButton, "star"),
            (self.myCommentButton, "message_square"),
            (self.remoteHistoryButton, "clock"),
            (self.localCollectButton, "bookmark"),
            (self.historyButton, "history"),
            (self.indexButton, "home"),
            (self.searchButton, "search"),
            (self.categoryButton, "grid"),
            (self.weekButton, "calendar"),
            (self.commentButton, "comment"),
            (self.downloadButton, "download"),
            (self.nasButton, "cloud"),
            (self.localReadButton, "folder"),
            (self.waifu2xButton, "sparkles"),
            (self.batchSrButton, "layers"),
            (self.helpButton, "help"),
            (self.settingButton, "settings"),
        )
        for btn, _ in self._navIconSpecs:
            btn.setMinimumWidth(0)
            btn.setIconSize(QSize(18, 18))
            btn.setCursor(Qt.PointingHandCursor)
        self._sectionLabels = (self.label, self.label_2, self.label_3)
        self._topActionWidgets = (
            self.pushButton,
            self.signButton,
            self.label_4,
            self.label_5,
            self.label_7,
            self.label_9,
            self.proxyName,
            self.proxyImgName,
            self.offlineButton,
            self.hideButton,
        )
        self._userInfoWidgets = (
            self.nameLabel,
            self.titleLabel,
            self.label_6,
            self.coins,
            self.expLabel,
            self.levelLabel,
            self.label_8,
            self.favorite,
        )
        self.setProperty("collapsed", False)
        self._RefreshNavIcons()
        self._SetUserInfoVisible(False)

    def _getNavWidth(self):
        return self.width()

    def _setNavWidth(self, w):
        w = int(w)
        self.setMinimumWidth(w)
        self.setMaximumWidth(w)

    navWidth = Property(int, _getNavWidth, _setNavWidth)

    @property
    def isCollapsed(self) -> bool:
        return self._isCollapsed

    def _SetUserInfoVisible(self, visible: bool):
        self._isUserLoggedIn = bool(visible)
        show = self._isUserLoggedIn and not self._isCollapsed
        for w in self._userInfoWidgets:
            w.setVisible(show)

    def _RenderAvatarForSize(self, size: int):
        self.picLabel.setFixedSize(size, size)
        if self._avatarBytes:
            self.picLabel.SetPicture(self._avatarBytes)

    def _ApplyCollapsedLayout(self, collapsed: bool):
        self.setProperty("collapsed", collapsed)
        self.style().unpolish(self)
        self.style().polish(self)

        for lbl in self._sectionLabels:
            lbl.setVisible(not collapsed)
        for w in self._topActionWidgets:
            w.setVisible(not collapsed)
        for w in self._userInfoWidgets:
            w.setVisible((not collapsed) and self._isUserLoggedIn)

        if collapsed:
            self.verticalLayout.setContentsMargins(0, 6, 0, 6)
            self.verticalLayout_4.setContentsMargins(0, 4, 0, 4)
            self.verticalLayout_5.setContentsMargins(0, 4, 0, 6)
            self._RenderAvatarForSize(36)
            tip = self.nameLabel.text() if self._isUserLoggedIn and self.nameLabel.text() else Str.GetStr(Str.Login)
            self.picLabel.setToolTip(tip)
        else:
            self.verticalLayout.setContentsMargins(6, 6, 6, 6)
            self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
            self.verticalLayout_5.setContentsMargins(4, 4, 4, 6)
            self._RenderAvatarForSize(72)
            self.picLabel.setToolTip("")

        iconPx = 20 if collapsed else 18
        btnStyle = Qt.ToolButtonStyle.ToolButtonIconOnly if collapsed else Qt.ToolButtonStyle.ToolButtonTextBesideIcon
        for btn, _ in self._navIconSpecs:
            btn.setToolButtonStyle(btnStyle)
            btn.setIconSize(QSize(iconPx, iconPx))
            btn.setToolTip(btn.text() if collapsed else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._RefreshNavIcons()

    def _OnWidthAniFinished(self):
        if not self._isCollapsed:
            self._ApplyCollapsedLayout(False)

    def ToggleCollapsed(self):
        self.SetCollapsed(not self._isCollapsed, animate=True)

    def SetCollapsed(self, collapsed: bool, animate: bool = True):
        collapsed = bool(collapsed)
        targetWidth = self.COLLAPSED_WIDTH if collapsed else self.EXPANDED_WIDTH
        if self._isCollapsed == collapsed and not self.isHidden() and self.minimumWidth() == targetWidth and self.maximumWidth() == targetWidth:
            return
        super().show()
        self._isCollapsed = collapsed

        if collapsed:
            self._ApplyCollapsedLayout(True)

        self.__ani.stop()
        if animate:
            self.__ani.setStartValue(self.width())
            self.__ani.setEndValue(targetWidth)
            self.__ani.start()
        else:
            self._setNavWidth(targetWidth)
            if not collapsed:
                self._ApplyCollapsedLayout(False)

    def _RefreshNavIcons(self):
        isDark = Setting.ThemeIndex.autoValue == 1
        normalColor = "#94A3B8" if isDark else "#64748B"
        activeColor = QtOwner().GetThemeColorList(0)
        iconPx = 20 if self._isCollapsed else 18
        for btn, iconName in self._navIconSpecs:
            if btn is self.helpButton and self._hasNewUpdate:
                btn.setIcon(QtOwner().globalNewIcon)
            else:
                btn.setIcon(RenderStatefulSvgIcon(iconName, normalColor, activeColor, iconPx))

    def RefreshDisplay(self):
        self.proxyName.refresh_display()
        self.proxyImgName.refresh_display()

    def StatusImgBack(self, tick, st, status_code, size):
        if st != Status.Ok and status_code != 200:
            self.proxyImgName.update_result(-1)
        else:
            self.proxyImgName.update_result(int(tick*1000))
            self.proxyImgName.add_traffic(size)
        return

    def StatusApiBack(self, tick, st, status_code, size):
        if st != Status.Ok and status_code != 200:
            self.proxyName.update_result(-1)
        else:
            self.proxyName.update_result(int(tick*1000))
            self.proxyName.add_traffic(size)
        return

    def IsInFilter(self, categoryList, tagList, title):
        categoryList2 = Converter('zh-hans').convert(categoryList)
        tagList2 = Converter('zh-hans').convert(tagList)
        title2 = Converter('zh-hans').convert(title)
        if Setting.IsForbidCategory.value:
            for v in re.split(r"[,，]", categoryList2):
                if v in self.allFilterStr:
                    return True

        if Setting.IsForbidTag.value:
            for v in re.split(r"[,，]", tagList2):
                if v in self.allFilterStr:
                    return True

        if Setting.IsForbidTitle.value:
            for v in self.allFilterStr:
                if v in title2:
                    return True
        return False

    def retranslateUi(self, View):
        Ui_Navigation.retranslateUi(self, self)
        self.UpdateFilterStr()
        if self._isCollapsed:
            for btn, _ in self._navIconSpecs:
                btn.setToolTip(btn.text())

    def RefrshTheme(self):
        self.proxyName.update_theme()
        self.proxyImgName.update_theme()
        self.offlineButton.update()
        self._RefreshNavIcons()

    def UpdateFilterStr(self):
        self.allFilterStr.clear()
        num = 0
        for v in Setting.ForbidWords.value:
            v2 = Converter('zh-hans').convert(v)
            self.allFilterStr.add(v2)
            num += 1
        self.hideButton.setText("已选{}个".format(num))

    def OpenProxy(self):
        QtOwner().OpenProxy()
        self.UpdateProxyName()

    def OpenSign(self):
        if not QtOwner().user.isLogin:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        if self.isDailySign:
            signView = SignView(QtOwner().owner, self.signMap)
            signView.reSignButton.clicked.connect(self.ReSign)
            signView.reSignButton.setText(Str.GetStr(Str.ReSign) + f"({self.useReSignNum}/{self.maxReSignNum})")
            signView.closed.connect(self.CloseSignView)
            self.tmpSignView = signView
            signView.show()
        else:
            curDate = datetime.today().day
            self.AddHttpTask(req.SignDailyReq2(QtOwner().user.uid, self.signId), self.GetSignBack, curDate)
        return

    def CloseSignView(self):
        self.tmpSignView = None

        return

    def ReSign(self):
        # 选择一个未签到
        curDay = datetime.today().day
        day = None
        for k, v in sorted(self.signMap.items(), key=lambda a:a[0]):
            if k > curDay:
                continue
            if not v:
                day = k
                break
        if not day:
            return
        year = datetime.today().year
        month = datetime.today().month
        dt = datetime(year=year, month=month, day=day)
        date = dt.strftime("%Y-%m-%d")
        QtOwner().ShowLoading()
        self.AddHttpTask(req.SignDailyReq2(QtOwner().user.uid, self.signId, date=date), self.GetSignBack, day)

    def SwitchOffline(self, state):
        QtOwner().isOfflineModel = state
        return

    def OpenLoginView(self):
        # 已登录时这个按钮的文字是「登出」，点击应该登出，而不是再弹一次登录框
        if QtOwner().user.isLogin:
            self.Logout()
            return
        QtOwner().OpenLogin()
        return

    def Logout(self):
        # 清的是 QtOwner 持有的那个真实会话对象；User() 会新建一个
        # 临时对象，清它等于什么都没做，token 和 cookie 都还在
        QtOwner().user.Logout()
        # 在途的账号请求返回后不再交给界面，避免把旧账号数据填回来
        QtOwner().NewRequestGeneration()
        # 关闭自动登录并清掉保存的凭据，否则下次启动会立刻又登回去
        Setting.AutoLogin.SetValue(0)
        Setting.UserId.SetValue("")
        Setting.Password.SetValue("")
        Setting.SaveSetting()

        # 清空界面上残留的个人信息（本地已下载的漫画和阅读记录不会被动到）
        for label in (self.nameLabel, self.titleLabel, self.levelLabel,
                      self.favorite, self.coins):
            label.setText("")
        self._SetUserInfoVisible(False)
        self.picData = None
        self.pictureData = ""
        f = QFile(u":/png/icon/placeholder_avatar.png")
        if f.open(QFile.ReadOnly):
            self._avatarBytes = f.readAll()
            self.picLabel.SetPicture(self._avatarBytes)
            f.close()
        self.signId = 0
        self.signMap.clear()
        self.canResign = False
        self.isDailySign = False
        self.useReSignNum = 0
        self.maxReSignNum = 5
        self.resetDailySign = 3
        self.signButton.setText(Str.GetStr(Str.Sign))
        if self.tmpSignView:
            self.tmpSignView.close()
            self.tmpSignView = None
        config.LoginUserName = ""
        self.pushButton.setText(Str.GetStr(Str.Login))

        # 清掉界面上已经加载的该账号数据（收藏、历史、评论），磁盘上的数据不受影响
        try:
            QtOwner().owner.ClearAccountViews()
        except Exception as es:
            Log.Error(es)
        return

    def LoginSucBack(self):
        self.UpdateProxyName()
        # QtOwner().owner.LoginSucBack()
        if not QtOwner().user.isLogin:
            return
        # self.pushButton.hide()
        user = QtOwner().user
        self.levelLabel.setText("LV" + str(user.level) + "(" + str(user.exp) + "/" + str(user.nex_exp) + ")")
        self.favorite.setText("(" + str(user.favorites) + "/" + str(user.canFavorites) + ")")
        self.coins.setText(str(user.coin))
        self.titleLabel.setText(str("("+user.title+")"))
        self.nameLabel.setText(str(user.name))
        self._SetUserInfoVisible(True)
        config.LoginUserName = user.name.replace("@", "")
        if user.imgUrl and config.IsLoadingPicture:
            path = ToolUtil.GetRealPath(user.uid, "user")
            self.AddDownloadTask(user.imgUrl, path, completeCallBack=self.ShowUserImg)

        self.pushButton.setText(Str.GetStr(Str.LoginOut))
        self.AddHttpTask(req.GetDailyReq2(user.uid), self.GetSignDailyBack)
    #     self.AddHttpTask(req.GetUserInfoReq(), self.UpdateUserBack)

    def HourTimeOut(self):
        Log.Info("check_next_sign")
        self.timer.setInterval(1000*3600)
        if not QtOwner().user.isLogin:
            return
        user = QtOwner().user
        self.AddHttpTask(req.GetDailyReq2(user.uid), self.GetSignDailyBack)

    def GetSignDailyBack(self, raw):
        st = raw["st"]
        curDate = datetime.today().day
        if st == Status.Ok:
            data = raw.get("data", {})
            self.signId = data.get("daily_id", 0)
            self.signMap.clear()
            self.maxReSignNum = data.get('makeup_limit', 0)
            self.useReSignNum = data.get('makeup_used', 0)
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
                if Setting.AutoSign.value and self.resetDailySign > 0:
                    QtOwner().ShowMsg(Str.GetStr(Str.AutoCheckInDone))
                    self.resetDailySign -= 1
                    self.signButton.click()
        pass

    def GetSignBack(self, raw, curDate):
        QtOwner().CloseLoading()
        st = raw.get("st")
        msg = raw.get("data", {}).get("msg", "")
        if st == Status.Ok:
            self.isDailySign = True
            self.signButton.setText(Str.GetStr(Str.AlreadySign))
            self.signMap[curDate] = True
            if self.tmpSignView:
                self.tmpSignView.UpdateSign(curDate)
        else:
            self.AddHttpTask(req.GetDailyReq2(QtOwner().user.uid), self.GetSignDailyBack)
        QtOwner().ShowError(msg if msg else Str.GetStr(st))

    def UpdateProxyName(self):
        if GlobalConfig.IsCdnIndex(Setting.ProxySelectIndex.value):
            name = QtOwner().loginNewView.proxyWidget.GetProxyName()
            self.proxyName.setText(name)
        elif GlobalConfig.IsProxyUrlIndex(Setting.ProxySelectIndex.value):
            self.proxyName.setText(Str.GetStr(Str.UsProxyRoute))
        elif Setting.ProxySelectIndex.value == 7:
            self.proxyName.setText(Str.GetStr(Str.CustomDomain))
        else:
            self.proxyName.setText(Str.GetStr(Str.Route).format(Setting.ProxySelectIndex.value))

        if GlobalConfig.IsCdnIndex(Setting.ProxyImgSelectIndex.value):
            name = QtOwner().loginNewView.proxyWidget.GetProxyName()
            self.proxyImgName.setText(name)
        elif GlobalConfig.IsProxyUrlIndex(Setting.ProxyImgSelectIndex.value):
            self.proxyImgName.setText(Str.GetStr(Str.UsProxyRoute))
        elif Setting.ProxyImgSelectIndex.value == 7:
            self.proxyImgName.setText(Str.GetStr(Str.CustomDomain))
        else:
            self.proxyImgName.setText(Str.GetStr(Str.Route).format(Setting.ProxyImgSelectIndex.value))

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
        self._avatarBytes = data
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
        """ 展开侧边栏 """
        self.SetCollapsed(False, animate=True)

    def aniHide(self):
        """ 折叠为紧凑图标栏 """
        self.SetCollapsed(True, animate=True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.picLabel:
                    if self._isCollapsed:
                        self.SetCollapsed(False, animate=True)
                        return True
                    if self.picData:
                        QtOwner().OpenWaifu2xTool(self.picData)
                        return True
                return False
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def SetNewUpdate(self):
        self._hasNewUpdate = True
        self.helpButton.setIcon(QtOwner().globalNewIcon)
        return

    def OpenForbidWords(self, bookId=""):
        from view.tool.forbid_words_view import ForbidWordsView
        w = ForbidWordsView(QtOwner().owner, self, bookId)

        w.show()
        w.AddFold.connect(self.AddCategory)
        w.DelFold.connect(self.DelCategory)
        w.MoveOkBack.connect(self.MoveCategory)

    def AddCategory(self, words):
        if words in Setting.AddForbidWords.value:
            return
        newList = Setting.AddForbidWords.value[::]
        newList.append(words)
        Setting.AddForbidWords.SetValue(newList)
        self.UpdateFilterStr()
        return

    def DelCategory(self, words):
        if words not in Setting.AddForbidWords.value:
            return
        newList = Setting.AddForbidWords.value[::]
        newList.remove(words)
        Setting.AddForbidWords.SetValue(newList)

        words2 = Converter('zh-hans').convert(words)
        if words2 not in Setting.ForbidWords.value:
            return
        newList = Setting.ForbidWords.value[::]
        newList.remove(words2)
        Setting.ForbidWords.SetValue(newList)
        self.UpdateFilterStr()
        return

    def MoveCategory(self, words, list):
        self.UpdateFilterStr()
        return

    def Stop(self):
        self.timer.stop()
        self.refresh_timer.stop()
