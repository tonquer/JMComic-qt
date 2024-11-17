# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_user_manager_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_UserManagerWidget(object):
    def setupUi(self, UserManagerWidget):
        if not UserManagerWidget.objectName():
            UserManagerWidget.setObjectName(u"UserManagerWidget")
        UserManagerWidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(UserManagerWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(UserManagerWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 390, 462))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)

        self.commandLinkButton = QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton.setObjectName(u"commandLinkButton")

        self.verticalLayout_2.addWidget(self.commandLinkButton)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.verfyEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.verfyEdit.setObjectName(u"verfyEdit")

        self.horizontalLayout.addWidget(self.verfyEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verfyButton = QPushButton(self.scrollAreaWidgetContents)
        self.verfyButton.setObjectName(u"verfyButton")

        self.verticalLayout_2.addWidget(self.verfyButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.resetEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.resetEdit.setObjectName(u"resetEdit")

        self.horizontalLayout_2.addWidget(self.resetEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.resetButton = QPushButton(self.scrollAreaWidgetContents)
        self.resetButton.setObjectName(u"resetButton")

        self.verticalLayout_2.addWidget(self.resetButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.sendEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.sendEdit.setObjectName(u"sendEdit")

        self.horizontalLayout_3.addWidget(self.sendEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.sendButton = QPushButton(self.scrollAreaWidgetContents)
        self.sendButton.setObjectName(u"sendButton")

        self.verticalLayout_2.addWidget(self.sendButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(UserManagerWidget)

        QMetaObject.connectSlotsByName(UserManagerWidget)
    # setupUi

    def retranslateUi(self, UserManagerWidget):
        UserManagerWidget.setWindowTitle(QCoreApplication.translate("UserManagerWidget", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("UserManagerWidget", u"\u5982\u679c\u4f60\u7684\u90ae\u4ef6\u4e00\u76f4\u65e0\u6cd5\u63a5\u53d7\u5230\u9a8c\u8bc1\u8fde\u63a5", None))
        self.label_8.setText(QCoreApplication.translate("UserManagerWidget", u"\u8bf7\u524d\u5f80\u5b98\u65b9Discord\u9891\u9053-\u672a\u6536\u5230\u9a8c\u8bc1\u4fe1\u534f\u52a9\u533a", None))
        self.commandLinkButton.setText(QCoreApplication.translate("UserManagerWidget", u"\u5b98\u65b9Discord", None))
        self.label.setText(QCoreApplication.translate("UserManagerWidget", u"\u91cd\u65b0\u53d1\u9001\u90ae\u7bb1\u9a8c\u8bc1", None))
        self.label_2.setText(QCoreApplication.translate("UserManagerWidget", u"\u90ae\u7bb1\uff1a", None))
        self.verfyButton.setText(QCoreApplication.translate("UserManagerWidget", u"\u53d1\u9001", None))
        self.label_3.setText(QCoreApplication.translate("UserManagerWidget", u"\u91cd\u7f6e\u5bc6\u7801", None))
        self.label_4.setText(QCoreApplication.translate("UserManagerWidget", u"\u90ae\u7bb1\uff1a", None))
        self.resetButton.setText(QCoreApplication.translate("UserManagerWidget", u"\u53d1\u9001", None))
        self.label_5.setText(QCoreApplication.translate("UserManagerWidget", u"\u8d26\u53f7\u9a8c\u8bc1\uff08\u5982\u679c\u4f60\u65e0\u6cd5\u6253\u5f00\u90ae\u7bb1\u91cc\u7684\u9a8c\u8bc1\u5730\u5740\uff0c\u53ef\u4ee5\u590d\u5236\u5230\u6b64\u5904\u9a8c\u8bc1\uff09", None))
        self.label_6.setText(QCoreApplication.translate("UserManagerWidget", u"\u5730\u5740\uff1a", None))
        self.sendButton.setText(QCoreApplication.translate("UserManagerWidget", u"\u53d1\u9001", None))
    # retranslateUi

