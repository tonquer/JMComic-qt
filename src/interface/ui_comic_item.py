# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_comic_item.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

from component.label.comic_label import ComicLabel

class Ui_ComicItem(object):
    def setupUi(self, ComicItem):
        if not ComicItem.objectName():
            ComicItem.setObjectName(u"ComicItem")
        ComicItem.resize(300, 300)
        ComicItem.setMinimumSize(QSize(0, 0))
        ComicItem.setMaximumSize(QSize(16777215, 16777215))
        ComicItem.setStyleSheet(u"QToolButton\n"
"{\n"
"background-color:transparent;\n"
"  border: 0px;\n"
"  height: 0px;\n"
"  margin: 0px;\n"
"  padding: 0px;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"QToolButton:hover  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:pressed  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:checked  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(ComicItem)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.picLabel = ComicLabel(ComicItem)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.picLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 2, 0, 0)
        self.toolButton = QToolButton(ComicItem)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(0, 20))

        self.horizontalLayout.addWidget(self.toolButton)

        self.categoryLabel = QLabel(ComicItem)
        self.categoryLabel.setObjectName(u"categoryLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryLabel.sizePolicy().hasHeightForWidth())
        self.categoryLabel.setSizePolicy(sizePolicy)
        self.categoryLabel.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.categoryLabel)

        self.starButton = QToolButton(ComicItem)
        self.starButton.setObjectName(u"starButton")
        self.starButton.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.starButton)

        self.timeLabel = QLabel(ComicItem)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.timeLabel, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.nameLable = QLabel(ComicItem)
        self.nameLable.setObjectName(u"nameLable")
        self.nameLable.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.nameLable)


        self.retranslateUi(ComicItem)

        QMetaObject.connectSlotsByName(ComicItem)
    # setupUi

    def retranslateUi(self, ComicItem):
        ComicItem.setWindowTitle(QCoreApplication.translate("ComicItem", u"Form", None))
        self.picLabel.setText(QCoreApplication.translate("ComicItem", u"TextLabel", None))
        self.toolButton.setText("")
        self.categoryLabel.setText(QCoreApplication.translate("ComicItem", u"TextLabel", None))
        self.starButton.setText("")
        self.timeLabel.setText(QCoreApplication.translate("ComicItem", u"TextLabel", None))
        self.nameLable.setText(QCoreApplication.translate("ComicItem", u"TextLabel", None))
    # retranslateUi

