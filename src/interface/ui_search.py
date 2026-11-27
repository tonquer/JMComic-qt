# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from component.line_edit.search_line_edit import SearchLineEdit
from component.list.comic_list_widget import ComicListWidget

class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(900, 560)
        Search.setMinimumSize(QSize(80, 0))
        self.verticalLayout = QVBoxLayout(Search)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 10, 12, 10)
        self.searchTab = QLabel(Search)
        self.searchTab.setObjectName(u"searchTab")
        self.searchTab.setEnabled(True)
        self.searchTab.setProperty(u"role", u"sectionTitle")
        self.searchTab.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.verticalLayout.addWidget(self.searchTab)

        self.searchWidget = QFrame(Search)
        self.searchWidget.setObjectName(u"searchWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchWidget.sizePolicy().hasHeightForWidth())
        self.searchWidget.setSizePolicy(sizePolicy)
        self.searchWidget.setProperty(u"role", u"card")
        self.verticalLayout_2 = QVBoxLayout(self.searchWidget)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(12, 10, 12, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.searchWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setProperty(u"role", u"muted")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.searchWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(20, 20))
        self.label_3.setMaximumSize(QSize(20, 20))
        self.label_3.setProperty(u"role", u"muted")
        self.label_3.setStyleSheet(u"QLabel#label_3 { border: 1px solid #94A3B8; border-radius: 10px; font-weight: 600; }")
        self.label_3.setToolTipDuration(-1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = SearchLineEdit(self.searchWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 0))
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(self.searchWidget)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.cateLabel = QLabel(self.searchWidget)
        self.cateLabel.setObjectName(u"cateLabel")
        self.cateLabel.setProperty(u"role", u"muted")

        self.horizontalLayout_6.addWidget(self.cateLabel)

        self.typeBox = QComboBox(self.searchWidget)
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.addItem("")
        self.typeBox.setObjectName(u"typeBox")
        self.typeBox.setMinimumSize(QSize(104, 0))

        self.horizontalLayout_6.addWidget(self.typeBox)

        self.yearBox = QComboBox(self.searchWidget)
        self.yearBox.addItem("")
        self.yearBox.setObjectName(u"yearBox")
        self.yearBox.setMinimumSize(QSize(104, 0))

        self.horizontalLayout_6.addWidget(self.yearBox)

        self.monthBox = QComboBox(self.searchWidget)
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.addItem("")
        self.monthBox.setObjectName(u"monthBox")
        self.monthBox.setMinimumSize(QSize(104, 0))

        self.horizontalLayout_6.addWidget(self.monthBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.searchWidget)

        self.bookList = ComicListWidget(Search)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout.addWidget(self.bookList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, -1)
        self.sortCombox = QComboBox(Search)
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.addItem("")
        self.sortCombox.setObjectName(u"sortCombox")
        self.sortCombox.setEnabled(True)
        self.sortCombox.setMinimumSize(QSize(110, 0))

        self.horizontalLayout.addWidget(self.sortCombox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label = QLabel(Search)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(Search)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(68, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.jumpPage = QPushButton(Search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(68, 0))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(2, 1)

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
        self.label_3.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u7cbe\u786e\u641c\u7d22\u3011</p><p>jm+\u53f7\u7801</p><p><br/></p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Search", u"?", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Search", u"\u8f93\u5165\u5173\u952e\u8bcd\u6216 JM \u7f16\u53f7\u641c\u7d22\u2026", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.cateLabel.setText(QCoreApplication.translate("Search", u"\u9ad8\u7ea7\u641c\u7d22\uff1a", None))
        self.typeBox.setItemText(0, QCoreApplication.translate("Search", u"\u7ad9\u5185\u641c\u7d22", None))
        self.typeBox.setItemText(1, QCoreApplication.translate("Search", u"\u4f5c\u54c1", None))
        self.typeBox.setItemText(2, QCoreApplication.translate("Search", u"\u4f5c\u8005", None))
        self.typeBox.setItemText(3, QCoreApplication.translate("Search", u"\u6807\u7b7e", None))
        self.typeBox.setItemText(4, QCoreApplication.translate("Search", u"\u767b\u573a\u4eba\u7269", None))

        self.yearBox.setItemText(0, QCoreApplication.translate("Search", u"\u5168\u90e8\u5e74\u4efd", None))

        self.monthBox.setItemText(0, QCoreApplication.translate("Search", u"\u5168\u90e8\u6708\u4efd", None))
        self.monthBox.setItemText(1, QCoreApplication.translate("Search", u"1", None))
        self.monthBox.setItemText(2, QCoreApplication.translate("Search", u"2", None))
        self.monthBox.setItemText(3, QCoreApplication.translate("Search", u"3", None))
        self.monthBox.setItemText(4, QCoreApplication.translate("Search", u"4", None))
        self.monthBox.setItemText(5, QCoreApplication.translate("Search", u"5", None))
        self.monthBox.setItemText(6, QCoreApplication.translate("Search", u"6", None))
        self.monthBox.setItemText(7, QCoreApplication.translate("Search", u"7", None))
        self.monthBox.setItemText(8, QCoreApplication.translate("Search", u"8", None))
        self.monthBox.setItemText(9, QCoreApplication.translate("Search", u"9", None))
        self.monthBox.setItemText(10, QCoreApplication.translate("Search", u"10", None))
        self.monthBox.setItemText(11, QCoreApplication.translate("Search", u"11", None))
        self.monthBox.setItemText(12, QCoreApplication.translate("Search", u"12", None))

        self.sortCombox.setItemText(0, QCoreApplication.translate("Search", u"\u6700\u65b0", None))
        self.sortCombox.setItemText(1, QCoreApplication.translate("Search", u"\u6700\u591a\u70b9\u51fb", None))
        self.sortCombox.setItemText(2, QCoreApplication.translate("Search", u"\u6700\u591a\u56fe\u7247", None))
        self.sortCombox.setItemText(3, QCoreApplication.translate("Search", u"\u6700\u591a\u7231\u5fc3", None))

        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u8df3\u8f6c", None))
    # retranslateUi

