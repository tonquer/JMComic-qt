# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download_some_edit.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QHBoxLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_DownloadSomeEdit(object):
    def setupUi(self, DownloadSomeEdit):
        if not DownloadSomeEdit.objectName():
            DownloadSomeEdit.setObjectName(u"DownloadSomeEdit")
        DownloadSomeEdit.resize(897, 500)
        self.verticalLayout = QVBoxLayout(DownloadSomeEdit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DownloadSomeEdit)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.textEdit = QTextEdit(DownloadSomeEdit)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.saveButton = QPushButton(DownloadSomeEdit)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMaximumSize(QSize(150, 30))
        self.saveButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.saveButton)

        self.closeButton = QPushButton(DownloadSomeEdit)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        QWidget.setTabOrder(self.saveButton, self.closeButton)

        self.retranslateUi(DownloadSomeEdit)

        QMetaObject.connectSlotsByName(DownloadSomeEdit)
    # setupUi

    def retranslateUi(self, DownloadSomeEdit):
        DownloadSomeEdit.setWindowTitle(QCoreApplication.translate("DownloadSomeEdit", u"Form", None))
        self.label.setText(QCoreApplication.translate("DownloadSomeEdit", u"\u8bf7\u8f93\u5165\u5e26JM\u53f7\u7684\u6587\u672c", None))
        self.saveButton.setText(QCoreApplication.translate("DownloadSomeEdit", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.saveButton.setShortcut(QCoreApplication.translate("DownloadSomeEdit", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeButton.setText(QCoreApplication.translate("DownloadSomeEdit", u"\u5173\u95ed", None))
    # retranslateUi

