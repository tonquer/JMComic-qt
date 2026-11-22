import os
import re

from PySide6.QtCore import QStringListModel, QPoint
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, \
    QHBoxLayout

from config.setting import Setting
from interface.ui_line_edit_help_widget import Ui_LineEditHelp
from qt_owner import QtOwner
from tools.langconv import Converter
from tools.log import Log


class TipLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        proxy = self.focusPolicy()

        self.widget = QWidget()
        self.help = Ui_LineEditHelp()
        self.help.setupUi(self.widget)
        self.help.label.setText("")

        self.widget.setParent(self, Qt.Popup)
        self.widget.setFocusProxy(self)
        self.widget.setWindowFlags(Qt.ToolTip)
        self.qLabel = QLabel("asdasdasdasd")
        self.hLayout = QHBoxLayout(self.widget)
        self.hLayout.addWidget(self.qLabel)

        self.words = []
        self.model = QStringListModel(self)
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.SetText)

        self.isNotReload = False
        self.isShowSearch = True

        self.searchTag1 = "<font color=#232629>"
        self.searchTag2 = "</font>"

    @property
    def listView(self):
        return self.help.listView

    def SetWordData(self, data):
        self.words = data
        self.model.setStringList(data)

    def SetText(self, index):
        item = self.model.itemData(index)
        text = item.get(0)
        self.setText(text)
        return

    def keyReleaseEvent(self, ev):
        # print(ev.key())
        count = self.listView.model().rowCount()
        currentIndex = self.listView.currentIndex()
        if ev.key() == Qt.Key_Up:
            if count > 0:
                if currentIndex.row() < 0:
                    row = 0
                elif currentIndex.row() == 0:
                    row = count - 1
                else:
                    row = currentIndex.row() - 1 if currentIndex.row() > 0 else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        elif ev.key() == Qt.Key_Down:
            if count > 0:
                if currentIndex.row() < 0:
                    row = 0
                else:
                    row = currentIndex.row() + 1 if currentIndex.row() + 1 < count else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        if ev.key() == Qt.Key_Enter or ev.key() == Qt.Key_Return:
            currentIndex = self.listView.currentIndex()
            if currentIndex.row() >= 0:
                text = currentIndex.data()
                self.setText(text)
            self.HideListView()
            self.clearFocus()
        return QLineEdit.keyReleaseEvent(self, ev)

    def Search(self):
        self.HideListView()
        self.clearFocus()
        return

    def clearFocus(self) -> None:
        return QLineEdit.clearFocus(self)

    def focusInEvent(self, ev):
        # print("in")
        self.ShowListView()
        return QLineEdit.focusInEvent(self, ev)

    def focusOutEvent(self, ev):
        self.widget.hide()
        # print("out")
        return QLineEdit.focusOutEvent(self, ev)

    def HideListView(self):
        if self.widget.isHidden():
            return
        self.widget.hide()
        # self.widget.clear()

    def ShowListView(self):
        if not self.widget.isHidden():
            return
        if not self.isShowSearch:
            return
        self.widget.show()
        pos = self.mapToGlobal(self.pos())
        # print(pos, self.pos(), self.size())
        self.widget.move(pos-self.pos()+QPoint(0, self.height()))
        self.widget.resize(max(500, self.width()), QtOwner().owner.height() // 2)
        # self.ShowInit()

    def CheckClick(self, pos):
        if self.widget.isHidden():
            return
        self.clearFocus()
        return
