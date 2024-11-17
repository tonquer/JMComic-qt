# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_week.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QListWidgetItem, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Week(object):
    def setupUi(self, Week):
        if not Week.objectName():
            Week.setObjectName(u"Week")
        Week.resize(423, 311)
        self.verticalLayout_2 = QVBoxLayout(Week)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(Week)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(400, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.label = QLabel(Week)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(Week)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mangaWidget = ComicListWidget(self.tab)
        self.mangaWidget.setObjectName(u"mangaWidget")

        self.verticalLayout.addWidget(self.mangaWidget)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.hanmanWidget = ComicListWidget(self.tab_2)
        self.hanmanWidget.setObjectName(u"hanmanWidget")

        self.verticalLayout_3.addWidget(self.hanmanWidget)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.anotherWidget = ComicListWidget(self.tab_3)
        self.anotherWidget.setObjectName(u"anotherWidget")

        self.verticalLayout_4.addWidget(self.anotherWidget)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(Week)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Week)
    # setupUi

    def retranslateUi(self, Week):
        Week.setWindowTitle(QCoreApplication.translate("Week", u"\u6bcf\u5468\u5fc5\u770b", None))
        self.label.setText(QCoreApplication.translate("Week", u"\u6bcf\u5468\u4e94 18:00\u66f4\u65b0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Week", u"\u65e5\u6f2b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Week", u"\u97e9\u6f2b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Week", u"\u5176\u4ed6", None))
    # retranslateUi

