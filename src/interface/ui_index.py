# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_index.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidgetItem, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Index(object):
    def setupUi(self, Index):
        if not Index.objectName():
            Index.setObjectName(u"Index")
        Index.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(Index)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButton = QToolButton(Index)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.bookList = ComicListWidget(Index)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout_2.addWidget(self.bookList)


        self.retranslateUi(Index)

        QMetaObject.connectSlotsByName(Index)
    # setupUi

    def retranslateUi(self, Index):
        Index.setWindowTitle(QCoreApplication.translate("Index", u"\u9996\u9875", None))
        self.toolButton.setText(QCoreApplication.translate("Index", u"\u5237\u65b0(F5)", None))
#if QT_CONFIG(shortcut)
        self.toolButton.setShortcut(QCoreApplication.translate("Index", u"F5", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

