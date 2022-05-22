from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from component.list.base_list_widget import BaseListWidget
from config import config
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class UserListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)
        self.resize(800, 600)
        # self.setMinimumHeight(400)
        # self.setFrameShape(self.NoFrame)  # 无边框
        self.setFlow(self.TopToBottom)
        # self.setWrapping(True)
        # self.setResizeMode(self.Adjust)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.SelectMenuBook)
        # self.doubleClicked.connect(self.OpenBookInfo)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(self.NoFrame)  # 无边框
        self.setFocusPolicy(Qt.NoFocus)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")

    def AddUserItem(self, info, floor, isSub=False):
        from tools.book import CommentInfo
        assert isinstance(info, CommentInfo)

        from component.widget.comment_item_widget import CommentItemWidget
        index = self.count()
        widget = CommentItemWidget(self)
        widget.index = index
        widget.setFocusPolicy(Qt.NoFocus)
        widget.linkId = info.linkBookId
        if widget.linkId and widget.linkId != "0":
            widget.linkLabel.setText("<u><font color=#d5577c>{}</font></u>".format(info.linkBookName))
            widget.linkLabel.setVisible(True)
        if isSub:
            widget.commentButton.hide()

        widget.id = info.id
        widget.commentLabel.setText(info.content)
        widget.nameLabel.setText(info.name)
        widget.commentButton.setText("({})".format(len(info.subComments)))
        widget.levelLabel.setText("Lv{}".format(info.level))
        widget.titleLabel.setText(" " + info.title + " ")
        widget.url = info.headUrl
        widget.dateLabel.setText(info.date)
        widget.starButton.setText("({})".format(info.like))
        widget.adjustSize()
        item = QListWidgetItem(self)
        item.setSizeHint(widget.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.setItemWidget(item, widget)
        widget.PicLoad.connect(self.LoadingPicture)
        widget.commentList = info.subComments[:]
        # if widget.url and config.IsLoadingPicture:
        #     self.AddDownloadTask(widget.url, "", None, self.LoadingPictureComplete, index, False)

    def LoadingPicture(self, index):
        item = self.item(index)
        widget = self.itemWidget(item)

        from component.widget.comment_item_widget import CommentItemWidget
        assert isinstance(widget, CommentItemWidget)
        if widget.url:
            self.AddDownloadTask(widget.url, completeCallBack=self.LoadingPictureComplete, backParam=index)

    def LoadingPictureComplete(self, data, status, index):

        from component.widget.comment_item_widget import CommentItemWidget
        if status == Status.Ok:
            item = self.item(index)
            widget = self.itemWidget(item)
            assert isinstance(widget, CommentItemWidget)
            widget.SetPicture(data)
            pass
        else:
            item = self.item(index)
            widget = self.itemWidget(item)
            assert isinstance(widget, CommentItemWidget)
            widget.SetPictureErr()
        return