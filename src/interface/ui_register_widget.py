# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_register_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QWidget)

class Ui_RegisterWidget(object):
    def setupUi(self, RegisterWidget):
        if not RegisterWidget.objectName():
            RegisterWidget.setObjectName(u"RegisterWidget")
        RegisterWidget.resize(388, 198)
        self.gridLayout_2 = QGridLayout(RegisterWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.name = QLabel(RegisterWidget)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(80, 0))
        self.name.setMaximumSize(QSize(60, 16777215))
        self.name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.name)

        self.nameEdit = QLineEdit(RegisterWidget)
        self.nameEdit.setObjectName(u"nameEdit")

        self.horizontalLayout.addWidget(self.nameEdit)


        self.gridLayout.addLayout(self.horizontalLayout, 11, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.user = QLabel(RegisterWidget)
        self.user.setObjectName(u"user")
        self.user.setMinimumSize(QSize(80, 0))
        self.user.setMaximumSize(QSize(60, 16777215))
        self.user.setLayoutDirection(Qt.LeftToRight)
        self.user.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.user)

        self.userEdit = QLineEdit(RegisterWidget)
        self.userEdit.setObjectName(u"userEdit")
        self.userEdit.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.userEdit)


        self.gridLayout.addLayout(self.horizontalLayout_3, 10, 1, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.passwd = QLabel(RegisterWidget)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setMinimumSize(QSize(80, 0))
        self.passwd.setMaximumSize(QSize(60, 16777215))
        self.passwd.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.passwd)

        self.passwdEdit = QLineEdit(RegisterWidget)
        self.passwdEdit.setObjectName(u"passwdEdit")

        self.horizontalLayout_19.addWidget(self.passwdEdit)


        self.gridLayout.addLayout(self.horizontalLayout_19, 12, 1, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.gender_Male = QRadioButton(RegisterWidget)
        self.buttonGroup = QButtonGroup(RegisterWidget)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.gender_Male)
        self.gender_Male.setObjectName(u"gender_Male")
        self.gender_Male.setChecked(True)

        self.horizontalLayout_10.addWidget(self.gender_Male)

        self.gender_Female = QRadioButton(RegisterWidget)
        self.buttonGroup.addButton(self.gender_Female)
        self.gender_Female.setObjectName(u"gender_Female")

        self.horizontalLayout_10.addWidget(self.gender_Female)


        self.gridLayout.addLayout(self.horizontalLayout_10, 13, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.userEdit, self.nameEdit)
        QWidget.setTabOrder(self.nameEdit, self.passwdEdit)
        QWidget.setTabOrder(self.passwdEdit, self.gender_Male)
        QWidget.setTabOrder(self.gender_Male, self.gender_Female)

        self.retranslateUi(RegisterWidget)

        QMetaObject.connectSlotsByName(RegisterWidget)
    # setupUi

    def retranslateUi(self, RegisterWidget):
        RegisterWidget.setWindowTitle(QCoreApplication.translate("RegisterWidget", u"\u65b0\u7528\u6237\u6ce8\u518c", None))
        self.name.setText(QCoreApplication.translate("RegisterWidget", u"\u7528\u6237\u540d\uff1a", None))
        self.user.setText(QCoreApplication.translate("RegisterWidget", u"\u90ae\u7bb1\uff1a", None))
        self.passwd.setText(QCoreApplication.translate("RegisterWidget", u"\u5bc6\u7801\uff1a", None))
        self.gender_Male.setText(QCoreApplication.translate("RegisterWidget", u"\u7537", None))
        self.gender_Female.setText(QCoreApplication.translate("RegisterWidget", u"\u5973", None))
    # retranslateUi

