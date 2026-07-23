# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_proxy_ip_item.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QListView, QListWidgetItem, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from component.list.tag_list_widget import TagListWidget

class Ui_ProxyIPItem(object):
    def setupUi(self, ProxyIPItem):
        if not ProxyIPItem.objectName():
            ProxyIPItem.setObjectName(u"ProxyIPItem")
        ProxyIPItem.resize(400, 106)
        self.verticalLayout = QVBoxLayout(ProxyIPItem)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameBox = QCheckBox(ProxyIPItem)
        self.nameBox.setObjectName(u"nameBox")

        self.horizontalLayout.addWidget(self.nameBox)

        self.ipLabel = QLabel(ProxyIPItem)
        self.ipLabel.setObjectName(u"ipLabel")

        self.horizontalLayout.addWidget(self.ipLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.speedLabel = QLabel(ProxyIPItem)
        self.speedLabel.setObjectName(u"speedLabel")
        self.speedLabel.setMinimumSize(QSize(30, 0))

        self.horizontalLayout.addWidget(self.speedLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = TagListWidget(ProxyIPItem)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(16777215, 60))
        self.listWidget.setStyleSheet(u"background-color:transparent;")
        self.listWidget.setFlow(QListView.LeftToRight)

        self.verticalLayout.addWidget(self.listWidget)


        self.retranslateUi(ProxyIPItem)

        QMetaObject.connectSlotsByName(ProxyIPItem)
    # setupUi

    def retranslateUi(self, ProxyIPItem):
        ProxyIPItem.setWindowTitle(QCoreApplication.translate("ProxyIPItem", u"Frame", None))
        self.nameBox.setText(QCoreApplication.translate("ProxyIPItem", u"CheckBox", None))
        self.ipLabel.setText(QCoreApplication.translate("ProxyIPItem", u"TextLabel", None))
        self.speedLabel.setText("")
    # retranslateUi

