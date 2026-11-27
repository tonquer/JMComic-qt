# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget
from component.list.tag_list_widget import TagListWidget

class Ui_Local(object):
    def setupUi(self, Local):
        if not Local.objectName():
            Local.setObjectName(u"Local")
        Local.resize(900, 560)
        self.gridLayout_2 = QVBoxLayout(Local)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(12, 10, 12, 10)
        self.topCard = QFrame(Local)
        self.topCard.setObjectName(u"topCard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topCard.sizePolicy().hasHeightForWidth())
        self.topCard.setSizePolicy(sizePolicy)
        self.topCard.setProperty(u"role", u"card")
        self.topCardLayout = QVBoxLayout(self.topCard)
        self.topCardLayout.setSpacing(8)
        self.topCardLayout.setObjectName(u"topCardLayout")
        self.topCardLayout.setContentsMargins(12, 10, 12, 10)
        self.widget = QWidget(self.topCard)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"QWidget#widget { background: transparent; border: none; }")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")

        self.horizontalLayout_3.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.delAll = QPushButton(self.widget)
        self.delAll.setObjectName(u"delAll")
        self.delAll.setMinimumSize(QSize(84, 0))

        self.horizontalLayout_3.addWidget(self.delAll)

        self.toolButton = QPushButton(self.widget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setMinimumSize(QSize(84, 0))
        self.toolButton.setProperty(u"variant", u"primary")

        self.horizontalLayout_3.addWidget(self.toolButton)


        self.topCardLayout.addWidget(self.widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tagsList = TagListWidget(self.topCard)
        self.tagsList.setObjectName(u"tagsList")
        self.tagsList.setFrameShape(QFrame.Shape.NoFrame)
        self.tagsList.setSpacing(0)

        self.horizontalLayout_2.addWidget(self.tagsList)


        self.topCardLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addWidget(self.topCard)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.bookList = ComicListWidget(Local)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, -1)
        self.sortKeyCombox = QComboBox(Local)
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.setObjectName(u"sortKeyCombox")
        self.sortKeyCombox.setEnabled(True)
        self.sortKeyCombox.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.sortKeyCombox)

        self.sortIdCombox = QComboBox(Local)
        self.sortIdCombox.addItem("")
        self.sortIdCombox.addItem("")
        self.sortIdCombox.setObjectName(u"sortIdCombox")
        self.sortIdCombox.setEnabled(True)
        self.sortIdCombox.setMinimumSize(QSize(76, 0))

        self.horizontalLayout.addWidget(self.sortIdCombox)

        self.msgLabel = QLabel(Local)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.nums = QLabel(Local)
        self.nums.setObjectName(u"nums")
        self.nums.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(Local)
        self.pages.setObjectName(u"pages")
        self.pages.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.pages)

        self.spinBox = QSpinBox(Local)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(68, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.jumpButton = QPushButton(Local)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(68, 0))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2.setStretch(1, 1)

        self.retranslateUi(Local)
        self.jumpButton.clicked.connect(Local.JumpPage)

        QMetaObject.connectSlotsByName(Local)
    # setupUi

    def retranslateUi(self, Local):
        Local.setWindowTitle(QCoreApplication.translate("Local", u"\u672c\u5730\u6f2b\u753b", None))
        self.label.setText(QCoreApplication.translate("Local", u"\u641c\u7d22\uff1a", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Local", u"\u641c\u7d22\u672c\u5730\u6f2b\u753b\u6807\u9898...", None))
        self.delAll.setText(QCoreApplication.translate("Local", u"\u6279\u91cf\u5220\u9664", None))
        self.toolButton.setText(QCoreApplication.translate("Local", u"\u5bfc\u5165", None))
        self.sortKeyCombox.setItemText(0, QCoreApplication.translate("Local", u"\u4e0a\u6b21\u9605\u8bfb\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(1, QCoreApplication.translate("Local", u"\u6dfb\u52a0\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(2, QCoreApplication.translate("Local", u"\u540d\u79f0", None))

        self.sortIdCombox.setItemText(0, QCoreApplication.translate("Local", u"\u964d\u5e8f", None))
        self.sortIdCombox.setItemText(1, QCoreApplication.translate("Local", u"\u5347\u5e8f", None))

        self.msgLabel.setText("")
        self.nums.setText(QCoreApplication.translate("Local", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("Local", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("Local", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Local", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

