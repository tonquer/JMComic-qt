import os
import shutil

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtGui import QColor, QFont, QPixmap, QIcon
from PySide6.QtWidgets import QListWidgetItem, QLabel, QScroller, QPushButton, QMessageBox

from component.layout.flow_layout import FlowLayout
from config.setting import Setting
from interface.ui_book_info import Ui_BookInfo
from qt_owner import QtOwner
from server import req, ToolUtil, config, Status
from task.qt_task import QtTaskBase
from tools.book import BookMgr, BookInfo
from tools.str import Str


class BookInfoView(QtWidgets.QWidget, Ui_BookInfo, QtTaskBase):
    ReloadHistory = Signal()

    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookInfo.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.url = ""
        self.path = ""
        self.bookName = ""
        self.lastEpsId = -1
        self.lastIndex = 0
        self.pictureData = None
        self.isFavorite = False
        self.isLike = False

        self.picture.installEventFilter(self)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.autorList.clicked.connect(self.ClickAutorItem)
        self.autorList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.autorList.customContextMenuRequested.connect(self.CopyClickAutorItem)

        self.idLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.description.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.downloadButton.setIconSize(QSize(50, 50))
        self.favoriteButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.favoriteButton.setIconSize(QSize(50, 50))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setIconSize(QSize(50, 50))
        self.commentButton.clicked.connect(self.OpenComment)
        self.description.adjustSize()
        self.title.adjustSize()

        # self.tagsList.clicked.connect(self.ClickTagsItem)
        # self.tagsList.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tagsList.customContextMenuRequested.connect(self.CopyClickTagsItem)

        self.epsListWidget.setFlow(self.epsListWidget.LeftToRight)
        self.epsListWidget.setWrapping(True)
        self.epsListWidget.setFrameShape(self.epsListWidget.NoFrame)
        self.epsListWidget.setResizeMode(self.epsListWidget.Adjust)

        self.epsListWidget.clicked.connect(self.OpenReadImg)

        self.listWidget.setFlow(self.listWidget.LeftToRight)
        self.listWidget.setWrapping(True)
        self.listWidget.setFrameShape(self.listWidget.NoFrame)
        self.listWidget.setResizeMode(self.listWidget.Adjust)
        self.listWidget.clicked.connect(self.OpenReadImg2)
        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.epsListWidget, QScroller.LeftMouseButtonGesture)
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

    def UpdateFavoriteIcon(self):
        p = QPixmap()
        if self.isFavorite:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like.png"))
        else:
            self.favoriteButton.setIcon(QIcon(":/png/icon/icon_like_off.png"))

        if QtOwner().localFavoriteView.IsHave(self.bookId):
            self.localButton.setIcon(QIcon(":/png/icon/icon_like.png"))
        else:
            self.localButton.setIcon(QIcon(":/png/icon/icon_like_off.png"))
        path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "book/{}".format(self.bookId))
        waifuPath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir), "waifu2x/book/{}".format(self.bookId))
        if os.path.isdir(path) or os.path.isdir(waifuPath):
            self.clearButton.setIcon(QIcon(":/png/icon/clear_on.png"))
        else:
            self.clearButton.setIcon(QIcon(":/png/icon/clear_off.png"))

    def Clear(self):
        self.ClearTask()
        self.epsListWidget.clear()

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        if bookId:
            self.bookId = str(bookId)
            self.idLabel.setText(self.bookId)
            self.OpenBook(self.bookId)

        bookName = kwargs.get("bookName")
        if bookName:
            self.bookName = bookName
            self.title.setText(bookName)
        pass

    def OpenBook(self, bookId):
        self.bookId = bookId
        if QtOwner().isOfflineModel:
            self.tabWidget.setCurrentIndex(1)
        else:
            self.tabWidget.setCurrentIndex(0)
        self.setFocus()
        self.Clear()
        self.show()
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetBookInfoReq2(self.bookId), self.OpenBookBack)

    def OpenBookBack(self, raw):
        QtOwner().CloseLoading()
        self.ClearTags()
        self.autorList.clear()
        info = BookMgr().books.get(self.bookId)
        st = raw["st"]
        self.UpdateDownloadEps()
        if info:
            isFavorite = raw.get('isFavorite')
            self.isFavorite = bool(isFavorite)
            assert isinstance(info, BookInfo)
            for author in info.baseInfo.authorList:
                self.autorList.AddItem(author)
            title = info.baseInfo.title
            if info.pageInfo.pages:
                title += "<font color=#d5577c>{}</font>".format("(" + str(info.pageInfo.pages) + "P)")
            self.title.setText(title)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.likeLabel.setText("{}".format(info.baseInfo.likes))
            self.viewLabel.setText("{}".format(info.baseInfo.views))
            self.title.setFont(font)
            self.idLabel.setText(str(info.baseInfo.id))
            self.commentNum = info.pageInfo.commentNum
            self.commentButton.setText("({})".format(info.pageInfo.commentNum))
            self.bookName = info.baseInfo.title
            self.description.setPlainText(info.pageInfo.des)

            # for name in info.categories:
            #     self.categoriesList.AddItem(name)
            for name in info.baseInfo.tagList:
                self.AddTags(name)
            # self.starButton.setText(str(info.totalLikes))
            # self.views.setText(str(info.totalViews))
            # self.isFavorite = info.isFavourite
            # self.isLike = info.isLiked
            self.UpdateFavoriteIcon()
            self.picture.setText(Str.GetStr(Str.LoadingPicture))
            self.url = info.baseInfo.coverUrl
            self.path = ToolUtil.GetRealPath(self.bookId, "cover")
            # dayStr = ToolUtil.GetUpdateStr(info.pageInfo.createDate)
            # self.updateTick.setText(str(dayStr) + Str.GetStr(Str.Updated))
            if config.IsLoadingPicture:
                if QtOwner().isOfflineModel:
                    self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture)
                else:
                    self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture, isReload=True)
            self.UpdateEpsData()
            self.lastEpsId = -1
            self.LoadHistory()
        else:
            if QtOwner().isOfflineModel:
                self.path = ToolUtil.GetRealPath(self.bookId, "cover")
                self.AddDownloadTask(self.url, self.path, completeCallBack=self.UpdatePicture)
            # QtWidgets.QMessageBox.information(self, '加载失败', msg, QtWidgets.QMessageBox.Yes)
            QtOwner().CheckShowMsg(raw)

        # if st == Status.UnderReviewBook:
        #     QtOwner().ShowError(Str.GetStr(st))

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
                    label = QLabel(str(i + 1) + "-" + "未下载")
                    item.setToolTip("未下载")
                else:
                    assert isinstance(epsInfo, DownloadEpsItem)
                    label = QLabel(str(i + 1) + "-" + epsInfo.epsTitle)
                    item.setToolTip(epsInfo.epsTitle)

                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: rgb(196, 95, 125);")
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                label.setFont(font)
                # label.setWordWrap(True)
                # label.setContentsMargins(20, 10, 20, 10)
                # if index in downloadIds:
                #     item.setBackground(QColor(18, 161, 130))
                # else:
                #     item.setBackground(QColor(0, 0, 0, 0))
                item.setSizeHint(label.sizeHint() + QSize(20, 20))
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
        # box.setMinimumWidth(160)
        # self.allBox[text] = box
        box.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        box.customContextMenuRequested.connect(self.CopyClickTagsItem)
        box.clicked.connect(self.ClickTagsItem)
        self.flowLayout.addWidget(box)
        return

    def UpdatePicture(self, data, status):
        if status == Status.Ok:
            self.pictureData = data
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
            # self.picture.setScaledContents(True)
            if Setting.CoverIsOpenWaifu.value:
                w, h, mat, _ = ToolUtil.GetPictureSize(self.pictureData)
                if max(w, h) <= Setting.CoverMaxNum.value:
                    model = ToolUtil.GetModelByIndex(Setting.CoverLookNoise.value, Setting.CoverLookScale.value, Setting.CoverLookModel.value, mat)
                    self.AddConvertTask(self.path, self.pictureData, model, self.Waifu2xPictureBack)
        else:
            self.picture.setPixmap(QPixmap())
            self.picture.setText(Str.GetStr(Str.LoadingFail))
        return

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        if data:
            pic = QtGui.QPixmap()
            pic.loadFromData(data)
            radio = self.devicePixelRatio()
            pic.setDevicePixelRatio(radio)
            newPic = pic.scaled(self.picture.size()*radio, QtCore.Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.picture.setPixmap(newPic)
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
        info = BookMgr().books.get(self.bookId)
        if not info:
            return
        assert isinstance(info, BookInfo)
        self.startRead.setEnabled(True)
        # downloadIds = QtOwner().owner.downloadForm.GetDownloadCompleteEpsId(self.bookId)
        for index in sorted(info.pageInfo.epsInfo.keys()):
            epsInfo = info.pageInfo.epsInfo.get(index)
            label = QLabel(epsInfo.title)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: rgb(196, 95, 125);")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
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
        self.AddHttpTask(req.AddAndDelFavoritesReq2(self.bookId), self.AddFavoriteBack)

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

    def ClearCache(self):
        isClear = QMessageBox.information(self, '清除缓存', "是否清除本书所有缓存", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if isClear == QtWidgets.QMessageBox.Yes:
            if not Setting.SavePath.value:
                return
            path = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                                "book/{}".format(self.bookId))
            waifuPath = os.path.join(os.path.join(Setting.SavePath.value, config.CachePathDir),
                                     "waifu2x/book/{}".format(self.bookId))
            if os.path.isdir(path):
                shutil.rmtree(path, True)
            if os.path.isdir(waifuPath):
                shutil.rmtree(waifuPath, True)
        self.UpdateFavoriteIcon()

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
        st = raw["st"]
        if st == Status.Ok:
            self.isFavorite = not self.isFavorite
            self.UpdateFavoriteIcon()
            if self.isFavorite:
                QtOwner().OpenFavoriteFold(self.bookId)
        QtOwner().CheckShowMsg(raw)

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
        self.OpenReadIndex(index)

    def OpenReadImg2(self, modelIndex):
        index = modelIndex.row()
        item = self.listWidget.item(index)
        if not item:
            return
        if not QtOwner().downloadView.IsDownloadEpsId(self.bookId, index):
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
        QtOwner().OpenSearch2(text)
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

    def CopyClickCategoriesItem(self, pos):
        index = self.categoriesList.indexAt(pos)
        item = self.categoriesList.itemFromIndex(index)
        if index.isValid() and item:
            text = item.text()
            QtOwner().CopyText(text)

    def CopyClickAutorItem(self, pos):
        index = self.autorList.indexAt(pos)
        item = self.autorList.itemFromIndex(index)
        if index.isValid() and item:
            widget = self.autorList.itemWidget(item)
            text = widget.text()
            QtOwner().CopyText(text)