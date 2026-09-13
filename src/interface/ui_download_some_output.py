# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download_some_output.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_DownloadSomeOutput(object):
    def setupUi(self, DownloadSomeOutput):
        if not DownloadSomeOutput.objectName():
            DownloadSomeOutput.setObjectName(u"DownloadSomeOutput")
        DownloadSomeOutput.resize(897, 500)
        self.verticalLayout = QVBoxLayout(DownloadSomeOutput)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DownloadSomeOutput)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.textEdit = QTextEdit(DownloadSomeOutput)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.switchButton = QPushButton(DownloadSomeOutput)
        self.switchButton.setObjectName(u"switchButton")
        self.switchButton.setMaximumSize(QSize(150, 30))
        self.switchButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.switchButton)

        self.closeButton = QPushButton(DownloadSomeOutput)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        QWidget.setTabOrder(self.switchButton, self.closeButton)

        self.retranslateUi(DownloadSomeOutput)

        QMetaObject.connectSlotsByName(DownloadSomeOutput)
    # setupUi

    def retranslateUi(self, DownloadSomeOutput):
        DownloadSomeOutput.setWindowTitle(QCoreApplication.translate("DownloadSomeOutput", u"Form", None))
        self.label.setText(QCoreApplication.translate("DownloadSomeOutput", u"\u5bfc\u51fa\u7684JM\u53f7", None))
        self.switchButton.setText(QCoreApplication.translate("DownloadSomeOutput", u"\u5207\u6362", None))
#if QT_CONFIG(shortcut)
        self.switchButton.setShortcut(QCoreApplication.translate("DownloadSomeOutput", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeButton.setText(QCoreApplication.translate("DownloadSomeOutput", u"\u5173\u95ed", None))
    # retranslateUi

