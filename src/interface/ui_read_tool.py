# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_read_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.box.wheel_slider import WheelSlider
from component.box.wheel_spin_box import WheelSpinBox
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_ReadImg(object):
    def setupUi(self, ReadImg):
        if not ReadImg.objectName():
            ReadImg.setObjectName(u"ReadImg")
        ReadImg.resize(400, 820)
        ReadImg.setAutoFillBackground(False)
        ReadImg.setStyleSheet(u"")
        self.drawerRootLayout = QHBoxLayout(ReadImg)
        self.drawerRootLayout.setSpacing(0)
        self.drawerRootLayout.setObjectName(u"drawerRootLayout")
        self.drawerRootLayout.setContentsMargins(0, 0, 0, 0)
        self.drawerDivider = QFrame(ReadImg)
        self.drawerDivider.setObjectName(u"drawerDivider")
        self.drawerDivider.setFrameShape(QFrame.Shape.VLine)
        self.drawerDivider.setFrameShadow(QFrame.Shadow.Sunken)

        self.drawerRootLayout.addWidget(self.drawerDivider)

        self.drawerContentLayout = QVBoxLayout()
        self.drawerContentLayout.setSpacing(8)
        self.drawerContentLayout.setObjectName(u"drawerContentLayout")
        self.drawerContentLayout.setContentsMargins(8, 8, 8, 8)
        self.scrollArea22 = SmoothScrollArea(ReadImg)
        self.scrollArea22.setObjectName(u"scrollArea22")
        self.scrollArea22.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea22.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -81, 367, 751))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 4, 2)
        self.infoCard = QFrame(self.scrollAreaWidgetContents)
        self.infoCard.setObjectName(u"infoCard")
        self.infoCard.setProperty(u"role", u"card")
        self.infoCardLayout = QVBoxLayout(self.infoCard)
        self.infoCardLayout.setSpacing(8)
        self.infoCardLayout.setObjectName(u"infoCardLayout")
        self.infoCardLayout.setContentsMargins(12, 10, 12, 12)
        self.label_4 = QLabel(self.infoCard)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setProperty(u"role", u"sectionTitle")

        self.infoCardLayout.addWidget(self.label_4)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setVerticalSpacing(6)
        self.epsLabel = QLabel(self.infoCard)
        self.epsLabel.setObjectName(u"epsLabel")
        self.epsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.epsLabel.setProperty(u"role", u"muted")

        self.gridLayout_3.addWidget(self.epsLabel, 0, 0, 1, 1)

        self.epsLabel2 = QLabel(self.infoCard)
        self.epsLabel2.setObjectName(u"epsLabel2")
        self.epsLabel2.setWordWrap(True)

        self.gridLayout_3.addWidget(self.epsLabel2, 0, 1, 1, 1)

        self.resolutionLabel = QLabel(self.infoCard)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.resolutionLabel.setProperty(u"role", u"muted")

        self.gridLayout_3.addWidget(self.resolutionLabel, 1, 0, 1, 1)

        self.resolutionLabel2 = QLabel(self.infoCard)
        self.resolutionLabel2.setObjectName(u"resolutionLabel2")
        self.resolutionLabel2.setWordWrap(True)

        self.gridLayout_3.addWidget(self.resolutionLabel2, 1, 1, 1, 1)

        self.sizeLabel = QLabel(self.infoCard)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.sizeLabel.setProperty(u"role", u"muted")

        self.gridLayout_3.addWidget(self.sizeLabel, 2, 0, 1, 1)

        self.sizeLabel2 = QLabel(self.infoCard)
        self.sizeLabel2.setObjectName(u"sizeLabel2")
        self.sizeLabel2.setWordWrap(True)

        self.gridLayout_3.addWidget(self.sizeLabel2, 2, 1, 1, 1)

        self.stateLable = QLabel(self.infoCard)
        self.stateLable.setObjectName(u"stateLable")
        self.stateLable.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.stateLable.setProperty(u"role", u"muted")

        self.gridLayout_3.addWidget(self.stateLable, 3, 0, 1, 1)

        self.stateLable2 = QLabel(self.infoCard)
        self.stateLable2.setObjectName(u"stateLable2")
        self.stateLable2.setWordWrap(True)

        self.gridLayout_3.addWidget(self.stateLable2, 3, 1, 1, 1)

        self.gridLayout_3.setColumnStretch(1, 1)

        self.infoCardLayout.addLayout(self.gridLayout_3)


        self.verticalLayout_2.addWidget(self.infoCard)

        self.waifuCard = QFrame(self.scrollAreaWidgetContents)
        self.waifuCard.setObjectName(u"waifuCard")
        self.waifuCard.setProperty(u"role", u"card")
        self.waifuCardLayout = QVBoxLayout(self.waifuCard)
        self.waifuCardLayout.setSpacing(8)
        self.waifuCardLayout.setObjectName(u"waifuCardLayout")
        self.waifuCardLayout.setContentsMargins(12, 10, 12, 12)
        self.waifuHeaderLayout = QHBoxLayout()
        self.waifuHeaderLayout.setSpacing(8)
        self.waifuHeaderLayout.setObjectName(u"waifuHeaderLayout")
        self.label = QLabel(self.waifuCard)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"sectionTitle")

        self.waifuHeaderLayout.addWidget(self.label)

        self.waifuHeaderSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.waifuHeaderLayout.addItem(self.waifuHeaderSpacer)

        self.waifu2xSave = QPushButton(self.waifuCard)
        self.waifu2xSave.setObjectName(u"waifu2xSave")

        self.waifuHeaderLayout.addWidget(self.waifu2xSave)

        self.waifu2xCancle = QPushButton(self.waifuCard)
        self.waifu2xCancle.setObjectName(u"waifu2xCancle")
        self.waifu2xCancle.setProperty(u"variant", u"primary")

        self.waifuHeaderLayout.addWidget(self.waifu2xCancle)


        self.waifuCardLayout.addLayout(self.waifuHeaderLayout)

        self.waifuSwitchRow1 = QHBoxLayout()
        self.waifuSwitchRow1.setSpacing(14)
        self.waifuSwitchRow1.setObjectName(u"waifuSwitchRow1")
        self.checkBox = QCheckBox(self.waifuCard)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.waifuSwitchRow1.addWidget(self.checkBox)

        self.curWaifu2x = QCheckBox(self.waifuCard)
        self.curWaifu2x.setObjectName(u"curWaifu2x")

        self.waifuSwitchRow1.addWidget(self.curWaifu2x)

        self.waifuSwitchSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.waifuSwitchRow1.addItem(self.waifuSwitchSpacer)


        self.waifuCardLayout.addLayout(self.waifuSwitchRow1)

        self.preDownWaifu2x = QCheckBox(self.waifuCard)
        self.preDownWaifu2x.setObjectName(u"preDownWaifu2x")

        self.waifuCardLayout.addWidget(self.preDownWaifu2x)

        self.line = QFrame(self.waifuCard)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.waifuCardLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(6)
        self.label_3 = QLabel(self.waifuCard)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.scaleLabel = QLabel(self.waifuCard)
        self.scaleLabel.setObjectName(u"scaleLabel")

        self.horizontalLayout_6.addWidget(self.scaleLabel)

        self.scaleBox = WheelDoubleSpinBox(self.waifuCard)
        self.scaleBox.setObjectName(u"scaleBox")
        self.scaleBox.setDecimals(1)
        self.scaleBox.setMaximum(32.000000000000000)
        self.scaleBox.setSingleStep(0.100000000000000)
        self.scaleBox.setValue(2.000000000000000)

        self.horizontalLayout_6.addWidget(self.scaleBox)


        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)

        self.label_8 = QLabel(self.waifuCard)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.modelNameButton = QPushButton(self.waifuCard)
        self.modelNameButton.setObjectName(u"modelNameButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelNameButton.sizePolicy().hasHeightForWidth())
        self.modelNameButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.modelNameButton)


        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 1, 1, 1)

        self.label_9 = QLabel(self.waifuCard)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_9.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.gpuLabel = QLabel(self.waifuCard)
        self.gpuLabel.setObjectName(u"gpuLabel")
        self.gpuLabel.setWordWrap(True)

        self.gridLayout.addWidget(self.gpuLabel, 2, 1, 1, 1)

        self.resolutionWaifu = QLabel(self.waifuCard)
        self.resolutionWaifu.setObjectName(u"resolutionWaifu")
        self.resolutionWaifu.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.resolutionWaifu, 3, 0, 1, 1)

        self.waifu2xRes = QLabel(self.waifuCard)
        self.waifu2xRes.setObjectName(u"waifu2xRes")
        self.waifu2xRes.setWordWrap(True)

        self.gridLayout.addWidget(self.waifu2xRes, 3, 1, 1, 1)

        self.sizeWaifu = QLabel(self.waifuCard)
        self.sizeWaifu.setObjectName(u"sizeWaifu")
        self.sizeWaifu.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.sizeWaifu, 4, 0, 1, 1)

        self.waifu2xSize = QLabel(self.waifuCard)
        self.waifu2xSize.setObjectName(u"waifu2xSize")
        self.waifu2xSize.setWordWrap(True)

        self.gridLayout.addWidget(self.waifu2xSize, 4, 1, 1, 1)

        self.tickLabel = QLabel(self.waifuCard)
        self.tickLabel.setObjectName(u"tickLabel")
        self.tickLabel.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.tickLabel, 5, 0, 1, 1)

        self.waifu2xTick = QLabel(self.waifuCard)
        self.waifu2xTick.setObjectName(u"waifu2xTick")
        self.waifu2xTick.setWordWrap(True)

        self.gridLayout.addWidget(self.waifu2xTick, 5, 1, 1, 1)

        self.stateWaifu = QLabel(self.waifuCard)
        self.stateWaifu.setObjectName(u"stateWaifu")
        self.stateWaifu.setProperty(u"role", u"muted")

        self.gridLayout.addWidget(self.stateWaifu, 6, 0, 1, 1)

        self.waifu2xStatus = QLabel(self.waifuCard)
        self.waifu2xStatus.setObjectName(u"waifu2xStatus")
        self.waifu2xStatus.setWordWrap(True)

        self.gridLayout.addWidget(self.waifu2xStatus, 6, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)

        self.waifuCardLayout.addLayout(self.gridLayout)


        self.verticalLayout_2.addWidget(self.waifuCard)

        self.readCard = QFrame(self.scrollAreaWidgetContents)
        self.readCard.setObjectName(u"readCard")
        self.readCard.setProperty(u"role", u"card")
        self.readCardLayout = QVBoxLayout(self.readCard)
        self.readCardLayout.setSpacing(8)
        self.readCardLayout.setObjectName(u"readCardLayout")
        self.readCardLayout.setContentsMargins(12, 10, 12, 12)
        self.label_6 = QLabel(self.readCard)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setProperty(u"role", u"sectionTitle")

        self.readCardLayout.addWidget(self.label_6)

        self.readGridLayout = QGridLayout()
        self.readGridLayout.setObjectName(u"readGridLayout")
        self.readGridLayout.setHorizontalSpacing(10)
        self.readGridLayout.setVerticalSpacing(8)
        self.label_5 = QLabel(self.readCard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setProperty(u"role", u"muted")

        self.readGridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.comboBox = WheelComboBox(self.readCard)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)

        self.readGridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.zoomLabel = QLabel(self.readCard)
        self.zoomLabel.setObjectName(u"zoomLabel")
        self.zoomLabel.setProperty(u"role", u"muted")

        self.readGridLayout.addWidget(self.zoomLabel, 1, 0, 1, 1)

        self.zoomSlider = WheelSlider(self.readCard)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setMinimum(10)
        self.zoomSlider.setMaximum(200)
        self.zoomSlider.setSingleStep(10)
        self.zoomSlider.setValue(120)
        self.zoomSlider.setOrientation(Qt.Orientation.Horizontal)

        self.readGridLayout.addWidget(self.zoomSlider, 1, 1, 1, 1)

        self.readGridLayout.setColumnStretch(1, 1)

        self.readCardLayout.addLayout(self.readGridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(14)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.animeBox = QCheckBox(self.readCard)
        self.animeBox.setObjectName(u"animeBox")
        self.animeBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.animeBox)

        self.switchDouble = QCheckBox(self.readCard)
        self.switchDouble.setObjectName(u"switchDouble")

        self.horizontalLayout_2.addWidget(self.switchDouble)

        self.readSwitchSpacer = QSpacerItem(0, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.readSwitchSpacer)


        self.readCardLayout.addLayout(self.horizontalLayout_2)

        self.openGLBox = QCheckBox(self.readCard)
        self.openGLBox.setObjectName(u"openGLBox")

        self.readCardLayout.addWidget(self.openGLBox)


        self.verticalLayout_2.addWidget(self.readCard)

        self.autoCard = QFrame(self.scrollAreaWidgetContents)
        self.autoCard.setObjectName(u"autoCard")
        self.autoCard.setProperty(u"role", u"card")
        self.autoCardLayout = QVBoxLayout(self.autoCard)
        self.autoCardLayout.setSpacing(8)
        self.autoCardLayout.setObjectName(u"autoCardLayout")
        self.autoCardLayout.setContentsMargins(12, 10, 12, 12)
        self.label_7 = QLabel(self.autoCard)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setProperty(u"role", u"sectionTitle")

        self.autoCardLayout.addWidget(self.label_7)

        self.autoGridLayout = QGridLayout()
        self.autoGridLayout.setObjectName(u"autoGridLayout")
        self.autoGridLayout.setHorizontalSpacing(10)
        self.autoGridLayout.setVerticalSpacing(8)
        self.label_12 = QLabel(self.autoCard)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setProperty(u"role", u"muted")

        self.autoGridLayout.addWidget(self.label_12, 0, 0, 1, 1)

        self.scrollInitSpeed = WheelSpinBox(self.autoCard)
        self.scrollInitSpeed.setObjectName(u"scrollInitSpeed")
        sizePolicy.setHeightForWidth(self.scrollInitSpeed.sizePolicy().hasHeightForWidth())
        self.scrollInitSpeed.setSizePolicy(sizePolicy)
        self.scrollInitSpeed.setMinimum(1)
        self.scrollInitSpeed.setMaximum(4000)
        self.scrollInitSpeed.setValue(200)

        self.autoGridLayout.addWidget(self.scrollInitSpeed, 0, 1, 1, 1)

        self.label_10 = QLabel(self.autoCard)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setProperty(u"role", u"muted")

        self.autoGridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.scrollSpeed = WheelSpinBox(self.autoCard)
        self.scrollSpeed.setObjectName(u"scrollSpeed")
        sizePolicy.setHeightForWidth(self.scrollSpeed.sizePolicy().hasHeightForWidth())
        self.scrollSpeed.setSizePolicy(sizePolicy)
        self.scrollSpeed.setMinimum(1)
        self.scrollSpeed.setMaximum(4000)
        self.scrollSpeed.setValue(200)

        self.autoGridLayout.addWidget(self.scrollSpeed, 1, 1, 1, 1)

        self.label_11 = QLabel(self.autoCard)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setProperty(u"role", u"muted")

        self.autoGridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.turnSpeed = WheelDoubleSpinBox(self.autoCard)
        self.turnSpeed.setObjectName(u"turnSpeed")
        sizePolicy.setHeightForWidth(self.turnSpeed.sizePolicy().hasHeightForWidth())
        self.turnSpeed.setSizePolicy(sizePolicy)
        self.turnSpeed.setMinimum(0.100000000000000)
        self.turnSpeed.setSingleStep(0.100000000000000)
        self.turnSpeed.setValue(5.000000000000000)

        self.autoGridLayout.addWidget(self.turnSpeed, 2, 1, 1, 1)

        self.autoGridLayout.setColumnStretch(1, 1)

        self.autoCardLayout.addLayout(self.autoGridLayout)


        self.verticalLayout_2.addWidget(self.autoCard)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea22.setWidget(self.scrollAreaWidgetContents)

        self.drawerContentLayout.addWidget(self.scrollArea22)

        self.navCard = QFrame(ReadImg)
        self.navCard.setObjectName(u"navCard")
        self.navCard.setProperty(u"role", u"card")
        self.navCardLayout = QVBoxLayout(self.navCard)
        self.navCardLayout.setSpacing(8)
        self.navCardLayout.setObjectName(u"navCardLayout")
        self.navCardLayout.setContentsMargins(12, 10, 12, 10)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")

        self.navCardLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lastPage = QPushButton(self.navCard)
        self.lastPage.setObjectName(u"lastPage")
        sizePolicy.setHeightForWidth(self.lastPage.sizePolicy().hasHeightForWidth())
        self.lastPage.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lastPage)

        self.nextPage = QPushButton(self.navCard)
        self.nextPage.setObjectName(u"nextPage")
        sizePolicy.setHeightForWidth(self.nextPage.sizePolicy().hasHeightForWidth())
        self.nextPage.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.nextPage)


        self.navCardLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_4 = QPushButton(self.navCard)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.navCard)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.navCardLayout.addLayout(self.horizontalLayout_5)

        self.navActionLayout = QHBoxLayout()
        self.navActionLayout.setSpacing(8)
        self.navActionLayout.setObjectName(u"navActionLayout")
        self.pushButton_2 = QPushButton(self.navCard)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)

        self.navActionLayout.addWidget(self.pushButton_2)

        self.fullButton = QPushButton(self.navCard)
        self.fullButton.setObjectName(u"fullButton")
        sizePolicy.setHeightForWidth(self.fullButton.sizePolicy().hasHeightForWidth())
        self.fullButton.setSizePolicy(sizePolicy)

        self.navActionLayout.addWidget(self.fullButton)

        self.returePage = QPushButton(self.navCard)
        self.returePage.setObjectName(u"returePage")
        sizePolicy.setHeightForWidth(self.returePage.sizePolicy().hasHeightForWidth())
        self.returePage.setSizePolicy(sizePolicy)
        self.returePage.setProperty(u"variant", u"primary")

        self.navActionLayout.addWidget(self.returePage)


        self.navCardLayout.addLayout(self.navActionLayout)


        self.drawerContentLayout.addWidget(self.navCard)


        self.drawerRootLayout.addLayout(self.drawerContentLayout)


        self.retranslateUi(ReadImg)
        self.pushButton_5.clicked.connect(ReadImg.OpenNextEps)
        self.lastPage.clicked.connect(ReadImg.LastPage)
        self.nextPage.clicked.connect(ReadImg.NextPage)
        self.pushButton_4.clicked.connect(ReadImg.OpenLastEps)
        self.pushButton_2.clicked.connect(ReadImg.hide)
        self.returePage.clicked.connect(ReadImg.ReturnPage)
        self.checkBox.clicked.connect(ReadImg.OpenWaifu)
        self.fullButton.clicked.connect(ReadImg.FullScreen)
        self.waifu2xSave.clicked.connect(ReadImg.Waifu2xSave)
        self.waifu2xCancle.clicked.connect(ReadImg.Waifu2xCancle)
        self.zoomSlider.valueChanged.connect(ReadImg.ScalePicture)

        QMetaObject.connectSlotsByName(ReadImg)
    # setupUi

    def retranslateUi(self, ReadImg):
        ReadImg.setWindowTitle(QCoreApplication.translate("ReadImg", u"\u5de5\u5177", None))
        self.label_4.setText(QCoreApplication.translate("ReadImg", u"\u56fe\u7247\u4fe1\u606f", None))
        self.epsLabel.setText(QCoreApplication.translate("ReadImg", u"\u4f4d\u7f6e\uff1a", None))
        self.epsLabel2.setText("")
        self.resolutionLabel.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.resolutionLabel2.setText("")
        self.sizeLabel.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.sizeLabel2.setText("")
        self.stateLable.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.stateLable2.setText("")
        self.label.setText(QCoreApplication.translate("ReadImg", u"Waifu2x\u53c2\u6570", None))
        self.waifu2xSave.setText(QCoreApplication.translate("ReadImg", u"\u4fee\u6539\u53c2\u6570", None))
        self.waifu2xCancle.setText(QCoreApplication.translate("ReadImg", u"\u4fdd\u5b58", None))
        self.checkBox.setText(QCoreApplication.translate("ReadImg", u"\u81ea\u52a8Waifu2x", None))
        self.curWaifu2x.setText(QCoreApplication.translate("ReadImg", u"\u672c\u5f20\u56fe\u5f00\u542fWaifu2x (F2)", None))
        self.preDownWaifu2x.setText(QCoreApplication.translate("ReadImg", u"\u4f18\u5148\u4f7f\u7528\u4e0b\u8f7d\u8f6c\u6362\u597d\u7684", None))
        self.label_3.setText(QCoreApplication.translate("ReadImg", u"\u653e\u5927\u500d\u6570\uff1a", None))
        self.scaleLabel.setText(QCoreApplication.translate("ReadImg", u"2", None))
        self.label_8.setText(QCoreApplication.translate("ReadImg", u"\u6a21\u578b\uff1a", None))
        self.modelNameButton.setText("")
        self.label_9.setText(QCoreApplication.translate("ReadImg", u"\u8f6c\u6362\u6a21\u5f0f\uff1a", None))
        self.gpuLabel.setText(QCoreApplication.translate("ReadImg", u"GPU", None))
        self.resolutionWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5206\u8fa8\u7387\uff1a", None))
        self.waifu2xRes.setText("")
        self.sizeWaifu.setText(QCoreApplication.translate("ReadImg", u"\u5927\u5c0f\uff1a", None))
        self.waifu2xSize.setText("")
        self.tickLabel.setText(QCoreApplication.translate("ReadImg", u"\u8017\u65f6\uff1a", None))
        self.waifu2xTick.setText("")
        self.stateWaifu.setText(QCoreApplication.translate("ReadImg", u"\u72b6\u6001\uff1a", None))
        self.waifu2xStatus.setText("")
        self.label_6.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u8bbe\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u6a21\u5f0f\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ReadImg", u"\u4e0a\u4e0b\u6eda\u52a8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ReadImg", u"\u9ed8\u8ba4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u53cc\u9875", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u53cc\u9875", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("ReadImg", u"\u5de6\u53f3\u6eda\u52a8", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("ReadImg", u"\u53f3\u5de6\u6eda\u52a8", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("ReadImg", u"\u7b49\u5bbd\u6a21\u5f0f", None))

        self.zoomLabel.setText(QCoreApplication.translate("ReadImg", u"\u7f29\u653e\uff08120%\uff09", None))
        self.animeBox.setText(QCoreApplication.translate("ReadImg", u"\u542f\u7528\u7ffb\u9875\u52a8\u753b", None))
        self.switchDouble.setText(QCoreApplication.translate("ReadImg", u"\u5207\u6362\u53cc\u9875\u5bf9\u9f50", None))
        self.openGLBox.setText(QCoreApplication.translate("ReadImg", u"\u6253\u5f00OpenGL\u52a0\u901f", None))
        self.label_7.setText(QCoreApplication.translate("ReadImg", u"\u81ea\u52a8\u6eda\u52a8/\u7ffb\u9875", None))
        self.label_12.setText(QCoreApplication.translate("ReadImg", u"\u624b\u52a8\u6eda\u52a8\uff08\u50cf\u7d20\uff09\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("ReadImg", u"\u81ea\u52a8\u6eda\u52a8\uff08\u50cf\u7d20\uff09\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("ReadImg", u"\u7ffb\u9875\u901f\u5ea6\uff08\u79d2\uff09\uff1a", None))
        self.lastPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u9875", None))
        self.nextPage.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u9875", None))
        self.pushButton_4.setText(QCoreApplication.translate("ReadImg", u"\u4e0a\u4e00\u7ae0", None))
        self.pushButton_5.setText(QCoreApplication.translate("ReadImg", u"\u4e0b\u4e00\u7ae0", None))
        self.pushButton_2.setText(QCoreApplication.translate("ReadImg", u"\u9690\u85cf", None))
        self.fullButton.setText(QCoreApplication.translate("ReadImg", u"\u5168\u5c4f", None))
        self.returePage.setText(QCoreApplication.translate("ReadImg", u"\u8fd4\u56de", None))
    # retranslateUi

