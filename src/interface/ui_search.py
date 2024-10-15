# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from component.line_edit.search_line_edit import SearchLineEdit
from component.list.comic_list_widget import ComicListWidget

class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(740, 369)
        Search.setMinimumSize(QSize(80, 0))
        self.verticalLayout = QVBoxLayout(Search)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.searchTab = QLabel(Search)
        self.searchTab.setObjectName(u"searchTab")
        self.searchTab.setEnabled(True)
        self.searchTab.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout.addWidget(self.searchTab)

        self.searchWidget = QWidget(Search)
        self.searchWidget.setObjectName(u"searchWidget")
        self.verticalLayout_2 = QVBoxLayout(self.searchWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.searchWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.searchWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(20, 0))
        self.label_3.setMaximumSize(QSize(20, 16777215))
        self.label_3.setToolTipDuration(-1)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = SearchLineEdit(self.searchWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 40))
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(self.searchWidget)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.searchWidget)

        self.bookList = ComicListWidget(Search)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout.addWidget(self.bookList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sortCombox = QComboBox(Search)
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.setObjectName(u"sortCombox")
        self.sortCombox.setEnabled(True)
        self.sortCombox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.sortCombox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.line_4 = QFrame(Search)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(Search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.line_5 = QFrame(Search)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.spinBox = QSpinBox(Search)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 0))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_6 = QFrame(Search)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_6)

        self.jumpPage = QPushButton(Search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(60, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Search)

        QMetaObject.connectSlotsByName(Search)
    # setupUi

    def retranslateUi(self, Search):
        Search.setWindowTitle(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.searchTab.setText("")
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Search", u"\u641c\u7d22\uff1a", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Search", u"?", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.sortCombox.setItemText(0, QCoreApplication.translate("Search", u"\u6700\u65b0", None))
        self.sortCombox.setItemText(1, QCoreApplication.translate("Search", u"\u6700\u591a\u70b9\u51fb", None))
        self.sortCombox.setItemText(2, QCoreApplication.translate("Search", u"\u6700\u591a\u56fe\u7247", None))
        self.sortCombox.setItemText(3, QCoreApplication.translate("Search", u"\u6700\u591a\u7231\u5fc3", None))

        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u8df3\u8f6c", None))
    # retranslateUi

