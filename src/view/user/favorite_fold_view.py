from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QLabel

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_favorite_fold import Ui_FavoriteFold
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.book import FavoriteInfo
from PySide6.QtCore import Signal

from tools.str import Str


class FavoriteFoldItem(QWidget):
    itemDeleted = Signal(QListWidgetItem)

    def __init__(self, text, item, isDel, *args, **kwargs):
        super(FavoriteFoldItem, self).__init__(*args, **kwargs)
        self._item = item  # 保留list item的对象引用
        self.fid = ""
        self.text = text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # self.lineEdit = QLineEdit(text, self)
        if isDel:
            self.lineEdit = QLabel(text, self)
            self.pushButton = QPushButton("x", self, clicked=self._DoDeleteItem)
            self.SetEditEnable(False)
        else:
            self.lineEdit = QLineEdit(text, self)
            self.lineEdit.setStyleSheet("border: 2px solid #ff4081")
            self.lineEdit.setMinimumSize(100, 40)
            self.pushButton = QPushButton(Str.GetStr(Str.Save), self, clicked=self._DoDeleteItem)
            self.SetEditEnable(True)

        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)

    def SetEditEnable(self, isEnable):
        if isEnable:
            # self.lineEdit.setEnabled(True)
            # self.lineEdit.setFocusPolicy(Qt.ClickFocus)
            self.pushButton.setVisible(True)
        else:
            # self.lineEdit.setEnabled(False)
            # self.lineEdit.setFocusPolicy(Qt.NoFocus)
            self.pushButton.setVisible(False)

    def _DoDeleteItem(self):
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)


class FavoriteFoldView(BaseMaskDialog, Ui_FavoriteFold, QtTaskBase):
    MoveOkBack = Signal()
    FoldChange = Signal()

    def __init__(self, parent=None, bookId="", fid=""):
        BaseMaskDialog.__init__(self, parent)
        QtTaskBase.__init__(self)
        self.setupUi(self.widget)
        self.setMinimumSize(400, 500)
        # self.listWidget.setFlow(self.listWidget.LeftToRight)
        self.listWidget.setSelectionMode(self.listWidget.SelectionMode.SingleSelection)
        self.widget.adjustSize()
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self._MoveBookToFold)
        self.editButton.clicked.connect(self.SwitchEdit)
        self.isEditMode = False
        self.bookId = bookId
        self.fid = fid
        self.isFoldChange = False
        if not self.bookId:
            self.saveButton.hide()

        self.Init()
        self.listWidget.setFocus()

    def Init(self):
        self.listWidget.clear()
        self.AddHttpTask(req.GetFavoritesReq2(), self.InitBack)
        return

    def InitBack(self, raw):
        if raw["st"] == Status.Ok:
            f = raw["favorite"]
            assert isinstance(f, FavoriteInfo)
            self.AddAllItem()
            for name, fid in f.fold.items():
                self.AddItem(name, fid)
            if self.isEditMode:
                self._SwitchEdit()
        return

    def SwitchEdit(self):
        self.isEditMode = not self.isEditMode
        self._SwitchEdit()

    def _SwitchEdit(self):
        if self.isEditMode:
            self.saveButton.hide()
            self.AddEditItem("")
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                w = self.listWidget.itemWidget(item)
                if i == 0:
                    continue
                w.SetEditEnable(True)
                # item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        else:
            if self.bookId:
                self.saveButton.setVisible(True)

            # 删除最后一个
            row = self.listWidget.count() - 1
            item = self.listWidget.takeItem(row)
            # 删除widget
            self.listWidget.removeItemWidget(item)
            del item
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                w = self.listWidget.itemWidget(item)
                w.SetEditEnable(False)
                # item.setFlags(item.flags() & Qt.ItemIsSelectable)

                if w.fid == self.fid:
                    item.setSelected(True)

        return

    def AddItem(self, name, fid):
        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(name, item, True, self.listWidget)
        # 绑定删除信号
        widget.itemDeleted.connect(self._DoDeleteItem)
        widget.fid = fid
        item.setSizeHint(widget.sizeHint())
        self.listWidget.setItemWidget(item, widget)
        if widget.fid == self.fid:
            item.setSelected(True)
        return

    def AddEditItem(self, name):
        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(name, item, False, self.listWidget)
        # 绑定删除信号
        item.setSizeHint(widget.sizeHint()+QSize(0, 20))
        widget.itemDeleted.connect(self._DoAddItem)
        self.listWidget.setItemWidget(item, widget)
        return

    def AddAllItem(self):
        item = QListWidgetItem(self.listWidget)
        widget = FavoriteFoldItem(Str.GetStr(Str.All), item, True, self.listWidget)
        item.setSizeHint(widget.sizeHint())
        self.listWidget.setItemWidget(item, widget)
        if widget.fid == self.fid:
            item.setSelected(True)

    def _DoAddItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        QtOwner().ShowLoading()
        self.AddHttpTask(req.AddFavoritesFoldReq2(w.lineEdit.text()), self._DoAddItemBack, row)

    def _DoAddItemBack(self, raw, row):
        QtOwner().CloseLoading()
        if raw["st"] == Status.Ok:
            self.Init()
            self.isFoldChange = True
        QtOwner().CheckShowMsg(raw)

    def _DoDeleteItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        QtOwner().ShowLoading()
        self.AddHttpTask(req.DelFavoritesFoldReq2(w.fid), self._DoDeleteItemBack, row)

    def _DoDeleteItemBack(self, raw, row):
        QtOwner().CloseLoading()
        if raw["st"] == Status.Ok:
            # 删除item
            item = self.listWidget.takeItem(row)
            # 删除widget
            self.listWidget.removeItemWidget(item)
            del item
            self.isFoldChange = True
        QtOwner().CheckShowMsg(raw)

    def _MoveBookToFold(self):
        fid = ""
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            w = self.listWidget.itemWidget(item)
            if item.isSelected():
                fid = w.fid
        QtOwner().ShowLoading()
        self.AddHttpTask(req.MoveFavoritesFoldReq2(self.bookId, fid), self._MoveBookToFoldBack)

    def _MoveBookToFoldBack(self, raw):
        QtOwner().CloseLoading()
        QtOwner().CheckShowMsg(raw)
        if raw["st"] == Status.Ok:
            self.close()
            self.MoveOkBack.emit()

    def closeEvent(self, arg__1) -> None:
        self.closed.emit()
        self.Close()
        arg__1.accept()

    def Close(self):
        if self.isFoldChange:
            self.FoldChange.emit()
