from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QLabel, QListWidgetItem, QFrame, QListWidget, QAbstractItemView

from interface.ui_book_eps import Ui_BookEps
from qt_owner import QtOwner
from server import req
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.status import Status
from tools.str import Str


class BookEpsView(QtWidgets.QWidget, Ui_BookEps, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_BookEps.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.listWidget.setFlow(QListWidget.LeftToRight)
        self.listWidget.setWrapping(True)
        self.listWidget.setFrameShape(QFrame.NoFrame)
        self.listWidget.setResizeMode(QListWidget.Adjust)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setSpacing(6)
        self.bookId = ""
        self.selectButton.clicked.connect(self.SelectAll)
        self.cancleButton.clicked.connect(self.CancleSelect)
        self.downloadButton.clicked.connect(self.StartDownload)

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        if bookId:
            self.OpenEpsInfo(bookId)
        pass

    def OpenEpsInfo(self, bookId):
        QtOwner().ShowLoading()
        self.bookId = bookId
        self.listWidget.clear()
        self.AddHttpTask(req.GetBookInfoReq2(self.bookId), self.OpenEpsInfoBack)

    def OpenEpsInfoBack(self, raw):
        QtOwner().CloseLoading()
        self.listWidget.clear()
        st = raw["st"]
        if st == Status.Ok:
            self.UpdateEpsInfo()
        return

    def UpdateEpsInfo(self):
        self.listWidget.clear()
        info = BookMgr().GetBook(self.bookId)
        if not info:
            return
        downloadEpsId = QtOwner().downloadView.GetDownloadEpsId(self.bookId)
        for index, epsInfo in info.pageInfo.epsInfo.items():
            label = QLabel(str(index + 1) + "-" + epsInfo.title)
            label.setAlignment(Qt.AlignCenter)
            # label.setStyleSheet("color: rgb(196, 95, 125);")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            label.setFont(font)
            # label.setWordWrap(True)
            # label.setContentsMargins(20, 10, 20, 10)
            item = QListWidgetItem(self.listWidget)
            item.setSizeHint(label.sizeHint() + QSize(20, 20))
            item.setToolTip(epsInfo.title)
            item.index = index

            if index in downloadEpsId:
                item.setSelected(True)
            else:
                item.setSelected(False)
            self.listWidget.setItemWidget(item, label)

    def SelectAll(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setSelected(True)
            # item.setCheckState(Qt.CheckState.Checked)
            # if item.background().color() == self.greed:
            #     continue
            # item.setBackground(self.blue)
        return

    def CancleSelect(self):
        downloadEpsId = QtOwner().downloadView.GetDownloadEpsId(self.bookId)
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.setSelected(False)
            if i in downloadEpsId:
                item.setSelected(True)
            else:
                item.setSelected(False)

            # item.setCheckState(Qt.CheckState.Unchecked)
            # if item.background().color() == self.greed:
            #     continue
            # item.setBackground(self.white)
        return

    def StartDownload(self):
        downloadIds = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.isSelected():
                downloadIds.append(item.index)

            # if item.background().color() == self.blue:
            #     downloadIds.append(i)
        if not downloadIds:
            return
        QtOwner().downloadView.AddDownload(self.bookId, downloadIds)
        QtOwner().ShowMsg(Str.GetStr(Str.AddDownload))
        self.UpdateEpsInfo()
        return
