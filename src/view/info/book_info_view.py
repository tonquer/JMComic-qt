import os
import re
import shutil
from datetime import datetime
from functools import partial

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon, QCursor
from PySide6.QtWidgets import QListWidgetItem, QLabel, QScroller, QPushButton, QMessageBox, QMenu, QListWidget, QFrame

from component.layout.flow_layout import FlowLayout
from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from qt_owner import QtOwner
from server import req, ToolUtil, config, Status
from task.qt_task import QtTaskBase
from task.task_cache import TaskCache
from tools.book import BookMgr, BookInfo
from tools.str import Str
from tools.svg_icon import RenderSvgIcon


class BookInfoView(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    ReloadHistory = Signal()

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self._rawCoverPixmap = None
        self._coverShadow = None
        self.setupUi(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.lastIndex = 0
        self.pictureData = None
        self._rawCoverPixmap = None
        self.isFavorite = False
        self.isLike = False

        self.picture.installEventFilter(self)
        self.picture.setCursor(Qt.PointingHandCursor)
        self.picture.setAlignment(Qt.AlignCenter)
        self._coverShadow = QtWidgets.QGraphicsDropShadowEffect(self.picture)
        self._coverShadow.setBlurRadius(20)
        self._coverShadow.setOffset(0, 4)
        self.picture.setGraphicsEffect(self._coverShadow)
        self._SetCoverEmptyState(True)
        self.label.setVisible(False)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.autorList.clicked.connect(self.ClickAutorItem)
        self.autorList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.autorList.customContextMenuRequested.connect(self.CopyClickAutorItem)

        self.idLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)

        for actionBtn in (
            self.favoriteButton,
            self.localButton,
            self.commentButton,
            self.downloadButton,
            self.uploadButton,
            self.clearButton,
        ):
            actionBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            actionBtn.setIconSize(QSize(20, 20))
            actionBtn.setCursor(Qt.PointingHandCursor)
        self.commentButton.clicked.connect(self.OpenComment)
        self.description.adjustSize()
        self.title.adjustSize()

        # self.tagsList.clicked.connect(self.ClickTagsItem)
        # self.tagsList.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tagsList.customContextMenuRequested.connect(self.CopyClickTagsItem)

        self.epsListWidget.setFlow(QListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(QListWidget.NoFrame)
        self.epsListWidget.setResizeMode(QListWidget.Adjust)

        self.epsListWidget.clicked.connect(self.OpenReadImg)

        self.listWidget.setFlow(QListWidget.LeftToRight)
        self.listWidget.setWrapping(True)
        self.listWidget.setFrameShape(QFrame.NoFrame)
        self.listWidget.setResizeMode(QListWidget.Adjust)
        self.listWidget.clicked.connect(self.OpenReadImg2)
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.epsListWidget, QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        # QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
        # self.epsListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.epsListWidget.verticalScrollBar().setStyleSheet(QssDataMgr().GetData('qt_list_scrollbar'))
        # self.epsListWidget.verticalScrollBar().setSingleStep(30)
        self.userIconData = None

        # self.epsListWidget.verticalScrollBar().rangeChanged.connect(self.ChageMaxNum)
        self.epsListWidget.setMinimumHeight(300)
        self.commentNum = 0
        self.ReloadHistory.connect(self.LoadHistory)
        self.readOffline.clicked.connect(self.StartRead2)
        self.flowLayout = FlowLayout(self.tagList)
        self.uploadButton.clicked.connect(self.ShowMenu)
        self.buyButton.setVisible(False)
        self.buyButton.clicked.connect(self.DoBuyBook)
        self.commandLinkButton.clicked.connect(self.OpenRecommend)

        self.mainButton.setVisible(False)
        self.mainButton.clicked.connect(self.OpenMainJmID)

        # self.toolMenu = QMenu(self.uploadButton)
        # self.uploadButton.setMenu(self.toolMenu)

    def retranslateUi(self, view):
        Ui_BookInfo.retranslateUi(self, view)
        self.RefreshTheme()

    def RefreshTheme(self):
        isDark = Setting.ThemeIndex.autoValue == 1
        primary = QtOwner().GetThemeColorList(0)
        softBg = QtOwner().GetThemeColorList(1)
        accentText = QtOwner().GetThemeColorList(2)
        cardBg = "#22252D" if isDark else "#FFFFFF"
        cardBorder = "#2E333E" if isDark else "#E2E8F0"
        textColor = "#E8ECF2" if isDark else "#1E293B"

        self.tagList.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {softBg};
                color: {accentText};
                border: 1px solid transparent;
                border-radius: 12px;
                padding: 0px 12px;
                height: 24px;
                min-height: 24px;
                max-height: 24px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {primary};
                border: 1px solid {primary};
                border-radius: 12px;
                color: #FFFFFF;
            }}
            """
        )
        itemQss = f"""
            QListWidget {{
                background-color: transparent;
                border: none;
            }}
            QListWidget::item {{
                background-color: {cardBg};
                color: {textColor};
                border: 1px solid {cardBorder};
                border-radius: 8px;
                padding: 4px 10px;
            }}
            QListWidget::item:hover,
            QListWidget::item:selected {{
                background-color: {primary};
                border: 1px solid {primary};
                border-radius: 8px;
                color: #FFFFFF;
            }}
        """
        self.epsListWidget.setStyleSheet(itemQss)
        self.listWidget.setStyleSheet(itemQss)
        self._RefreshActionButtons()
        self._UpdateCoverShadow()
        if self._rawCoverPixmap is not None and not self._rawCoverPixmap.isNull():
            self._SetRoundedCoverPixmap(self._rawCoverPixmap)

    def _UpdateCoverShadow(self):
        if self._coverShadow is None:
            return
        isDark = Setting.ThemeIndex.autoValue == 1
        if self.picture.property("empty"):
            self._coverShadow.setColor(QColor(0, 0, 0, 0))
        else:
            self._coverShadow.setColor(QColor(0, 0, 0, 115) if isDark else QColor(15, 23, 42, 42))

    def _SetCoverEmptyState(self, isEmpty: bool):
        if self.picture.property("empty") != isEmpty:
            self.picture.setProperty("empty", isEmpty)
            self.picture.style().unpolish(self.picture)
            self.picture.style().polish(self.picture)
        self._UpdateCoverShadow()

    def _RefreshActionButtons(self):
        isDark = Setting.ThemeIndex.autoValue == 1
        iconColor = "#CBD5E1" if isDark else "#475569"
        hoverBg = "#2F3440" if isDark else "#EEF1F5"
        pressedBg = "#232731" if isDark else "#E2E8F0"
        textColor = "#E8ECF2" if isDark else "#1E293B"

        actionBtnQss = f"""
            QToolButton {{
                background-color: transparent;
                color: {textColor};
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                height: 36px;
                min-height: 36px;
            }}
            QToolButton:hover {{
                background-color: {hoverBg};
            }}
            QToolButton:pressed {{
                background-color: {pressedBg};
            }}
        """
        for btn in (
            self.favoriteButton,
            self.localButton,
            self.commentButton,
            self.downloadButton,
            self.uploadButton,
            self.clearButton,
        ):
            btn.setStyleSheet(actionBtnQss)

        self.commentButton.setIcon(RenderSvgIcon("comment", iconColor, 20))
        self.downloadButton.setIcon(RenderSvgIcon("download", iconColor, 20))
        self.uploadButton.setIcon(RenderSvgIcon("cloud_upload", iconColor, 20))
        self.UpdateFavoriteIcon()

    def UpdateFavoriteIcon(self):
        isDark = Setting.ThemeIndex.autoValue == 1
        primary = QtOwner().GetThemeColorList(0)
        iconColor = "#CBD5E1" if isDark else "#475569"
        mutedColor = "#64748B" if isDark else "#94A3B8"
        dangerColor = "#EF4444" if isDark else "#DC2626"

        if getattr(self, "isFavorite", False):
            self.favoriteButton.setIcon(RenderSvgIcon("star_filled", primary, 20))
        else:
            self.favoriteButton.setIcon(RenderSvgIcon("star", iconColor, 20))

        bookId = getattr(self, "bookId", "")
        owner = QtOwner().owner if getattr(QtOwner(), "_owner", None) else None
        localFavView = getattr(owner, "localFavoriteView", None) if owner is not None else None
        if bookId and localFavView is not None and localFavView.IsHave(bookId):
            self.localButton.setIcon(RenderSvgIcon("bookmark_filled", primary, 20))
        else:
            self.localButton.setIcon(RenderSvgIcon("bookmark", iconColor, 20))

        hasCache = False
        if bookId:
            path = os.path.join(Setting.GetCachePath(), "book_new/{}".format(bookId))
            waifuPath = os.path.join(Setting.GetCachePath(), "waifu2x/book/{}".format(bookId))
            hasCache = os.path.isdir(path) or os.path.isdir(waifuPath)
        if hasCache:
            self.clearButton.setIcon(RenderSvgIcon("trash", dangerColor, 20))
        else:
            self.clearButton.setIcon(RenderSvgIcon("trash", mutedColor, 20))

    def Clear(self):
        self.ClearTask()
        self.epsListWidget.clear()

    def OpenMainJmID(self):
        text = self.mainButton.text()
        if text and (re.match('JM\d+', text) or re.match('jm\d+', text)):
            bookId = text.lower().replace("jm", "")
            self.OpenBook(bookId)

    def SwitchCurrent(self, **kwargs):
        self.update()
        bookId = kwargs.get("bookId")
        if bookId:
            self.bookId = str(bookId)
            self.idLabel.setText("JM" +str(self.bookId))
            self.OpenBook(self.bookId)

        bookName = kwargs.get("bookName")
        if bookName:
            self.bookName = bookName
            self.title.setText(bookName)
        pass

    def OpenBook(self, bookId):
        self.commandLinkButton.setVisible(False)
        self.bookId = bookId
        if QtOwner().isOfflineModel:
            self.tabWidget.setCurrentIndex(1)
        else:
            self.tabWidget.setCurrentIndex(0)
        self.setFocus()
        self.Clear()
        self.show()
        QtOwner().ShowLoading()
        self.buyButton.setVisible(False)
        self.AddHttpTask(req.GetBookInfoReq2(self.bookId), self.OpenBookBack)

    def OpenRecommend(self):
        info = BookMgr().GetBook(self.bookId)
        if not info:
            return
        if not info.related_list:
            return
        QtOwner().OpenRecomment(self.bookId, info.related_list)

    def OpenBookBack(self, raw):
        QtOwner().CloseLoading()
        self.ClearTags()
        self.autorList.clear()
        info = BookMgr().GetBook(self.bookId)
        st = raw["st"]
        self.UpdateDownloadEps()
        if info:
            isFavorite = raw.get('isFavorite')
            self.isFavorite = bool(isFavorite)
            assert isinstance(info, BookInfo)
            for author in info.baseInfo.authorList:
                self.autorList.AddItem(author)
            if info.related_list:
                self.commandLinkButton.setVisible(True)

            title = info.baseInfo.title

            if info.pageInfo.pages:
                title += "<font color={}>{}</font>".format(QtOwner().GetThemeColor(), "(" + str(info.pageInfo.pages) + "P)")
            self.title.setText(title)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.likeLabel.setText("{}".format(info.baseInfo.likes))
            self.viewLabel.setText("{}".format(info.baseInfo.views))
            self.title.setFont(font)
            self.idLabel.setText("JM"+str(info.baseInfo.id))
            self.commentNum = info.pageInfo.commentNum
            self.commentButton.setText("({})".format(info.pageInfo.commentNum))
            self.bookName = info.baseInfo.title
            self.description.setPlainText(info.pageInfo.des)
            if info.baseInfo.series_id and str(info.baseInfo.series_id) != str(info.baseInfo.id):
                self.mainButton.setVisible(True)
                self.mainButton.setText("JM"+str(info.baseInfo.series_id))
            else:
                self.mainButton.setVisible(False)
            if info.baseInfo.addTime:
                dt_object = datetime.fromtimestamp(info.baseInfo.addTime)
                date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                self.lastUpTime.setText(date_string)
            # for name in info.categories:
            #     self.categoriesList.AddItem(name)
            for name in info.baseInfo.tagList:
                self.AddTags(name)
            for name in info.baseInfo.workList:
                self.AddTags(Str.GetStr(Str.WorksName)  + "#"+name)
            for name in info.baseInfo.actorList:
                self.AddTags(Str.GetStr(Str.ActorsName)  + "#"+name)
            # self.starButton.setText(str(info.totalLikes))
            # self.views.setText(str(info.totalViews))
            # self.isFavorite = info.isFavourite
            # self.isLike = info.isLiked
            self.UpdateFavoriteIcon()
            self._rawCoverPixmap = None
            self.picture.setPixmap(QPixmap())
            self._SetCoverEmptyState(True)
            self.picture.setText(Str.GetStr(Str.LoadingPicture))
            self.url = info.baseInfo.coverUrl
            self.path = ToolUtil.GetRealPath(self.bookId, "cover")
            # dayStr = ToolUtil.GetUpdateStr(info.pageInfo.createDate)
            # self.updateTick.setText(str(dayStr) + Str.GetStr(Str.Updated))
            otherParams = {"bookId": self.bookId, "type": "cover"}
            if config.IsLoadingPicture:
                if QtOwner().isOfflineModel:
                    self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture, otherParams=otherParams)
                else:
                    self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture, isReload=True, otherParams=otherParams)
            self.UpdateEpsData()
            self.lastEpsId = -1
            self.LoadHistory()
            self.UpdateBuyButtong(info)
        else:
            if QtOwner().isOfflineModel:
                self.path = ToolUtil.GetRealPath(self.bookId, "cover")
                self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture)
            # QtWidgets.QMessageBox.information(self, '加载失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().CheckShowMsg(raw)

        # if st == Status.UnderReviewBook:
        #     QtOwner().ShowError(Str.GetStr(st))

        return

    def UpdateBuyButtong(self, info):
        self.buyButton.setVisible(False)
        if info.baseInfo.price > 0 and not info.baseInfo.purchased:
            self.buyButton.setVisible(True)
            self.buyButton.setText(Str.GetStr(Str.BuyWithJcoin).format(info.baseInfo.price))

    def DoBuyBook(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetBuyComicsReq2(self.bookId), callBack=self.DoBuyBookBack)

    def DoBuyBookBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        data = raw.get("data", {})
        if data.get("status") == "ok":
            self.buyButton.setVisible(False)
        if data.get("msg"):
            QtOwner().ShowMsg(data.get("msg"))

        return

    def UpdateDownloadEps(self):
        info = QtOwner().downloadView.GetDownloadInfo(self.bookId)
        self.listWidget.clear()
        if info:
            from view.download.download_item import DownloadItem
            from view.download.download_item import DownloadEpsItem
            assert isinstance(info, DownloadItem)
            # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
            maxEpsId = max(info.epsIds)
            for i in range(0, maxEpsId+1):
                epsInfo = info.epsInfo.get(i)

                item = QListWidgetItem(self.listWidget)
                if not epsInfo:
                    label = QLabel(str(i + 1) + "-" + Str.GetStr(Str.NotDownload))
                    item.setToolTip(Str.GetStr(Str.NotDownload))
                else:
                    assert isinstance(epsInfo, DownloadEpsItem)
                    label = QLabel(str(i + 1) + "-" + epsInfo.epsTitle)
                    item.setToolTip(epsInfo.epsTitle)

                label.setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setPointSize(11)
                font.setWeight(QFont.Weight.DemiBold)
                label.setFont(font)
                # label.setWordWrap(True)
                # label.setContentsMargins(20, 10, 20, 10)
                # if index in downloadIds:
                #     item.setBackground(QColor(18, 161, 130))
                # else:
                #     item.setBackground(QColor(0, 0, 0, 0))
                item.setSizeHint(label.sizeHint() + QSize(20, 20))
                item.index = i
                self.listWidget.setItemWidget(item, label)
        return
    # def LoadingPictureComplete(self, data, status):
    #     if status == Status.Ok:
    #         self.userIconData = data
    #         self.user_icon.SetPicture(data)

    def ClearTags(self):
        while 1:
            child = self.flowLayout.takeAt(0)
            if not child:
                break
            if child.widget():
                child.widget().setParent(None)
            del child
        return

    def AddTags(self, name):
        box = QPushButton(name)
        box.setCursor(Qt.PointingHandCursor)
        # box.setMinimumWidth(160)
        # self.allBox[text] = box
        box.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        box.customContextMenuRequested.connect(self.CopyClickTagsItem)
        box.clicked.connect(self.ClickTagsItem)
        self.flowLayout.addWidget(box)
        return

    def _SetRoundedCoverPixmap(self, rawPixmap: QtGui.QPixmap):
        self._rawCoverPixmap = rawPixmap
        if rawPixmap.isNull():
            self.picture.setPixmap(QPixmap())
            self._SetCoverEmptyState(True)
            return
        isDark = Setting.ThemeIndex.autoValue == 1
        radio = self.devicePixelRatio()
        maxW = max(120, min(self.picture.width(), self.picture.maximumWidth()) - 12)
        maxH = max(120, min(self.picture.height(), self.picture.maximumHeight()) - 12)
        scaled = rawPixmap.scaled(
            int(maxW * radio),
            int(maxH * radio),
            QtCore.Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        scaled.setDevicePixelRatio(radio)
        w = max(1, int(round(scaled.width() / radio)))
        h = max(1, int(round(scaled.height() / radio)))
        rounded = QtGui.QPixmap(int(w * radio), int(h * radio))
        rounded.setDevicePixelRatio(radio)
        rounded.fill(Qt.transparent)
        painter = QtGui.QPainter(rounded)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        clipPath = QtGui.QPainterPath()
        clipPath.addRoundedRect(QtCore.QRectF(0, 0, w, h), 10.0, 10.0)
        painter.save()
        painter.setClipPath(clipPath)
        painter.drawPixmap(0, 0, scaled)
        painter.restore()

        # 紧贴封面真实边缘的 1px 细腻描边，避免留白黑边/白边
        borderColor = QColor(255, 255, 255, 32) if isDark else QColor(15, 23, 42, 26)
        painter.setPen(QtGui.QPen(borderColor, 1.0))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, w - 1.0, h - 1.0), 9.5, 9.5)
        painter.end()

        self._SetCoverEmptyState(False)
        self.picture.setPixmap(rounded)

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            self._SetRoundedCoverPixmap(pic)
            if Setting.CoverIsOpenWaifu.value:
                w, h, mat, _ = ToolUtil.GetPictureSize(self.pictureData)
                if max(w, h) <= Setting.CoverMaxNum.value:
                    model = ToolUtil.GetModelByIndex(Setting.CoverLookModelName.value, Setting.CoverLookScale.value, mat)
                    self.AddConvertTask(self.path, self.pictureData, model, self.Waifu2xPictureBack)
        else:
            self._rawCoverPixmap = None
            self.picture.setPixmap(QPixmap())
            self._SetCoverEmptyState(True)
            self.picture.setText(Str.GetStr(Str.LoadingFail))
        return

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        if data:
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            self._SetRoundedCoverPixmap(pic)
        return

    def GetEpsBack(self, raw):
        st = raw["st"]
        if st == Status.Ok:
            self.UpdateEpsData()
            self.lastEpsId = -1
            self.LoadHistory()
            return
        else:
            QtOwner().CheckShowMsg(raw)
            # QtOwner().ShowError(Str.GetStr(Str.ChapterLoadFail) + ", {}".format(Str.GetStr(st)))
        return

    def UpdateEpsData(self):
        self.epsListWidget.clear()
        info = BookMgr().GetBook(self.bookId)
        if not info:
            return
        assert isinstance(info, BookInfo)
        self.startRead.setEnabled(True)
        # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
        for index in sorted(info.pageInfo.epsInfo.keys()):
            epsInfo = info.pageInfo.epsInfo.get(index)
            label = QLabel(epsInfo.title)
            label.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(11)
            font.setWeight(QFont.Weight.DemiBold)
            label.setFont(font)
            # label.setWordWrap(True)
            # label.setContentsMargins(20, 10, 20, 10)
            item = QListWidgetItem(self.epsListWidget)
            # if index in downloadIds:
            #     item.setBackground(QColor(18, 161, 130))
            # else:
            #     item.setBackground(QColor(0, 0, 0, 0))
            item.setSizeHint(label.sizeHint() + QSize(20, 20))
            item.setToolTip(epsInfo.title)
            item.index = index
            self.epsListWidget.setItemWidget(item, label)

        return

    # def ChageMaxNum(self):
    #     maxHeight = self.epsListWidget.verticalScrollBar().maximum()
    #     print(maxHeight)
    #     self.epsListWidget.setMinimumHeight(maxHeight)

    def AddDownload(self):
        QtOwner().OpenEpsInfo(self.bookId)
        return

    def AddFavorite(self):
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.AddAndDelFavoritesReq2(self.bookId), self.AddFavoriteBack)

    def ClearCache(self):
        if not self.bookId:
            return
        path = os.path.join(Setting.GetCachePath(), "book_new/{}".format(self.bookId))
        waifuPath = os.path.join(Setting.GetCachePath(), "waifu2x/book/{}".format(self.bookId))
        isClear = QMessageBox.information(self, Str.GetStr(Str.ClearCache), Str.GetStr(Str.ConfirmClearBookCache).format(path, waifuPath), QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isClear == QtWidgets.QMessageBox.Yes:
            if not Setting.SavePath.value:
                return
            if os.path.isdir(path):
                shutil.rmtree(path, True)
            if os.path.isdir(waifuPath):
                shutil.rmtree(waifuPath, True)
        self.UpdateFavoriteIcon()
        TaskCache().ClearMemData(self.bookId)

    def DelFavoriteBack(self, raw):
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        st = raw["st"]
        if st == Status.Ok:
            self.isFavorite = False
            self.UpdateFavoriteIcon()
            QtOwner().CheckShowMsg(raw)
        else:
            QtOwner().CheckShowMsg(raw)

    def AddFavoriteBack(self, raw):
        QtOwner().CloseLoading()
        st = raw["st"]
        if st == Status.Ok:
            self.isFavorite = not self.isFavorite
            self.UpdateFavoriteIcon()
            if self.isFavorite:
                QtOwner().OpenFavoriteFold(self.bookId)
        QtOwner().CheckShowMsg(raw)

    def AddLocalFavorite(self):
        if QtOwner().localFavoriteView.IsHave(self.bookId):
            QtOwner().localFavoriteView.DelFavorites(self.bookId)
            QtOwner().ShowMsg(Str.GetStr(Str.DelFavoriteSuc))
            self.UpdateFavoriteIcon()
        else:
            bookInfo = BookMgr().GetBook(self.bookId)
            if bookInfo:
                QtOwner().localFavoriteView.AddFavorites(bookInfo)
                QtOwner().ShowMsg(Str.GetStr(Str.AddFavoriteSuc))
                self.UpdateFavoriteIcon()
                QtOwner().OpenLocalFavoriteFold(self.bookId)

    def OpenComment(self):
        QtOwner().OpenComment(self.bookId)

    def OpenReadImg(self, modelIndex):
        index = modelIndex.row()
        item = self.epsListWidget.item(index)
        if not item:
            return
        book = BookMgr().GetBook(self.bookId)
        if not book:
            return
        self.OpenReadIndex(item.index)

    def OpenReadImg2(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, item.index):
            QtOwner().ShowError(Str.GetStr(Str.NotDownload))
            return
        self.OpenReadIndex(index, isOffline=True)

    def OpenReadIndex(self, epsId, pageIndex=-1, isOffline=False):
        QtOwner().OpenReadView(self.bookId, epsId, pageIndex=pageIndex, isOffline=isOffline)
        # self.stackedWidget.setCurrentIndex(1)

    def StartRead(self):
        if self.lastEpsId >= 0:
            self.OpenReadIndex(self.lastEpsId, self.lastIndex)
        else:
            self.OpenReadIndex(0)
        return

    def StartRead2(self):
        if self.lastEpsId >= 0:
            if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, self.lastEpsId):
                QtOwner().ShowError(Str.GetStr(Str.NotDownload))
                return
            self.OpenReadIndex(self.lastEpsId, self.lastIndex, isOffline=True)
        else:
            if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, 0):
                QtOwner().ShowError(Str.GetStr(Str.NotDownload))
                return
            self.OpenReadIndex(0, isOffline=True)
        return

    def LoadHistory(self):
        info = QtOwner().historyView.GetHistory(self.bookId)
        if not info:
            self.startRead.setText(Str.GetStr(Str.LookFirst))
            self.readOffline.setText(Str.GetStr(Str.LookFirst))
            return
        if self.lastEpsId == info.epsId:
            self.lastIndex = info.picIndex
            self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
            self.readOffline.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(
                info.picIndex + 1) + Str.GetStr(Str.Page))
            return
        item = self.epsListWidget.item(info.epsId)
        if not item:
            return
        item.setBackground(QColor(238, 162, 164))
        self.lastEpsId = info.epsId
        self.lastIndex = info.picIndex
        self.startRead.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))
        self.readOffline.setText(Str.GetStr(Str.LastLook) + str(self.lastEpsId + 1) + Str.GetStr(Str.Chapter) + str(info.picIndex + 1) + Str.GetStr(Str.Page))

    def ClickAutorItem(self, modelIndex):
        index = modelIndex.row()
        item = self.autorList.item(index)
        if not item:
            return
        widget = self.autorList.itemWidget(item)
        text = widget.text()
        QtOwner().OpenSearch2Author(text)
        return

    def ClickTagsItem(self):
        text = self.sender().text()
        # QtOwner().owner.searchForm.SearchTags(text)
        texts = text.split("#", 2)
        if len(texts)>1:
            newText = texts[1]
        else:
            newText = texts[0]
        QtOwner().OpenSearch2(newText)
        return

    def CopyClickTagsItem(self):
        text = self.sender().text()
        QtOwner().CopyText(text)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if obj == self.picture:
                    if self.pictureData:
                        QtOwner().OpenWaifu2xTool(self.pictureData)
                # elif obj == self.user_name:
                #     QtOwner().owner.searchForm.SearchCreator(self.user_name.text())
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def keyPressEvent(self, ev):
        key = ev.key()
        if Qt.Key_Escape == key:
            self.close()
        return super(self.__class__, self).keyPressEvent(ev)

    # def CopyClickCategoriesItem(self, pos):
    #     index = self.categoriesList.indexAt(pos)
    #     item = self.categoriesList.itemFromIndex(index)
    #     if index.isValid() and item:
    #         text = item.text()
    #         QtOwner().CopyText(text)

    def CopyClickAutorItem(self, pos):
        index = self.autorList.indexAt(pos)
        item = self.autorList.itemFromIndex(index)
        if index.isValid() and item:
            widget = self.autorList.itemWidget(item)
            text = widget.text()
            QtOwner().CopyText(text)

    def ShowMenu(self):
        if not self.bookName:
            return
        if not self.bookId:
            return
        toolMenu = QMenu(self.uploadButton)
        toolMenu.clear()
        title = self.bookName
        if not title:
            return
        nasDict = QtOwner().owner.nasView.nasDict
        action = toolMenu.addAction(Str.GetStr(Str.NetNas))
        action.setEnabled(False)

        if not nasDict:
            action = toolMenu.addAction(Str.GetStr(Str.CvSpace))
            action.setEnabled(False)
        else:
            for k, v in nasDict.items():
                action = toolMenu.addAction(v.showTitle)
                if QtOwner().nasView.IsInUpload(k, self.bookId):
                    action.setEnabled(False)
                action.triggered.connect(partial(self.NasUploadHandler, k, self.bookId))
        toolMenu.exec(QCursor().pos())

    def NasUploadHandler(self, nasId, bookId):
        QtOwner().nasView.AddNasUpload(nasId, bookId)
        return
