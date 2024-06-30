import os

from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFileDialog, QHeaderView, QAbstractItemView

from component.dialog.base_mask_dialog import BaseMaskDialog
from component.label.gif_label import GifLabel
from config import config
from config.setting import Setting
from interface.ui_download_dir import Ui_DownloadDir
from interface.ui_download_some_edit import Ui_DownloadSomeEdit
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_upload import QtUpTask
from tools.str import Str
import re

class DownloadSomeEditView(BaseMaskDialog, Ui_DownloadSomeEdit, QtTaskBase):
    SaveLogin = Signal(list)

    def __init__(self, parent=None, nextID=1):
        BaseMaskDialog.__init__(self, parent)
        Ui_DownloadSomeEdit.__init__(self)
        QtTaskBase.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.Save)
        
    def Save(self):
        allBookIds = []
        data = self.textEdit.toPlainText()
        for text in data.split("\n"):
            text = text.lower()
            for bookId in re.findall('jm(\d+)', text):
                bookId = int(bookId)
                allBookIds.append(bookId)

        allBookIds = allBookIds[:1000]
        if not allBookIds:
            QtOwner().ShowError(Str.GetStr(Str.NotSpace))
            return
        self.SaveLogin.emit(allBookIds)
        self.close()
        return
    