# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_navigation.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from component.button.switch_button import SwitchButton
from component.label.head_label import HeadLabel
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
from component.widget.mini_node_title_frame import MiniNodeTileFrame

class Ui_Navigation(object):
    def setupUi(self, Navigation):
        if not Navigation.objectName():
            Navigation.setObjectName(u"Navigation")
        Navigation.resize(408, 1043)
        self.verticalLayout = QVBoxLayout(Navigation)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topWidget = QWidget(Navigation)
        self.topWidget.setObjectName(u"topWidget")
        self.verticalLayout_4 = QVBoxLayout(self.topWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.picLabel = HeadLabel(self.topWidget)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(72, 72))
        self.picLabel.setMaximumSize(QSize(72, 72))
        self.picLabel.setPixmap(QPixmap(u":/png/icon/placeholder_avatar.png"))
        self.picLabel.setScaledContents(True)

        self.verticalLayout_4.addWidget(self.picLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton = QPushButton(self.topWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.signButton = QPushButton(self.topWidget)
        self.signButton.setObjectName(u"signButton")
        sizePolicy.setHeightForWidth(self.signButton.sizePolicy().hasHeightForWidth())
        self.signButton.setSizePolicy(sizePolicy)
        self.signButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.proxyName = MiniNodeTileFrame(self.topWidget)
        self.proxyName.setObjectName(u"proxyName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.proxyName.sizePolicy().hasHeightForWidth())
        self.proxyName.setSizePolicy(sizePolicy1)
        self.proxyName.setFrameShape(QFrame.Shape.StyledPanel)
        self.proxyName.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.proxyName, 3, 1, 1, 1)

        self.offlineButton = SwitchButton(self.topWidget)
        self.offlineButton.setObjectName(u"offlineButton")

        self.gridLayout_2.addWidget(self.offlineButton, 5, 1, 1, 1)

        self.label_9 = QLabel(self.topWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 6, 0, 1, 1)

        self.label_5 = QLabel(self.topWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)

        self.expLabel = QLabel(self.topWidget)
        self.expLabel.setObjectName(u"expLabel")

        self.gridLayout_2.addWidget(self.expLabel, 1, 0, 1, 1)

        self.label_8 = QLabel(self.topWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 2, 0, 1, 1)

        self.hideButton = QPushButton(self.topWidget)
        self.hideButton.setObjectName(u"hideButton")

        self.gridLayout_2.addWidget(self.hideButton, 6, 1, 1, 1)

        self.favorite = QLabel(self.topWidget)
        self.favorite.setObjectName(u"favorite")

        self.gridLayout_2.addWidget(self.favorite, 2, 1, 1, 1)

        self.label_7 = QLabel(self.topWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(60, 0))

        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)

        self.label_4 = QLabel(self.topWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(60, 0))

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.levelLabel = QLabel(self.topWidget)
        self.levelLabel.setObjectName(u"levelLabel")

        self.gridLayout_2.addWidget(self.levelLabel, 1, 1, 1, 1)

        self.proxyImgName = MiniNodeTileFrame(self.topWidget)
        self.proxyImgName.setObjectName(u"proxyImgName")
        sizePolicy1.setHeightForWidth(self.proxyImgName.sizePolicy().hasHeightForWidth())
        self.proxyImgName.setSizePolicy(sizePolicy1)
        self.proxyImgName.setFrameShape(QFrame.Shape.StyledPanel)
        self.proxyImgName.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_2.addWidget(self.proxyImgName, 4, 1, 1, 1)

        self.label_6 = QLabel(self.topWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.coins = QLabel(self.topWidget)
        self.coins.setObjectName(u"coins")

        self.gridLayout_2.addWidget(self.coins, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.verticalLayout.addWidget(self.topWidget)

        self.scrollArea = SmoothScrollArea(Navigation)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 376, 692))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(1)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.collectButton.sizePolicy().hasHeightForWidth())
        self.collectButton.setSizePolicy(sizePolicy2)
        self.collectButton.setMinimumSize(QSize(150, 40))
        self.collectButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.collectButton.setIconSize(QSize(18, 18))
        self.collectButton.setCheckable(True)
        self.collectButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.collectButton)

        self.myCommentButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.myCommentButton)
        self.myCommentButton.setObjectName(u"myCommentButton")
        sizePolicy2.setHeightForWidth(self.myCommentButton.sizePolicy().hasHeightForWidth())
        self.myCommentButton.setSizePolicy(sizePolicy2)
        self.myCommentButton.setMinimumSize(QSize(150, 40))
        self.myCommentButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.myCommentButton.setIconSize(QSize(18, 18))
        self.myCommentButton.setCheckable(True)
        self.myCommentButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.myCommentButton)

        self.remoteHistoryButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.remoteHistoryButton)
        self.remoteHistoryButton.setObjectName(u"remoteHistoryButton")
        sizePolicy2.setHeightForWidth(self.remoteHistoryButton.sizePolicy().hasHeightForWidth())
        self.remoteHistoryButton.setSizePolicy(sizePolicy2)
        self.remoteHistoryButton.setMinimumSize(QSize(150, 40))
        self.remoteHistoryButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.remoteHistoryButton.setIconSize(QSize(18, 18))
        self.remoteHistoryButton.setCheckable(True)
        self.remoteHistoryButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.remoteHistoryButton)

        self.localCollectButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.localCollectButton)
        self.localCollectButton.setObjectName(u"localCollectButton")
        sizePolicy2.setHeightForWidth(self.localCollectButton.sizePolicy().hasHeightForWidth())
        self.localCollectButton.setSizePolicy(sizePolicy2)
        self.localCollectButton.setMinimumSize(QSize(150, 40))
        self.localCollectButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.localCollectButton.setIconSize(QSize(18, 18))
        self.localCollectButton.setCheckable(True)
        self.localCollectButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.localCollectButton)

        self.historyButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.historyButton)
        self.historyButton.setObjectName(u"historyButton")
        sizePolicy2.setHeightForWidth(self.historyButton.sizePolicy().hasHeightForWidth())
        self.historyButton.setSizePolicy(sizePolicy2)
        self.historyButton.setMinimumSize(QSize(150, 40))
        self.historyButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.historyButton.setIconSize(QSize(18, 18))
        self.historyButton.setCheckable(True)
        self.historyButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.historyButton)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.indexButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.indexButton)
        self.indexButton.setObjectName(u"indexButton")
        sizePolicy2.setHeightForWidth(self.indexButton.sizePolicy().hasHeightForWidth())
        self.indexButton.setSizePolicy(sizePolicy2)
        self.indexButton.setMinimumSize(QSize(150, 40))
        self.indexButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.indexButton.setIconSize(QSize(18, 18))
        self.indexButton.setCheckable(True)
        self.indexButton.setChecked(True)
        self.indexButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.indexButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.indexButton.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout_3.addWidget(self.indexButton)

        self.searchButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.searchButton)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy2.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy2)
        self.searchButton.setMinimumSize(QSize(150, 40))
        self.searchButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.searchButton.setIconSize(QSize(18, 18))
        self.searchButton.setCheckable(True)
        self.searchButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.searchButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.searchButton.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout_3.addWidget(self.searchButton)

        self.categoryButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.categoryButton)
        self.categoryButton.setObjectName(u"categoryButton")
        sizePolicy2.setHeightForWidth(self.categoryButton.sizePolicy().hasHeightForWidth())
        self.categoryButton.setSizePolicy(sizePolicy2)
        self.categoryButton.setMinimumSize(QSize(150, 40))
        self.categoryButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.categoryButton.setIconSize(QSize(18, 18))
        self.categoryButton.setCheckable(True)
        self.categoryButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.categoryButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.categoryButton.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout_3.addWidget(self.categoryButton)

        self.weekButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.weekButton)
        self.weekButton.setObjectName(u"weekButton")
        sizePolicy2.setHeightForWidth(self.weekButton.sizePolicy().hasHeightForWidth())
        self.weekButton.setSizePolicy(sizePolicy2)
        self.weekButton.setMinimumSize(QSize(150, 40))
        self.weekButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.weekButton.setIconSize(QSize(18, 18))
        self.weekButton.setCheckable(True)
        self.weekButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.weekButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.weekButton.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout_3.addWidget(self.weekButton)

        self.commentButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.commentButton)
        self.commentButton.setObjectName(u"commentButton")
        sizePolicy2.setHeightForWidth(self.commentButton.sizePolicy().hasHeightForWidth())
        self.commentButton.setSizePolicy(sizePolicy2)
        self.commentButton.setMinimumSize(QSize(150, 40))
        self.commentButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.commentButton.setIconSize(QSize(18, 18))
        self.commentButton.setCheckable(True)
        self.commentButton.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.commentButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.commentButton.setArrowType(Qt.ArrowType.NoArrow)

        self.verticalLayout_3.addWidget(self.commentButton)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.downloadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.downloadButton)
        self.downloadButton.setObjectName(u"downloadButton")
        sizePolicy2.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy2)
        self.downloadButton.setMinimumSize(QSize(150, 40))
        self.downloadButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.downloadButton.setIconSize(QSize(18, 18))
        self.downloadButton.setCheckable(True)
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.downloadButton)

        self.nasButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.nasButton)
        self.nasButton.setObjectName(u"nasButton")
        sizePolicy2.setHeightForWidth(self.nasButton.sizePolicy().hasHeightForWidth())
        self.nasButton.setSizePolicy(sizePolicy2)
        self.nasButton.setMinimumSize(QSize(150, 40))
        self.nasButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.nasButton.setIconSize(QSize(18, 18))
        self.nasButton.setCheckable(True)
        self.nasButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.nasButton)

        self.localReadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.localReadButton)
        self.localReadButton.setObjectName(u"localReadButton")
        sizePolicy2.setHeightForWidth(self.localReadButton.sizePolicy().hasHeightForWidth())
        self.localReadButton.setSizePolicy(sizePolicy2)
        self.localReadButton.setMinimumSize(QSize(0, 40))
        self.localReadButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.localReadButton.setIconSize(QSize(18, 18))
        self.localReadButton.setCheckable(True)
        self.localReadButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.localReadButton)

        self.waifu2xButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.waifu2xButton)
        self.waifu2xButton.setObjectName(u"waifu2xButton")
        sizePolicy2.setHeightForWidth(self.waifu2xButton.sizePolicy().hasHeightForWidth())
        self.waifu2xButton.setSizePolicy(sizePolicy2)
        self.waifu2xButton.setMinimumSize(QSize(150, 40))
        self.waifu2xButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.waifu2xButton.setIconSize(QSize(18, 18))
        self.waifu2xButton.setCheckable(True)
        self.waifu2xButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.waifu2xButton)

        self.batchSrButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.batchSrButton)
        self.batchSrButton.setObjectName(u"batchSrButton")
        sizePolicy2.setHeightForWidth(self.batchSrButton.sizePolicy().hasHeightForWidth())
        self.batchSrButton.setSizePolicy(sizePolicy2)
        self.batchSrButton.setMinimumSize(QSize(150, 40))
        self.batchSrButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.batchSrButton.setIconSize(QSize(18, 18))
        self.batchSrButton.setCheckable(True)
        self.batchSrButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.batchSrButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        sizePolicy2.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy2)
        self.helpButton.setMinimumSize(QSize(0, 40))
        self.helpButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.helpButton.setIconSize(QSize(18, 18))
        self.helpButton.setCheckable(True)
        self.helpButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout_5.addWidget(self.helpButton)

        self.settingButton = QToolButton(self.tailWidget)
        self.buttonGroup.addButton(self.settingButton)
        self.settingButton.setObjectName(u"settingButton")
        sizePolicy2.setHeightForWidth(self.settingButton.sizePolicy().hasHeightForWidth())
        self.settingButton.setSizePolicy(sizePolicy2)
        self.settingButton.setMinimumSize(QSize(150, 40))
        self.settingButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.settingButton.setStyleSheet(u"")
        self.settingButton.setIconSize(QSize(18, 18))
        self.settingButton.setCheckable(True)
        self.settingButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
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
        self.label_9.setText(QCoreApplication.translate("Navigation", u"\u5c4f\u853d\u8bcd\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Navigation", u"\u79bb\u7ebf\u6a21\u5f0f\uff1a", None))
        self.expLabel.setText(QCoreApplication.translate("Navigation", u"\u7b49\u7ea7:", None))
        self.label_8.setText(QCoreApplication.translate("Navigation", u"\u6536\u85cf\u6570\uff1a", None))
        self.hideButton.setText("")
        self.favorite.setText("")
        self.label_7.setText(QCoreApplication.translate("Navigation", u"\u56fe\u7247\u5206\u6d41\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Navigation", u"API\u5206\u6d41\uff1a", None))
        self.levelLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("Navigation", u"J Coins\uff1a", None))
        self.coins.setText("")
        self.label.setText(QCoreApplication.translate("Navigation", u"\u7528\u6237", None))
        self.collectButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u6536\u85cf", None))
        self.myCommentButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u8bc4\u8bba", None))
        self.remoteHistoryButton.setText(QCoreApplication.translate("Navigation", u"\u89c2\u770b\u8bb0\u5f55", None))
        self.localCollectButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u6536\u85cf", None))
        self.historyButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u8bb0\u5f55", None))
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
        self.batchSrButton.setText(QCoreApplication.translate("Navigation", u"\u6279\u91cf\u8d85\u5206", None))
        self.helpButton.setText(QCoreApplication.translate("Navigation", u"\u5e2e\u52a9", None))
        self.settingButton.setText(QCoreApplication.translate("Navigation", u"\u8bbe\u7f6e", None))
    # retranslateUi

