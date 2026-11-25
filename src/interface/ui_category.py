# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_category.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Category(object):
    def setupUi(self, Category):
        if not Category.objectName():
            Category.setObjectName(u"Category")
        Category.resize(552, 305)
        self.verticalLayout = QVBoxLayout(Category)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Category)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sortCombox = QComboBox(Category)
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.setObjectName(u"sortCombox")
        self.sortCombox.setEnabled(True)
        self.sortCombox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortCombox)

        self.subBox = QComboBox(Category)
        self.subBox.addItem("")
        self.subBox.setObjectName(u"subBox")
        self.subBox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.subBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label = QLabel(Category)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(Category)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(68, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.jumpPage = QPushButton(Category)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(64, 0))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Category)

        QMetaObject.connectSlotsByName(Category)
    # setupUi

    def retranslateUi(self, Category):
        Category.setWindowTitle(QCoreApplication.translate("Category", u"\u5206\u7c7b", None))
        self.sortCombox.setItemText(0, QCoreApplication.translate("Category", u"\u6700\u65b0", None))
        self.sortCombox.setItemText(1, QCoreApplication.translate("Category", u"\u603b\u6392\u884c", None))
        self.sortCombox.setItemText(2, QCoreApplication.translate("Category", u"\u6708\u6392\u884c", None))
        self.sortCombox.setItemText(3, QCoreApplication.translate("Category", u"\u5468\u6392\u884c", None))
        self.sortCombox.setItemText(4, QCoreApplication.translate("Category", u"\u65e5\u6392\u884c", None))
        self.sortCombox.setItemText(5, QCoreApplication.translate("Category", u"\u6700\u591a\u56fe\u7247", None))
        self.sortCombox.setItemText(6, QCoreApplication.translate("Category", u"\u6700\u591a\u7231\u5fc3", None))

        self.subBox.setItemText(0, QCoreApplication.translate("Category", u"\u5168\u90e8", None))

        self.label.setText(QCoreApplication.translate("Category", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Category", u"\u8df3\u8f6c", None))
    # retranslateUi

