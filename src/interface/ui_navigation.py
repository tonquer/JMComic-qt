# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_navigation.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCommandLinkButton, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from component.label.head_label import HeadLabel
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_Navigation(object):
    def setupUi(self, Navigation):
        if not Navigation.objectName():
            Navigation.setObjectName(u"Navigation")
        Navigation.resize(430, 516)
        self.verticalLayout = QVBoxLayout(Navigation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topWidget = QWidget(Navigation)
        self.topWidget.setObjectName(u"topWidget")
        self.verticalLayout_4 = QVBoxLayout(self.topWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.picLabel = HeadLabel(self.topWidget)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(100, 100))
        self.picLabel.setMaximumSize(QSize(100, 100))
        self.picLabel.setPixmap(QPixmap(u":/png/icon/placeholder_avatar.png"))
        self.picLabel.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.picLabel, 0, Qt.AlignHCenter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton = QPushButton(self.topWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.signButton = QPushButton(self.topWidget)
        self.signButton.setObjectName(u"signButton")
        sizePolicy.setHeightForWidth(self.signButton.sizePolicy().hasHeightForWidth())
        self.signButton.setSizePolicy(sizePolicy)
        self.signButton.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.signButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.nameLabel = QLabel(self.topWidget)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout_3.addWidget(self.nameLabel)

        self.titleLabel = QLabel(self.topWidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setMinimumSize(QSize(150, 0))
        font = QFont()
        font.setPointSize(7)
        self.titleLabel.setFont(font)

        self.horizontalLayout_3.addWidget(self.titleLabel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.topWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.coins = QLabel(self.topWidget)
        self.coins.setObjectName(u"coins")

        self.horizontalLayout_2.addWidget(self.coins)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.expLabel = QLabel(self.topWidget)
        self.expLabel.setObjectName(u"expLabel")

        self.horizontalLayout.addWidget(self.expLabel)

        self.levelLabel = QLabel(self.topWidget)
        self.levelLabel.setObjectName(u"levelLabel")

        self.horizontalLayout.addWidget(self.levelLabel)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(self.topWidget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.favorite = QLabel(self.topWidget)
        self.favorite.setObjectName(u"favorite")

        self.horizontalLayout_5.addWidget(self.favorite)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.topWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.proxyName = QCommandLinkButton(self.topWidget)
        self.proxyName.setObjectName(u"proxyName")

        self.horizontalLayout_6.addWidget(self.proxyName)

        self.proxyImgName = QCommandLinkButton(self.topWidget)
        self.proxyImgName.setObjectName(u"proxyImgName")

        self.horizontalLayout_6.addWidget(self.proxyImgName)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.topWidget)

        self.scrollArea = SmoothScrollArea(Navigation)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 393, 746))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 9)
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.collectButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup = QButtonGroup(Navigation)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.collectButton)
        self.collectButton.setObjectName(u"collectButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.collectButton.sizePolicy().hasHeightForWidth())
        self.collectButton.setSizePolicy(sizePolicy1)
        self.collectButton.setMinimumSize(QSize(150, 40))
        self.collectButton.setFocusPolicy(Qt.NoFocus)
        icon = QIcon()
        icon.addFile(u":/images/menu/Contact.png", QSize(), QIcon.Normal, QIcon.Off)
        self.collectButton.setIcon(icon)
        self.collectButton.setIconSize(QSize(32, 32))
        self.collectButton.setCheckable(True)
        self.collectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.collectButton)

        self.localCollectButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.localCollectButton)
        self.localCollectButton.setObjectName(u"localCollectButton")
        sizePolicy1.setHeightForWidth(self.localCollectButton.sizePolicy().hasHeightForWidth())
        self.localCollectButton.setSizePolicy(sizePolicy1)
        self.localCollectButton.setMinimumSize(QSize(150, 40))
        self.localCollectButton.setFocusPolicy(Qt.NoFocus)
        self.localCollectButton.setIcon(icon)
        self.localCollectButton.setIconSize(QSize(32, 32))
        self.localCollectButton.setCheckable(True)
        self.localCollectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.localCollectButton)

        self.myCommentButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.myCommentButton)
        self.myCommentButton.setObjectName(u"myCommentButton")
        sizePolicy1.setHeightForWidth(self.myCommentButton.sizePolicy().hasHeightForWidth())
        self.myCommentButton.setSizePolicy(sizePolicy1)
        self.myCommentButton.setMinimumSize(QSize(150, 40))
        self.myCommentButton.setFocusPolicy(Qt.NoFocus)
        self.myCommentButton.setIcon(icon)
        self.myCommentButton.setIconSize(QSize(32, 32))
        self.myCommentButton.setCheckable(True)
        self.myCommentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.myCommentButton)

        self.historyButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.historyButton)
        self.historyButton.setObjectName(u"historyButton")
        sizePolicy1.setHeightForWidth(self.historyButton.sizePolicy().hasHeightForWidth())
        self.historyButton.setSizePolicy(sizePolicy1)
        self.historyButton.setMinimumSize(QSize(150, 40))
        self.historyButton.setFocusPolicy(Qt.NoFocus)
        self.historyButton.setIcon(icon)
        self.historyButton.setIconSize(QSize(32, 32))
        self.historyButton.setCheckable(True)
        self.historyButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.historyButton)

        self.remoteHistoryButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.remoteHistoryButton)
        self.remoteHistoryButton.setObjectName(u"remoteHistoryButton")
        sizePolicy1.setHeightForWidth(self.remoteHistoryButton.sizePolicy().hasHeightForWidth())
        self.remoteHistoryButton.setSizePolicy(sizePolicy1)
        self.remoteHistoryButton.setMinimumSize(QSize(150, 40))
        self.remoteHistoryButton.setFocusPolicy(Qt.NoFocus)
        self.remoteHistoryButton.setIcon(icon)
        self.remoteHistoryButton.setIconSize(QSize(32, 32))
        self.remoteHistoryButton.setCheckable(True)
        self.remoteHistoryButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.remoteHistoryButton)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.indexButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.indexButton)
        self.indexButton.setObjectName(u"indexButton")
        sizePolicy1.setHeightForWidth(self.indexButton.sizePolicy().hasHeightForWidth())
        self.indexButton.setSizePolicy(sizePolicy1)
        self.indexButton.setMinimumSize(QSize(150, 40))
        self.indexButton.setFocusPolicy(Qt.NoFocus)
        self.indexButton.setIcon(icon)
        self.indexButton.setIconSize(QSize(32, 32))
        self.indexButton.setCheckable(True)
        self.indexButton.setChecked(True)
        self.indexButton.setPopupMode(QToolButton.DelayedPopup)
        self.indexButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.indexButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.indexButton)

        self.searchButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.searchButton)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy1.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy1)
        self.searchButton.setMinimumSize(QSize(150, 40))
        self.searchButton.setFocusPolicy(Qt.NoFocus)
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QSize(32, 32))
        self.searchButton.setCheckable(True)
        self.searchButton.setPopupMode(QToolButton.DelayedPopup)
        self.searchButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.searchButton)

        self.categoryButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.categoryButton)
        self.categoryButton.setObjectName(u"categoryButton")
        sizePolicy1.setHeightForWidth(self.categoryButton.sizePolicy().hasHeightForWidth())
        self.categoryButton.setSizePolicy(sizePolicy1)
        self.categoryButton.setMinimumSize(QSize(150, 40))
        self.categoryButton.setFocusPolicy(Qt.NoFocus)
        self.categoryButton.setIcon(icon)
        self.categoryButton.setIconSize(QSize(32, 32))
        self.categoryButton.setCheckable(True)
        self.categoryButton.setPopupMode(QToolButton.DelayedPopup)
        self.categoryButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.categoryButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.categoryButton)

        self.weekButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.weekButton)
        self.weekButton.setObjectName(u"weekButton")
        sizePolicy1.setHeightForWidth(self.weekButton.sizePolicy().hasHeightForWidth())
        self.weekButton.setSizePolicy(sizePolicy1)
        self.weekButton.setMinimumSize(QSize(150, 40))
        self.weekButton.setFocusPolicy(Qt.NoFocus)
        self.weekButton.setIcon(icon)
        self.weekButton.setIconSize(QSize(32, 32))
        self.weekButton.setCheckable(True)
        self.weekButton.setPopupMode(QToolButton.DelayedPopup)
        self.weekButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.weekButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.weekButton)

        self.commentButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.commentButton)
        self.commentButton.setObjectName(u"commentButton")
        sizePolicy1.setHeightForWidth(self.commentButton.sizePolicy().hasHeightForWidth())
        self.commentButton.setSizePolicy(sizePolicy1)
        self.commentButton.setMinimumSize(QSize(150, 40))
        self.commentButton.setFocusPolicy(Qt.NoFocus)
        self.commentButton.setIcon(icon)
        self.commentButton.setIconSize(QSize(32, 32))
        self.commentButton.setCheckable(True)
        self.commentButton.setPopupMode(QToolButton.DelayedPopup)
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commentButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.commentButton)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.downloadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.downloadButton)
        self.downloadButton.setObjectName(u"downloadButton")
        sizePolicy1.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy1)
        self.downloadButton.setMinimumSize(QSize(150, 40))
        self.downloadButton.setFocusPolicy(Qt.NoFocus)
        self.downloadButton.setIcon(icon)
        self.downloadButton.setIconSize(QSize(32, 32))
        self.downloadButton.setCheckable(True)
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.downloadButton)

        self.nasButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.nasButton)
        self.nasButton.setObjectName(u"nasButton")
        sizePolicy1.setHeightForWidth(self.nasButton.sizePolicy().hasHeightForWidth())
        self.nasButton.setSizePolicy(sizePolicy1)
        self.nasButton.setMinimumSize(QSize(150, 40))
        self.nasButton.setFocusPolicy(Qt.NoFocus)
        self.nasButton.setIcon(icon)
        self.nasButton.setIconSize(QSize(32, 32))
        self.nasButton.setCheckable(True)
        self.nasButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.nasButton)

        self.localReadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.localReadButton)
        self.localReadButton.setObjectName(u"localReadButton")
        sizePolicy1.setHeightForWidth(self.localReadButton.sizePolicy().hasHeightForWidth())
        self.localReadButton.setSizePolicy(sizePolicy1)
        self.localReadButton.setMinimumSize(QSize(0, 40))
        self.localReadButton.setFocusPolicy(Qt.NoFocus)
        self.localReadButton.setIcon(icon)
        self.localReadButton.setIconSize(QSize(32, 32))
        self.localReadButton.setCheckable(True)
        self.localReadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.localReadButton)

        self.waifu2xButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.waifu2xButton)
        self.waifu2xButton.setObjectName(u"waifu2xButton")
        sizePolicy1.setHeightForWidth(self.waifu2xButton.sizePolicy().hasHeightForWidth())
        self.waifu2xButton.setSizePolicy(sizePolicy1)
        self.waifu2xButton.setMinimumSize(QSize(150, 40))
        self.waifu2xButton.setFocusPolicy(Qt.NoFocus)
        self.waifu2xButton.setIcon(icon)
        self.waifu2xButton.setIconSize(QSize(32, 32))
        self.waifu2xButton.setCheckable(True)
        self.waifu2xButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.waifu2xButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.tailWidget = QWidget(Navigation)
        self.tailWidget.setObjectName(u"tailWidget")
        self.verticalLayout_5 = QVBoxLayout(self.tailWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.helpButton = QToolButton(self.tailWidget)
        self.buttonGroup.addButton(self.helpButton)
        self.helpButton.setObjectName(u"helpButton")
        sizePolicy1.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy1)
        self.helpButton.setMinimumSize(QSize(0, 40))
        self.helpButton.setFocusPolicy(Qt.NoFocus)
        self.helpButton.setIcon(icon)
        self.helpButton.setIconSize(QSize(32, 32))
        self.helpButton.setCheckable(True)
        self.helpButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_5.addWidget(self.helpButton)

        self.settingButton = QToolButton(self.tailWidget)
        self.buttonGroup.addButton(self.settingButton)
        self.settingButton.setObjectName(u"settingButton")
        sizePolicy1.setHeightForWidth(self.settingButton.sizePolicy().hasHeightForWidth())
        self.settingButton.setSizePolicy(sizePolicy1)
        self.settingButton.setMinimumSize(QSize(150, 40))
        self.settingButton.setFocusPolicy(Qt.NoFocus)
        self.settingButton.setStyleSheet(u"")
        self.settingButton.setIcon(icon)
        self.settingButton.setIconSize(QSize(32, 32))
        self.settingButton.setCheckable(True)
        self.settingButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.settingButton.setAutoRaise(False)

        self.verticalLayout_5.addWidget(self.settingButton)


        self.verticalLayout.addWidget(self.tailWidget)


        self.retranslateUi(Navigation)

        QMetaObject.connectSlotsByName(Navigation)
    # setupUi

    def retranslateUi(self, Navigation):
        Navigation.setWindowTitle(QCoreApplication.translate("Navigation", u"Form", None))
        self.picLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("Navigation", u"\u767b\u5f55", None))
        self.signButton.setText(QCoreApplication.translate("Navigation", u"\u6253\u5361", None))
        self.nameLabel.setText("")
        self.titleLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("Navigation", u"J Coins\uff1a", None))
        self.coins.setText("")
        self.expLabel.setText(QCoreApplication.translate("Navigation", u"\u7b49\u7ea7:", None))
        self.levelLabel.setText("")
        self.label_8.setText(QCoreApplication.translate("Navigation", u"\u6536\u85cf\u6570\uff1a", None))
        self.favorite.setText("")
        self.label_4.setText(QCoreApplication.translate("Navigation", u"\u5206\u6d41\uff1a", None))
        self.proxyName.setText("")
        self.proxyImgName.setText("")
        self.label.setText(QCoreApplication.translate("Navigation", u"\u7528\u6237", None))
        self.collectButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u6536\u85cf", None))
        self.localCollectButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u6536\u85cf", None))
        self.myCommentButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u8bc4\u8bba", None))
        self.historyButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u8bb0\u5f55", None))
        self.remoteHistoryButton.setText(QCoreApplication.translate("Navigation", u"\u89c2\u770b\u8bb0\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("Navigation", u"\u5bfc\u822a", None))
        self.indexButton.setText(QCoreApplication.translate("Navigation", u"\u9996\u9875", None))
        self.searchButton.setText(QCoreApplication.translate("Navigation", u"\u641c\u7d22", None))
        self.categoryButton.setText(QCoreApplication.translate("Navigation", u"\u5206\u7c7b\u4e0e\u6392\u884c", None))
        self.weekButton.setText(QCoreApplication.translate("Navigation", u"\u6bcf\u5468\u5fc5\u770b", None))
        self.commentButton.setText(QCoreApplication.translate("Navigation", u"\u8bc4\u8bba", None))
        self.label_3.setText(QCoreApplication.translate("Navigation", u"\u5176\u4ed6", None))
        self.downloadButton.setText(QCoreApplication.translate("Navigation", u"\u4e0b\u8f7d", None))
        self.nasButton.setText(QCoreApplication.translate("Navigation", u"\u7f51\u7edc\u5b58\u50a8", None))
        self.localReadButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u6f2b\u753b", None))
        self.waifu2xButton.setText(QCoreApplication.translate("Navigation", u"\u56fe\u7247\u8d85\u5206", None))
        self.helpButton.setText(QCoreApplication.translate("Navigation", u"\u5e2e\u52a9", None))
        self.settingButton.setText(QCoreApplication.translate("Navigation", u"\u8bbe\u7f6e", None))
    # retranslateUi

