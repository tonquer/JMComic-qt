# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local_history.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_LocalHistory(object):
    def setupUi(self, LocalHistory):
        if not LocalHistory.objectName():
            LocalHistory.setObjectName(u"LocalHistory")
        LocalHistory.resize(900, 560)
        self.gridLayout_2 = QVBoxLayout(LocalHistory)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(12, 10, 12, 10)
        self.widget = QFrame(LocalHistory)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setProperty(u"role", u"card")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 10, 12, 10)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.gridLayout_2.addWidget(self.widget)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.bookList = ComicListWidget(LocalHistory)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, -1)
        self.msgLabel = QLabel(LocalHistory)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.nums = QLabel(LocalHistory)
        self.nums.setObjectName(u"nums")
        self.nums.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(LocalHistory)
        self.pages.setObjectName(u"pages")
        self.pages.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.pages)

        self.spinBox = QSpinBox(LocalHistory)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(68, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.jumpButton = QPushButton(LocalHistory)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(68, 0))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2.setStretch(1, 1)

        self.retranslateUi(LocalHistory)
        self.jumpButton.clicked.connect(LocalHistory.JumpPage)

        QMetaObject.connectSlotsByName(LocalHistory)
    # setupUi

    def retranslateUi(self, LocalHistory):
        LocalHistory.setWindowTitle(QCoreApplication.translate("LocalHistory", u"\u672c\u5730\u8bb0\u5f55", None))
        self.label.setText(QCoreApplication.translate("LocalHistory", u"\u641c\u7d22\uff1a", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("LocalHistory", u"\u8f93\u5165\u89c2\u770b\u8bb0\u5f55\u6807\u9898\u6216 ID \u641c\u7d22\u2026", None))
        self.msgLabel.setText("")
        self.nums.setText(QCoreApplication.translate("LocalHistory", u"\u8bb0\u5f55\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LocalHistory", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LocalHistory", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("LocalHistory", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

