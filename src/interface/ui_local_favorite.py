# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_local_favorite.ui'
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

class Ui_LocalFavorite(object):
    def setupUi(self, LocalFavorite):
        if not LocalFavorite.objectName():
            LocalFavorite.setObjectName(u"LocalFavorite")
        LocalFavorite.resize(900, 560)
        self.gridLayout_2 = QVBoxLayout(LocalFavorite)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(12, 10, 12, 10)
        self.widget = QFrame(LocalFavorite)
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

        self.folderBox = QComboBox(self.widget)
        self.folderBox.setObjectName(u"folderBox")
        self.folderBox.setMinimumSize(QSize(124, 0))

        self.horizontalLayout_2.addWidget(self.folderBox)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.importButton = QPushButton(self.widget)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setMinimumSize(QSize(96, 0))

        self.horizontalLayout_2.addWidget(self.importButton)

        self.startEpsUpdate = QPushButton(self.widget)
        self.startEpsUpdate.setObjectName(u"startEpsUpdate")
        self.startEpsUpdate.setMinimumSize(QSize(88, 0))
        self.startEpsUpdate.setProperty(u"variant", u"primary")

        self.horizontalLayout_2.addWidget(self.startEpsUpdate)


        self.gridLayout_2.addWidget(self.widget)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.bookList = ComicListWidget(LocalFavorite)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, -1)
        self.sortKeyCombox = QComboBox(LocalFavorite)
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.addItem("")
        self.sortKeyCombox.setObjectName(u"sortKeyCombox")
        self.sortKeyCombox.setEnabled(True)
        self.sortKeyCombox.setMinimumSize(QSize(110, 0))

        self.horizontalLayout.addWidget(self.sortKeyCombox)

        self.sortIdCombox = QComboBox(LocalFavorite)
        self.sortIdCombox.addItem("")
        self.sortIdCombox.addItem("")
        self.sortIdCombox.setObjectName(u"sortIdCombox")
        self.sortIdCombox.setEnabled(True)
        self.sortIdCombox.setMinimumSize(QSize(76, 0))

        self.horizontalLayout.addWidget(self.sortIdCombox)

        self.msgLabel = QLabel(LocalFavorite)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.tipText = QLabel(LocalFavorite)
        self.tipText.setObjectName(u"tipText")
        self.tipText.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.tipText)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.nums = QLabel(LocalFavorite)
        self.nums.setObjectName(u"nums")
        self.nums.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(LocalFavorite)
        self.pages.setObjectName(u"pages")
        self.pages.setProperty(u"role", u"muted")

        self.horizontalLayout.addWidget(self.pages)

        self.spinBox = QSpinBox(LocalFavorite)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(68, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.jumpButton = QPushButton(LocalFavorite)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(68, 0))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2.setStretch(1, 1)

        self.retranslateUi(LocalFavorite)
        self.jumpButton.clicked.connect(LocalFavorite.JumpPage)

        QMetaObject.connectSlotsByName(LocalFavorite)
    # setupUi

    def retranslateUi(self, LocalFavorite):
        LocalFavorite.setWindowTitle(QCoreApplication.translate("LocalFavorite", u"\u672c\u5730\u6536\u85cf", None))
        self.label.setText(QCoreApplication.translate("LocalFavorite", u"\u641c\u7d22\uff1a", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("LocalFavorite", u"\u641c\u7d22\u672c\u5730\u6536\u85cf\u6807\u9898\u6216 ID\u2026", None))
        self.importButton.setText(QCoreApplication.translate("LocalFavorite", u"\u4ece\u6536\u85cf\u5bfc\u5165", None))
        self.startEpsUpdate.setText(QCoreApplication.translate("LocalFavorite", u"\u83b7\u53d6\u66f4\u65b0", None))
        self.sortKeyCombox.setItemText(0, QCoreApplication.translate("LocalFavorite", u"\u66f4\u65b0\u65f6\u95f4", None))
        self.sortKeyCombox.setItemText(1, QCoreApplication.translate("LocalFavorite", u"\u6536\u85cf\u65f6\u95f4", None))

        self.sortIdCombox.setItemText(0, QCoreApplication.translate("LocalFavorite", u"\u964d\u5e8f", None))
        self.sortIdCombox.setItemText(1, QCoreApplication.translate("LocalFavorite", u"\u5347\u5e8f", None))

        self.msgLabel.setText("")
        self.tipText.setText("")
        self.nums.setText(QCoreApplication.translate("LocalFavorite", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("LocalFavorite", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("LocalFavorite", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("LocalFavorite", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

