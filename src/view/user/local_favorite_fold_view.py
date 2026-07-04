from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QLineEdit, QPushButton, QLabel

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_favorite_fold import Ui_FavoriteFold
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
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
            self.lineEdit.setStyleSheet(f"border: 2px solid {QtOwner().GetThemeColor()}")
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


class LocalFavoriteFoldView(BaseMaskDialog, Ui_FavoriteFold, QtTaskBase):
    MoveOkBack = Signal()
    FoldChange = Signal()

    def __init__(self, parent=None, bookId=""):
        BaseMaskDialog.__init__(self, parent)
        QtTaskBase.__init__(self)
        self.setupUi(self.widget)
        self.setMinimumSize(400, 500)
        # self.listWidget.setFlow(self.listWidget.LeftToRight)
        self.listWidget.setSelectionMode(self.listWidget.SelectionMode.MultiSelection)
        self.widget.adjustSize()
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self._MoveBookToFold)
        self.editButton.clicked.connect(self.SwitchEdit)
        self.isEditMode = False
        self.bookId = bookId
        self.isFoldChange = False
        if not self.bookId:
            self.saveButton.hide()

        self.fids = set()
        self.Init()
        self.listWidget.setFocus()

    def Init(self):
        self.fids.clear()
        for k, v in QtOwner().localFavoriteView.fidBookList.items():
            if self.bookId in v:
                self.fids.add(k)

        self.listWidget.clear()
        self.AddAllItem()
        for fid, name in QtOwner().localFavoriteView.folderDict.items():
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

                if w.fid in self.fids:
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
        if widget.fid in self.fids:
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
        if widget.fid in self.fids:
            item.setSelected(True)

    def _DoAddItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        # QtOwner().ShowLoading()
        # self.AddHttpTask(req.AddFavoritesFoldReq2(w.lineEdit.text()), self._DoAddItemBack, row)
        text = w.lineEdit.text()
        QtOwner().localFavoriteView.AddFidByName(text)
        self.Init()
        self.isFoldChange = True

    # def _DoAddItemBack(self, raw, row):
    #     QtOwner().CloseLoading()
    #     if raw["st"] == Status.Ok:
    #         self.Init()
    #         self.isFoldChange = True
    #     QtOwner().CheckShowMsg(raw)

    def _DoDeleteItem(self, item):
        # 根据item得到它对应的行数
        row = self.listWidget.indexFromItem(item).row()
        w = self.listWidget.itemWidget(item)
        item = self.listWidget.takeItem(row)
        text = w.lineEdit.text()
        # 删除widget
        self.listWidget.removeItemWidget(item)
        del item
        QtOwner().localFavoriteView.DelFidByName(text)
        self.isFoldChange = True
        self.Init()

    def _MoveBookToFold(self):
        fids = set()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            w = self.listWidget.itemWidget(item)
            if item.isSelected():
                if w.fid:
                    fids.add(w.fid)

        QtOwner().localFavoriteView.UpdateBookFid(self.bookId, fids)
        self.close()
        self.MoveOkBack.emit()

    def closeEvent(self, arg__1) -> None:
        self.closed.emit()
        self.Close()
        arg__1.accept()

    def Close(self):
        if self.isFoldChange:
            self.FoldChange.emit()
