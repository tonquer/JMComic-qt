import os
import re

from PySide6.QtCore import QStringListModel, QPoint, QRect, QEvent, Signal
from PySide6.QtGui import Qt, QColor, QPalette
from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, \
    QHBoxLayout, QApplication, QStyle, QStyleOptionViewItem, QStyledItemDelegate

from config.setting import Setting
from interface.ui_line_edit_help_widget import Ui_LineEditHelp
from qt_owner import QtOwner
from tools.langconv import Converter
from tools.log import Log


class HistoryItemDelegate(QStyledItemDelegate):
    """在每条搜索历史的右侧绘制一个 ✕，点击即删除该条记录"""

    DeleteWidth = 26
    DeleteChar = "\u2715"

    deleteClicked = Signal(int)

    @classmethod
    def deleteRect(cls, itemRect):
        return QRect(itemRect.right() - cls.DeleteWidth + 1, itemRect.top(),
                     cls.DeleteWidth, itemRect.height())

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        style = opt.widget.style() if opt.widget else QApplication.style()
        text = opt.text
        # 由自己绘制文字，避免默认绘制铺满整个单元格、和 ✕ 重叠
        opt.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        painter.save()
        textRect = option.rect.adjusted(6, 0, -self.DeleteWidth, 0)
        elided = option.fontMetrics.elidedText(text, Qt.ElideRight, textRect.width())
        isSelected = bool(option.state & QStyle.State_Selected)
        painter.setPen(option.palette.color(
            QPalette.HighlightedText if isSelected else QPalette.Text))
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignLeft, elided)

        painter.setPen(option.palette.color(QPalette.HighlightedText if isSelected else QPalette.PlaceholderText))
        painter.drawText(self.deleteRect(option.rect), Qt.AlignCenter, self.DeleteChar)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            if self.deleteRect(option.rect).contains(event.pos()):
                self.deleteClicked.emit(index.row())
                return True
        return QStyledItemDelegate.editorEvent(self, event, model, option, index)


class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        # self.action = QAction()
        # self.action.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogResetButton))
        # self.addAction(self.action, self.TrailingPosition)
        # self.action.triggered.connect(self.Search)
        proxy = self.focusPolicy()
        # self.listView = BaseListWidget(self)
        # self.listView.setParent(self, Qt.Popup)
        # self.listView.setFocusPolicy(Qt.NoFocus)
        # self.listView.setFocusProxy(self)
        # self.setFocusPolicy(proxy)

        self.widget = QWidget()
        self.help = Ui_LineEditHelp()
        self.help.setupUi(self.widget)

        self.widget.setParent(self, Qt.Popup)
        # self.widget.setFocusPolicy(Qt.NoFocus)
        self.widget.setFocusProxy(self)
        # self.setFocusPolicy(proxy)
        # self.widget.setFocusPolicy(Qt.NoFocus)
        self.widget.setWindowFlags(Qt.ToolTip)
        self.qLabel = QLabel("asdasdasdasd")
        self.hLayout = QHBoxLayout(self.widget)
        self.hLayout.addWidget(self.qLabel)

        # self.model = QWidgetListModel(self)
        # self.listView.setWindowFlags(Qt.ToolTip)
        self.words = []
        self.cacheWords = []
        self.model = QStringListModel(self)
        self.listView.setModel(self.model)
        # self.textChanged.connect(self.setCompleter)
        self.listView.clicked.connect(self.SetText)

        self.isNotReload = False
        self.isShowSearch = True
        self.isMenuShowing = False

        self.searchTag1 = "<font color=#232629>"
        self.searchTag2 = "</font>"

        # 每行右侧的 ✕ 删除按钮
        self.historyDelegate = HistoryItemDelegate(self.listView)
        self.historyDelegate.deleteClicked.connect(self.DeleteHistoryRow)
        self.listView.setItemDelegate(self.historyDelegate)
        # 列表不抢焦点，否则点击列表会让输入框失焦、历史框被 focusOutEvent 隐藏
        self.listView.setFocusPolicy(Qt.NoFocus)

        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.customContextMenuRequested.connect(self.ShowHistoryMenu)

    @property
    def listView(self):
        return self.help.listView

    def SetWordData(self, data):
        self.words = data

    def SetCacheWord(self):
        self.model.setStringList(self.cacheWords)
        return

    def AddCacheWord(self, word):
        if not word:
            return
        if word in self.cacheWords:
            self.cacheWords.remove(word)
        self.cacheWords.insert(0, word)
        del self.cacheWords[200:]
        self.model.setStringList(self.cacheWords)

    def SetText(self, index):
        item = self.model.itemData(index)
        text = item.get(0)
        # self.setText(text.replace(self.searchTag1, "").replace(self.searchTag2, ""))
        self.setText(text)
        self.Search()
        return

    def setCompleter(self, strings):
        if not strings:
            # 显示搜索历史
            self.model.setStringList(self.cacheWords)
            return

        if self.isNotReload:
            return
        strings = strings.upper()

        strings2 = re.split('&|\|', strings)
        strings = strings2.pop() if len(strings2) > 0 else ""
        isSelf = False
        strings = Converter('zh-hans').convert(strings)
        matchIndex = {}
        for data in self.words:
            assert isinstance(data, str)
            if strings == data:
                isSelf = True

            else:
                index = data.find(strings)
                if index < 0:
                    continue
                matchIndex[data] = index
        datas = list(matchIndex.keys())
        datas.sort(key=matchIndex.get)

        if isSelf:
            datas.insert(0, strings)
        self.model.setStringList(datas)

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
            self.Search()
        return QLineEdit.keyReleaseEvent(self, ev)

    def Search(self):
        text = self.text()
        QtOwner().OpenSearch(text)
        self.clearFocus()
        return

    def clearFocus(self) -> None:
        return QLineEdit.clearFocus(self)

    def focusInEvent(self, ev):
        # print("in")
        self.ShowListView()
        return QLineEdit.focusInEvent(self, ev)

    def focusOutEvent(self, ev):
        # 右键菜单是模态的，弹出期间输入框必然失焦；此时不要隐藏历史框，
        # 否则菜单弹出的一瞬间列表内容就全没了
        if self.isMenuShowing:
            return QLineEdit.focusOutEvent(self, ev)
        self.widget.hide()
        # print("out")
        return QLineEdit.focusOutEvent(self, ev)

    def inputMethodEvent(self, event):
        # 输入法组词中(如拼音)隐藏历史框，避免遮挡候选词栏；组词结束后恢复
        if event.preeditString():
            self.HideListView()
        elif self.isShowSearch:
            self.ShowListView()
        return QLineEdit.inputMethodEvent(self, event)

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

    def DeleteHistoryRow(self, row):
        if row < 0:
            return
        index = self.model.index(row, 0)
        text = index.data()
        if text is not None and text in self.cacheWords:
            self.cacheWords.remove(text)
        self.model.removeRow(row)
        self.SaveCacheWord()
        if self.model.rowCount() == 0:
            self.HideListView()

    def ShowHistoryMenu(self, pos):
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        index = self.listView.indexAt(pos)
        actDel = menu.addAction("删除该条历史记录")
        actDel.setEnabled(index.isValid() and bool(self.cacheWords))
        actClear = menu.addAction("清空全部历史记录")
        actClear.setEnabled(bool(self.cacheWords))
        self.isMenuShowing = True
        try:
            act = menu.exec_(self.listView.viewport().mapToGlobal(pos))
        finally:
            self.isMenuShowing = False
        if act == actDel and index.isValid():
            self.DeleteHistoryRow(index.row())
        elif act == actClear:
            self.cacheWords = []
            self.model.setStringList([])
            self.SaveCacheWord()
            self.HideListView()

    def SaveCacheWord(self):
        path = os.path.join(Setting.GetDataPath(), "cache_word")
        try:
            f = open(path, "w+", encoding="utf-8")
            f.write("\n".join(self.cacheWords))
            f.close()
        except Exception as es:
            Log.Error(es)

    def LoadCacheWord(self):
        path = os.path.join(Setting.GetDataPath(), "cache_word")
        try:
            if not os.path.isfile(path):
                return
            f = open(path, "r", encoding="utf-8")
            data = f.read()
            f.close()
            for v in data.split("\n"):
                if v:
                    self.cacheWords.append(v)
        except Exception as es:
            Log.Error(es)