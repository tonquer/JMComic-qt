import re

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon

from config import config
from interface.ui_comment_item import Ui_CommentItem
from interface.ui_proxy_ip_item import Ui_ProxyIPItem
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str


class ProxyIpWidget(QtWidgets.QFrame, Ui_ProxyIPItem):

    def __init__(self, item):
        super(self.__class__, self).__init__()
        Ui_ProxyIPItem.__init__(self)
        self.setupUi(self)
        self.ipLabel.setText(item.ip)
        self.nameBox.setText(item.name)

    def Update(self, item):
        self.ipLabel.setText(item.ip)
        self.nameBox.setText(item.name)
        self.speedLabel.setText("<font color=#7fb80e>{}</font>".format(str(int(float(item.delay))) + "ms"))
        if item.isFail:
            self.speedLabel.setText("<font color=#d71345>{}</font>".format(Str.GetStr(item.st)))
        self.listWidget.clear()
        for tag in item.tags:
            self.listWidget.AddItem(tag)