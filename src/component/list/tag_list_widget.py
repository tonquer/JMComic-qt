from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QListWidgetItem, QLabel, QAbstractItemView, QListWidget

from component.list.base_list_widget import BaseListWidget
from component.scroll.smooth_scroll_bar import SmoothScrollBar
from config.setting import Setting
from qt_owner import QtOwner


class TagListWidget(BaseListWidget):
    def __init__(self, parent):
        BaseListWidget.__init__(self, parent)

        self.setViewMode(QListWidget.ListMode)
        self.setFlow(QListWidget.LeftToRight)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSpacing(0)
        self.setMaximumHeight(44)
        self.setFocusPolicy(Qt.NoFocus)
        self.hScrollBar = SmoothScrollBar()
        self.hScrollBar.setOrientation(Qt.Horizontal)
        self.setHorizontalScrollBar(self.hScrollBar)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalScrollBar().setSingleStep(30)
        self.itemSelectionChanged.connect(self.UpdateItemStyles)

    def wheelEvent(self, arg__1) -> None:
        if not self.wheelStatus:
            return
        if -arg__1.angleDelta().y() > 0 and abs(self.horizontalScrollBar().value() - self.horizontalScrollBar().maximum()) <= 2:
            arg__1.ignore()
            return
        elif -arg__1.angleDelta().y() < 0 and abs(self.horizontalScrollBar().value() - self.horizontalScrollBar().minimum()) <= 2:
            arg__1.ignore()
            return
        if Setting.IsGrabGesture.value:
            return QListWidget.wheelEvent(self, arg__1)
            # return
        self.hScrollBar.ScrollValue(-arg__1.angleDelta().y())

    def UpdateItemStyles(self):
        accentText = QtOwner().GetThemeColorList(2)
        fm = QFontMetrics(self.font())
        item_h = max(30, fm.height() + 12)
        self.setFixedHeight(item_h + 4)
        for i in range(self.count()):
            item = self.item(i)
            if not item:
                continue
            label = self.itemWidget(item)
            if label is None:
                continue
            if item.isSelected():
                label.setStyleSheet("color: #FFFFFF; font-weight: 600; background: transparent; padding: 0px;")
            else:
                label.setStyleSheet(f"color: {accentText}; background: transparent; padding: 0px;")
            text_w = fm.horizontalAdvance(label.text())
            item.setSizeHint(QSize(max(44, text_w + 32), item_h))

    def AddItem(self, name, isSelectable=False):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        label.setStyleSheet(f"color: {QtOwner().GetThemeColorList(2)}; background: transparent; padding: 0px;")

        item = QListWidgetItem(self)
        item.setTextAlignment(Qt.AlignCenter)
        fm = QFontMetrics(self.font())

        width = fm.horizontalAdvance(name)
        item_h = max(30, fm.height() + 12)
        self.setFixedHeight(item_h + 4)
        self.setItemWidget(item, label)
        item.setSizeHint(QSize(max(44, width + 32), item_h))
        if not isSelectable:
            item.setFlags(item.flags() & (~Qt.ItemIsSelectable))

        self.addItem(item)
        return item