from PySide6.QtCore import QStringListModel, QPoint, QRect, QEvent, QModelIndex
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QWidget, QAbstractItemView, QApplication

from interface.ui_line_edit_help_widget import Ui_LineEditHelp


class TipLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

        self.widget = QWidget(self, Qt.ToolTip)
        self.help = Ui_LineEditHelp()
        self.help.setupUi(self.widget)
        self.help.label.hide()
        self.widget.setFocusProxy(self)

        self.words = []
        self.model = QStringListModel(self)
        self.listView.setModel(self.model)
        self.listView.setFocusPolicy(Qt.NoFocus)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.clicked.connect(self.SetText)

        self.isNotReload = False
        self.isShowSearch = True
        self.isKeyNavigating = False
        self._filterInstalled = False

        self.searchTag1 = "<font color=#232629>"
        self.searchTag2 = "</font>"

    @property
    def listView(self):
        return self.help.listView

    def _InstallFilter(self):
        if self._filterInstalled:
            return
        app = QApplication.instance()
        if app is not None:
            app.installEventFilter(self)
            self._filterInstalled = True

    def _RemoveFilter(self):
        if not self._filterInstalled:
            return
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self)
        self._filterInstalled = False

    def eventFilter(self, watched, event):
        if not self.widget.isHidden():
            evType = event.type()
            if evType == QEvent.MouseButtonPress:
                globalPos = event.globalPosition().toPoint() if hasattr(event, "globalPosition") else event.globalPos()
                inSelf = QRect(self.mapToGlobal(QPoint(0, 0)), self.size()).contains(globalPos)
                inPopup = self.widget.geometry().contains(globalPos)
                if not inSelf and not inPopup:
                    self.HideListView()
                    self.clearFocus()
            elif evType == QEvent.Wheel:
                globalPos = event.globalPosition().toPoint() if hasattr(event, "globalPosition") else event.globalPos()
                if not self.widget.geometry().contains(globalPos):
                    self.HideListView()
            elif evType in (QEvent.WindowDeactivate, QEvent.ApplicationDeactivate):
                self.HideListView()
            elif evType == QEvent.Move and watched is self.window():
                self.HideListView()
        return QLineEdit.eventFilter(self, watched, event)

    def SetWordData(self, data):
        self.words = data
        self.model.setStringList(data)

    def ClearSelect(self):
        self.isKeyNavigating = False
        self.listView.clearSelection()
        self.listView.setCurrentIndex(QModelIndex())

    def SetText(self, index):
        if not index.isValid():
            return
        text = index.data()
        if text is None:
            item = self.model.itemData(index)
            text = item.get(0, "")
        self.setText(str(text))
        self.HideListView()
        if self.hasFocus():
            self.clearFocus()
        else:
            self.editingFinished.emit()
        return

    def keyReleaseEvent(self, ev):
        count = self.listView.model().rowCount()
        currentIndex = self.listView.currentIndex()
        if ev.key() == Qt.Key_Up:
            if count > 0:
                self.isKeyNavigating = True
                if currentIndex.row() < 0:
                    row = 0
                elif currentIndex.row() == 0:
                    row = count - 1
                else:
                    row = currentIndex.row() - 1
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        elif ev.key() == Qt.Key_Down:
            if count > 0:
                self.isKeyNavigating = True
                if currentIndex.row() < 0:
                    row = 0
                else:
                    row = currentIndex.row() + 1 if currentIndex.row() + 1 < count else 0
                index = self.listView.model().index(row, 0)
                self.listView.setCurrentIndex(index)

        elif ev.key() == Qt.Key_Escape:
            self.HideListView()

        elif ev.key() == Qt.Key_Enter or ev.key() == Qt.Key_Return:
            if self.isKeyNavigating and currentIndex.row() >= 0:
                text = currentIndex.data()
                if text is not None:
                    self.setText(str(text))
            self.HideListView()
            self.clearFocus()
        return QLineEdit.keyReleaseEvent(self, ev)

    def Search(self):
        self.HideListView()
        self.clearFocus()
        return

    def clearFocus(self) -> None:
        return QLineEdit.clearFocus(self)

    def mousePressEvent(self, ev):
        QLineEdit.mousePressEvent(self, ev)
        if self.widget.isHidden():
            self.ShowListView()

    def focusInEvent(self, ev):
        self.ClearSelect()
        self.ShowListView()
        return QLineEdit.focusInEvent(self, ev)

    def focusOutEvent(self, ev):
        self.HideListView()
        return QLineEdit.focusOutEvent(self, ev)

    def hideEvent(self, ev):
        self.HideListView()
        return QLineEdit.hideEvent(self, ev)

    def HideListView(self):
        self._RemoveFilter()
        if self.widget.isHidden():
            return
        self.widget.hide()

    def ShowListView(self):
        if not self.widget.isHidden():
            return
        if not self.isShowSearch:
            return
        count = self.model.rowCount()
        if count <= 0:
            return
        rowHeight = self.listView.sizeHintForRow(0)
        if rowHeight <= 0:
            rowHeight = 28
        maxHeight = 260
        win = self.window()
        if win is not None and win.height() > 0:
            maxHeight = min(320, max(160, win.height() // 2))
        height = min(maxHeight, count * rowHeight + 24)
        width = max(self.width(), 180)
        self.widget.resize(width, height)
        self.widget.move(self.mapToGlobal(QPoint(0, self.height())))
        self.widget.show()
        self._InstallFilter()

    def CheckClick(self, pos):
        if self.widget.isHidden():
            return
        self.HideListView()
        self.clearFocus()
        return
