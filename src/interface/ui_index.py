# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_index.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Index(object):
    def setupUi(self, Index):
        if not Index.objectName():
            Index.setObjectName(u"Index")
        Index.resize(595, 279)
        self.verticalLayout_2 = QVBoxLayout(Index)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(Index)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.newListWidget = ComicListWidget(self.tab)
        self.newListWidget.setObjectName(u"newListWidget")

        self.verticalLayout.addWidget(self.newListWidget)

        self.tabWidget.addTab(self.tab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.widget = QWidget(Index)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(383, 27, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pages = QLabel(self.widget)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line_3 = QFrame(self.widget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.spinBox = QSpinBox(self.widget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.jumpButton = QPushButton(self.widget)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Index)

        QMetaObject.connectSlotsByName(Index)
    # setupUi

    def retranslateUi(self, Index):
        Index.setWindowTitle(QCoreApplication.translate("Index", u"\u9996\u9875", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Index", u"\u6700\u65b0\u4e0a\u4f20", None))
        self.pages.setText(QCoreApplication.translate("Index", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("Index", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Index", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

