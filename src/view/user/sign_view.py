from PySide6 import QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QTableWidgetItem, QVBoxLayout, QCalendarWidget, QLabel

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_doh_dns import Ui_DohDns
from interface.ui_sign_widget import Ui_SignWidget
from tools.qt_domain import QtDomainMgr


class SignView(BaseMaskDialog, Ui_SignWidget):
    def __init__(self, parent=None, signMap=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_SignWidget.__init__(self)
        self.setupUi(self.widget)
        self.closeButton.clicked.connect(self.close)
        for i in range(1, 32):
            label = getattr(self, "label_{}".format(i), None)

            if not label:
                continue

            if i not in signMap:
                label.setText("")
                continue
            v = signMap.get(i)
            if v == False:
                label.setPixmap(QPixmap(":/png/icon/no_sign.svg"))
            elif v == True:
                label.setPixmap(QPixmap(":/png/icon/sign.svg"))
