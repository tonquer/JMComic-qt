# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
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
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Search)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(80, 0))
        self.label_2.setMaximumSize(QSize(80, 40))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit = SearchLineEdit(Search)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(40, 40))
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(Search)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

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

        self.dayCombox = QComboBox(Search)
        self.dayCombox.addItem("")
        self.dayCombox.addItem("")
        self.dayCombox.addItem("")
        self.dayCombox.addItem("")
        self.dayCombox.setObjectName(u"dayCombox")
        self.dayCombox.setEnabled(True)

        self.horizontalLayout.addWidget(self.dayCombox)

        self.categoryBox = QComboBox(Search)
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.addItem("")
        self.categoryBox.setObjectName(u"categoryBox")

        self.horizontalLayout.addWidget(self.categoryBox)

        self.subCategoryBox = QComboBox(Search)
        self.subCategoryBox.setObjectName(u"subCategoryBox")

        self.horizontalLayout.addWidget(self.subCategoryBox)

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
        self.label_2.setText(QCoreApplication.translate("Search", u"\u641c\u7d22\uff1a", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.sortCombox.setItemText(0, QCoreApplication.translate("Search", u"\u6700\u65b0", None))
        self.sortCombox.setItemText(1, QCoreApplication.translate("Search", u"\u6700\u591a\u70b9\u51fb", None))
        self.sortCombox.setItemText(2, QCoreApplication.translate("Search", u"\u6700\u591a\u56fe\u7247", None))
        self.sortCombox.setItemText(3, QCoreApplication.translate("Search", u"\u6700\u591a\u7231\u5fc3", None))

        self.dayCombox.setItemText(0, QCoreApplication.translate("Search", u"\u6240\u6709", None))
        self.dayCombox.setItemText(1, QCoreApplication.translate("Search", u"\u4eca\u65e5", None))
        self.dayCombox.setItemText(2, QCoreApplication.translate("Search", u"\u672c\u5468", None))
        self.dayCombox.setItemText(3, QCoreApplication.translate("Search", u"\u672c\u6708", None))

        self.categoryBox.setItemText(0, QCoreApplication.translate("Search", u"\u5168\u90e8", None))
        self.categoryBox.setItemText(1, QCoreApplication.translate("Search", u"\u5176\u4ed6\u6f2b\u753b", None))
        self.categoryBox.setItemText(2, QCoreApplication.translate("Search", u"\u540c\u4eba\u5fd7", None))
        self.categoryBox.setItemText(3, QCoreApplication.translate("Search", u"\u97e9\u6f2b", None))
        self.categoryBox.setItemText(4, QCoreApplication.translate("Search", u"\u7f8e\u6f2b", None))
        self.categoryBox.setItemText(5, QCoreApplication.translate("Search", u"\u77ed\u7247", None))
        self.categoryBox.setItemText(6, QCoreApplication.translate("Search", u"\u5355\u672c", None))

        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u8df3\u8f6c", None))
    # retranslateUi

