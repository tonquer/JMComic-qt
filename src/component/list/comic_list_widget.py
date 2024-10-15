from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QListWidgetItem, QMenu, QApplication, QFrame, QListWidget

from component.list.base_list_widget import BaseListWidget
from component.widget.comic_item_widget import ComicItemWidget
from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class ComicListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)

        self.setFrameShape(QFrame.NoFrame)  # 无边框
        self.setFlow(QListWidget.LeftToRight)  # 从左到右
        self.setWrapping(True)
        self.setResizeMode(QListWidget.Adjust)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.itemClicked.connect(self.SelectItem)
        self.isDelMenu = False
        self.isMoveMenu = False
        self.isGame = False
        self.isLocal = False
        self.isLocalEps = False
        self.openMenu = False

    def SelectMenuBook(self, pos):
        index = self.indexAt(pos)
        widget = self.indexWidget(index)
        if index.isValid() and widget:
            assert isinstance(widget, ComicItemWidget)
            popMenu = QMenu(self)

            if not self.isLocal:
                action = popMenu.addAction(Str.GetStr(Str.Open))
                action.triggered.connect(partial(self.OpenBookInfoHandler, index))

            action = popMenu.addAction(Str.GetStr(Str.LookCover))
            action.triggered.connect(partial(self.OpenPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.ReDownloadCover))
            action.triggered.connect(partial(self.ReDownloadPicture, index))
            if config.CanWaifu2x and widget.picData:
                if not widget.isWaifu2x:
                    action = popMenu.addAction(Str.GetStr(Str.Waifu2xConvert))
                    action.triggered.connect(partial(self.Waifu2xPicture, index))
                    if widget.isWaifu2xLoading or not config.CanWaifu2x:
                        action.setEnabled(False)
                else:
                    action = popMenu.addAction(Str.GetStr(Str.DelWaifu2xConvert))
                    action.triggered.connect(partial(self.CancleWaifu2xPicture, index))
            action = popMenu.addAction(Str.GetStr(Str.CopyTitle))
            action.triggered.connect(partial(self.CopyHandler, index))

            if not self.isLocal:
                action = popMenu.addAction(Str.GetStr(Str.Download))
                action.triggered.connect(partial(self.DownloadHandler, index))
                nas = QMenu(Str.GetStr(Str.NetNas))
                nasDict = QtOwner().owner.nasView.nasDict
                if not nasDict:
                    action = nas.addAction(Str.GetStr(Str.CvSpace))
                    action.setEnabled(False)
                else:
                    for k, v in nasDict.items():
                        action = nas.addAction(v.title)
                        if QtOwner().nasView.IsInUpload(k, widget.id):
                            action.setEnabled(False)
                        action.triggered.connect(partial(self.NasUploadHandler, k, index))
                popMenu.addMenu(nas)

                # if not self.isGame:
                #     action = popMenu.addAction(Str.GetStr(Str.DownloadAll))
                #     action.triggered.connect(self.OpenBookDownloadAll)

            if self.isDelMenu:
                action = popMenu.addAction(Str.GetStr(Str.Delete))
                action.triggered.connect(partial(self.DelHandler, index))
            if self.isMoveMenu:
                action = popMenu.addAction(Str.GetStr(Str.Move))
                action.triggered.connect(partial(self.MoveHandler, index))
            if self.openMenu:
                action = popMenu.addAction(Str.GetStr(Str.OpenDir))
                action.triggered.connect(partial(self.OpenDirHandler, index))
            popMenu.exec_(QCursor.pos())
        return

    def AddBookItemByBook(self, v, isShowHistory=False):
        from tools.book import BookInfo
        assert isinstance(v, BookInfo)
        title = v.baseInfo.title
        url = v.baseInfo.coverUrl
        _id = v.baseInfo.id
        categories = ",".join(v.baseInfo.category)
        self.AddBookItem(_id, title, categories, url)

    def AddBookByLocal(self, v, category=""):
        from task.task_local import LocalData
        assert isinstance(v, LocalData)
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.NoFocus)
        widget.id = v.id
        title = v.title
        widget.index = index
        widget.title = v.title
        widget.picNum = v.picCnt
        widget.url = v.file
        if len(v.eps) > 0:
            fontColor = "<font color=#d5577c>{}</font>".format("(" + str(len(v.eps)) + "E)")
        else:
            fontColor = "<font color=#d5577c>{}</font>".format("(" + str(v.picCnt) + "P)")
        if v.lastReadTime:
            categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.lastReadTime), Str.GetStr(Str.Looked))

            widget.timeLabel.setText(categories)
        else:
            widget.timeLabel.setVisible(False)
            widget.starButton.setVisible(False)

        widget.categoryLabel.setVisible(False)
        if category:
            widget.categoryLabel.setText(category)
            widget.categoryLabel.setVisible(True)

        widget.SetTitle(title, fontColor)
        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)

    def AddBookItemByHistory(self, v):
        _id = v.bookId
        title = v.name
        path = v.path
        url = v.url
        categories = "{} {}".format(ToolUtil.GetUpdateStrByTick(v.tick), Str.GetStr(Str.Looked))
        self.AddBookItem(_id, title, categories, url)

    def AddBookItem(self, _id, title, categoryStr="", url=""):
        index = self.count()
        widget = ComicItemWidget()
        widget.setFocusPolicy(Qt.NoFocus)
        widget.title = title
        widget.category = categoryStr

        widget.id = _id
        widget.url = url
        widget.index = index
        widget.categoryLabel.setText(categoryStr)
        widget.SetTitle(title, "")
        widget.path = ToolUtil.GetRealPath(_id, "cover")
        widget.starButton.setVisible(False)
        widget.timeLabel.setVisible(False)
        # if updated_at:
        #     dayStr = ToolUtil.GetUpdateStr(updated_at)
        #     updateStr = dayStr + Str.GetStr(Str.Update)
        #     widget.timeLabel.setText(updateStr)
        #     widget.timeLabel.setVisible(True)
        # else:
        #     widget.timeLabel.setVisible(False)

        # if likesCount:
        #     widget.starButton.setText(str(likesCount))
        #     widget.starButton.setVisible(True)
        # else:
        #     widget.starButton.setVisible(False)

        # if pagesCount:
        #     title += "<font color=#d5577c>{}</font>".format("("+str(pagesCount)+"P)")
        # if finished:
        #     title += "<font color=#d5577c>{}</font>".format("({})".format(Str.GetStr(Str.ComicFinished)))

        item = QListWidgetItem(self)
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)
        widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
        widget.PicLoad.connect(self.LoadingPicture)
        # if url and config.IsLoadingPicture:
        #     self.AddDownloadTask(url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def DelBookID(self, bookID):
        for row in range(0, self.count()):
            item = self.item(row)
            w = self.itemWidget(item)
            if w.id == bookID:
                item.setHidden(True)
                break

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def LoadingPictureComplete(self, data, status, index):
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPicture(data)
            if Setting.CoverIsOpenWaifu.value:
                item = self.item(index)
                indexModel = self.indexFromItem(item)
                self.Waifu2xPicture(indexModel, True)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            if not widget:
                return
            assert isinstance(widget, ComicItemWidget)
            widget.SetPictureErr()
        return

    def SelectItem(self, item):
        assert isinstance(item, QListWidgetItem)
        widget = self.itemWidget(item)
        assert isinstance(widget, ComicItemWidget)
        if self.isGame:
            QtOwner().OpenGameInfo(widget.id)
        elif self.isLocalEps:
            QtOwner().OpenLocalEpsBook(widget.id)
        elif self.isLocal:
            QtOwner().OpenLocalBook(widget.id)
        else:
            QtOwner().OpenBookInfo(widget.id, widget.GetTitle())
        return

    def OpenBookInfoHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            QtOwner().OpenBookInfo(widget.id, widget.GetTitle())
            return

    def OpenPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            QtOwner().OpenWaifu2xTool(widget.picData)
            return

    def ReDownloadPicture(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            if widget.url and config.IsLoadingPicture:
                widget.SetPicture("")
                item = self.itemFromIndex(index)
                count = self.row(item)
                widget.picLabel.setText(Str.GetStr(Str.LoadingPicture))
                self.AddDownloadTask(widget.url, widget.path, completeCallBack=self.LoadingPictureComplete, backParam=count, isReload=True)
                pass

    def Waifu2xPicture(self, index, isIfSize=False):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget and widget.picData:
            w, h, mat,_ = ToolUtil.GetPictureSize(widget.picData)
            if max(w, h) <= Setting.CoverMaxNum.value or not isIfSize:
                model = ToolUtil.GetModelByIndex(Setting.CoverLookModelName.value, Setting.CoverLookScale.value, mat)
                widget.isWaifu2xLoading = True
                if self.isLocal:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index, noSaveCache=True)
                else:
                    self.AddConvertTask(widget.path, widget.picData, model, self.Waifu2xPictureBack, index)

    def CancleWaifu2xPicture(self, index):
        widget = self.indexWidget(index)
        assert isinstance(widget, ComicItemWidget)
        if widget.isWaifu2x and widget.picData:
            widget.SetPicture(widget.picData)

    def Waifu2xPictureBack(self, data, waifuId, index, tick):
        widget = self.indexWidget(index)
        if data and widget:
            assert isinstance(widget, ComicItemWidget)
            widget.SetWaifu2xData(data)
        return

    def CopyHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            data = widget.GetTitle() + str("\r\n")
            clipboard = QApplication.clipboard()
            data = data.strip("\r\n")
            clipboard.setText(data)
        pass

    def MoveHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            assert isinstance(widget, ComicItemWidget)
            self.MoveCallBack(widget.id)

    def DelHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            self.DelCallBack(widget.id)

    def DelCallBack(self, cfgId):
        return

    def MoveCallBack(self, cfgId):
        return

    def DownloadHandler(self, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().OpenEpsInfo(widget.id)
        pass

    def NasUploadHandler(self, nasId, index):
        widget = self.indexWidget(index)
        if widget:
            QtOwner().nasView.AddNasUpload(nasId, widget.id)
        pass

    def OpenDirHandler(self, index):
        return