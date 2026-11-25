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
    QLabel, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_LocalHistory(object):
    def setupUi(self, LocalHistory):
        if not LocalHistory.objectName():
            LocalHistory.setObjectName(u"LocalHistory")
        LocalHistory.resize(628, 334)
        self.gridLayout_2 = QGridLayout(LocalHistory)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(LocalHistory)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(LocalHistory)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.line_2 = QFrame(LocalHistory)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(LocalHistory)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(LocalHistory)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(LocalHistory)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(LocalHistory)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(LocalHistory)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(LocalHistory)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(LocalHistory)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)


        self.retranslateUi(LocalHistory)
        self.jumpButton.clicked.connect(LocalHistory.JumpPage)

        QMetaObject.connectSlotsByName(LocalHistory)
    # setupUi

    def retranslateUi(self, LocalHistory):
        LocalHistory.setWindowTitle(QCoreApplication.translate("LocalHistory", u"\u672c\u5730\u8bb0\u5f55", None))
        self.msgLabel.setText("")
        self.nums.setText(QCoreApplication.translate("LocalHistory", u"\u8bb0\u5f55\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LocalHistory", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LocalHistory", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("LocalHistory", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

