# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_line_edit_help_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QLabel, QListView, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_LineEditHelp(object):
    def setupUi(self, LineEditHelp):
        if not LineEditHelp.objectName():
            LineEditHelp.setObjectName(u"LineEditHelp")
        LineEditHelp.resize(400, 440)
        self.verticalLayout_2 = QVBoxLayout(LineEditHelp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(LineEditHelp)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listView = QListView(LineEditHelp)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(0, 120))

        self.verticalLayout_2.addWidget(self.listView)


        self.retranslateUi(LineEditHelp)

        QMetaObject.connectSlotsByName(LineEditHelp)
    # setupUi

    def retranslateUi(self, LineEditHelp):
        LineEditHelp.setWindowTitle(QCoreApplication.translate("LineEditHelp", u"Form", None))
        self.label.setText(QCoreApplication.translate("LineEditHelp", u"\u641c\u7d22\u8bb0\u5f55", None))
    # retranslateUi

