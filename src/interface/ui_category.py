# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_category.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Category(object):
    def setupUi(self, Category):
        if not Category.objectName():
            Category.setObjectName(u"Category")
        Category.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Category)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Category)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Category)

        QMetaObject.connectSlotsByName(Category)
    # setupUi

    def retranslateUi(self, Category):
        Category.setWindowTitle(QCoreApplication.translate("Category", u"\u5206\u7c7b", None))
    # retranslateUi

