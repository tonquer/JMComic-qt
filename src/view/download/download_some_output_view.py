import os

from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFileDialog, QHeaderView, QAbstractItemView

from component.dialog.base_mask_dialog import BaseMaskDialog
from component.label.gif_label import GifLabel
from config import config
from config.setting import Setting
from interface.ui_download_dir import Ui_DownloadDir
from interface.ui_download_some_output import Ui_DownloadSomeOutput
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_upload import QtUpTask
from tools.str import Str
import re


class DownloadSomeOutputView(BaseMaskDialog, Ui_DownloadSomeOutput, QtTaskBase):
    SwitchSignal = Signal(list)

    def __init__(self, parent=None, nextID=1):
        BaseMaskDialog.__init__(self, parent)
        Ui_DownloadSomeOutput.__init__(self)
        QtTaskBase.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.closeButton.clicked.connect(self.close)
        self.switchButton.clicked.connect(self.Switch)
        self.mode = 0

    def retranslateUi(self, DownloadSomeOutput):
        Ui_DownloadSomeOutput.retranslateUi(self, DownloadSomeOutput)
        self.label.setText(Str.GetStr(Str.ExportedJmIds))
        self.closeButton.setText(Str.GetStr(Str.Close))
        self.switchButton.setText(Str.GetStr(Str.Switch))
    
    def Switch(self):
        self.mode = (self.mode + 1) % 4
        self.SwitchSignal.emit(self.mode)
