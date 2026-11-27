# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_waifu2x_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QGraphicsView, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_Waifu2xTool(object):
    def setupUi(self, Waifu2xTool):
        if not Waifu2xTool.objectName():
            Waifu2xTool.setObjectName(u"Waifu2xTool")
        Waifu2xTool.resize(820, 580)
        self.gridLayout = QGridLayout(Waifu2xTool)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.graphicsView = QGraphicsView(Waifu2xTool)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = SmoothScrollArea(Waifu2xTool)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(300, 0))
        self.scrollArea.setMaximumSize(QSize(320, 16777215))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 300, 564))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.convertCard = QFrame(self.scrollAreaWidgetContents)
        self.convertCard.setObjectName(u"convertCard")
        self.convertCard.setProperty(u"role", u"card")
        self.verticalLayout_2 = QVBoxLayout(self.convertCard)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(12, 10, 12, 12)
        self.convertTitleLabel = QLabel(self.convertCard)
        self.convertTitleLabel.setObjectName(u"convertTitleLabel")
        self.convertTitleLabel.setProperty(u"role", u"sectionTitle")

        self.verticalLayout_2.addWidget(self.convertTitleLabel)

        self.switchLayout = QHBoxLayout()
        self.switchLayout.setSpacing(16)
        self.switchLayout.setObjectName(u"switchLayout")
        self.checkBox = QCheckBox(self.convertCard)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.switchLayout.addWidget(self.checkBox)

        self.ttaModel = QCheckBox(self.convertCard)
        self.ttaModel.setObjectName(u"ttaModel")

        self.switchLayout.addWidget(self.ttaModel)

        self.switchSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.switchLayout.addItem(self.switchSpacer)


        self.verticalLayout_2.addLayout(self.switchLayout)

        self.convertFormLayout = QGridLayout()
        self.convertFormLayout.setObjectName(u"convertFormLayout")
        self.convertFormLayout.setHorizontalSpacing(8)
        self.convertFormLayout.setVerticalSpacing(8)
        self.scaleRadio = QRadioButton(self.convertCard)
        self.buttonGroup_2 = QButtonGroup(Waifu2xTool)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.scaleRadio)
        self.scaleRadio.setObjectName(u"scaleRadio")
        self.scaleRadio.setChecked(True)

        self.convertFormLayout.addWidget(self.scaleRadio, 0, 0, 1, 1)

        self.scaleEdit = QLineEdit(self.convertCard)
        self.scaleEdit.setObjectName(u"scaleEdit")
        self.scaleEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.convertFormLayout.addWidget(self.scaleEdit, 0, 1, 1, 1)

        self.heighRadio = QRadioButton(self.convertCard)
        self.buttonGroup_2.addButton(self.heighRadio)
        self.heighRadio.setObjectName(u"heighRadio")

        self.convertFormLayout.addWidget(self.heighRadio, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widthEdit = QLineEdit(self.convertCard)
        self.widthEdit.setObjectName(u"widthEdit")
        self.widthEdit.setEnabled(False)
        self.widthEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.widthEdit)

        self.label_2 = QLabel(self.convertCard)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setProperty(u"role", u"muted")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.heighEdit = QLineEdit(self.convertCard)
        self.heighEdit.setObjectName(u"heighEdit")
        self.heighEdit.setEnabled(False)
        self.heighEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.heighEdit)


        self.convertFormLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.label_5 = QLabel(self.convertCard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setProperty(u"role", u"muted")

        self.convertFormLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.modelName = QPushButton(self.convertCard)
        self.modelName.setObjectName(u"modelName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modelName.sizePolicy().hasHeightForWidth())
        self.modelName.setSizePolicy(sizePolicy)

        self.convertFormLayout.addWidget(self.modelName, 2, 1, 1, 1)

        self.label_3 = QLabel(self.convertCard)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setProperty(u"role", u"muted")

        self.convertFormLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.fmtComboBox = QComboBox(self.convertCard)
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.addItem("")
        self.fmtComboBox.setObjectName(u"fmtComboBox")
        sizePolicy.setHeightForWidth(self.fmtComboBox.sizePolicy().hasHeightForWidth())
        self.fmtComboBox.setSizePolicy(sizePolicy)

        self.convertFormLayout.addWidget(self.fmtComboBox, 3, 1, 1, 1)

        self.convertFormLayout.setColumnStretch(1, 1)

        self.verticalLayout_2.addLayout(self.convertFormLayout)

        self.changeButton = QPushButton(self.convertCard)
        self.changeButton.setObjectName(u"changeButton")
        sizePolicy.setHeightForWidth(self.changeButton.sizePolicy().hasHeightForWidth())
        self.changeButton.setSizePolicy(sizePolicy)
        self.changeButton.setProperty(u"variant", u"primary")

        self.verticalLayout_2.addWidget(self.changeButton)


        self.verticalLayout_4.addWidget(self.convertCard)

        self.infoCard = QFrame(self.scrollAreaWidgetContents)
        self.infoCard.setObjectName(u"infoCard")
        self.infoCard.setProperty(u"role", u"card")
        self.verticalLayout_3 = QVBoxLayout(self.infoCard)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(12, 10, 12, 12)
        self.infoTitleLabel = QLabel(self.infoCard)
        self.infoTitleLabel.setObjectName(u"infoTitleLabel")
        self.infoTitleLabel.setProperty(u"role", u"sectionTitle")

        self.verticalLayout_3.addWidget(self.infoTitleLabel)

        self.infoGridLayout = QGridLayout()
        self.infoGridLayout.setObjectName(u"infoGridLayout")
        self.infoGridLayout.setHorizontalSpacing(8)
        self.infoGridLayout.setVerticalSpacing(6)
        self.label_8 = QLabel(self.infoCard)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setProperty(u"role", u"muted")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.infoGridLayout.addWidget(self.label_8, 0, 0, 1, 1)

        self.resolutionLabel = QLabel(self.infoCard)
        self.resolutionLabel.setObjectName(u"resolutionLabel")
        self.resolutionLabel.setWordWrap(True)

        self.infoGridLayout.addWidget(self.resolutionLabel, 0, 1, 1, 1)

        self.label_10 = QLabel(self.infoCard)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setProperty(u"role", u"muted")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.infoGridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.sizeLabel = QLabel(self.infoCard)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setWordWrap(True)

        self.infoGridLayout.addWidget(self.sizeLabel, 1, 1, 1, 1)

        self.label = QLabel(self.infoCard)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.infoGridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.format = QLabel(self.infoCard)
        self.format.setObjectName(u"format")

        self.infoGridLayout.addWidget(self.format, 2, 1, 1, 1)

        self.label_6 = QLabel(self.infoCard)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setProperty(u"role", u"muted")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.infoGridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.tickLabel = QLabel(self.infoCard)
        self.tickLabel.setObjectName(u"tickLabel")

        self.infoGridLayout.addWidget(self.tickLabel, 3, 1, 1, 1)

        self.label_9 = QLabel(self.infoCard)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setProperty(u"role", u"muted")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.infoGridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.gpuLabel = QLabel(self.infoCard)
        self.gpuLabel.setObjectName(u"gpuLabel")
        self.gpuLabel.setWordWrap(True)

        self.infoGridLayout.addWidget(self.gpuLabel, 4, 1, 1, 1)

        self.infoGridLayout.setColumnStretch(1, 1)

        self.verticalLayout_3.addLayout(self.infoGridLayout)


        self.verticalLayout_4.addWidget(self.infoCard)

        self.actionCard = QFrame(self.scrollAreaWidgetContents)
        self.actionCard.setObjectName(u"actionCard")
        self.actionCard.setProperty(u"role", u"card")
        self.actionLayout = QVBoxLayout(self.actionCard)
        self.actionLayout.setSpacing(8)
        self.actionLayout.setObjectName(u"actionLayout")
        self.actionLayout.setContentsMargins(12, 10, 12, 12)
        self.actionTitleLabel = QLabel(self.actionCard)
        self.actionTitleLabel.setObjectName(u"actionTitleLabel")
        self.actionTitleLabel.setProperty(u"role", u"sectionTitle")

        self.actionLayout.addWidget(self.actionTitleLabel)

        self.actionGridLayout = QGridLayout()
        self.actionGridLayout.setObjectName(u"actionGridLayout")
        self.actionGridLayout.setHorizontalSpacing(8)
        self.actionGridLayout.setVerticalSpacing(8)
        self.oepnButton = QPushButton(self.actionCard)
        self.oepnButton.setObjectName(u"oepnButton")
        sizePolicy.setHeightForWidth(self.oepnButton.sizePolicy().hasHeightForWidth())
        self.oepnButton.setSizePolicy(sizePolicy)

        self.actionGridLayout.addWidget(self.oepnButton, 0, 0, 1, 1)

        self.saveButton = QPushButton(self.actionCard)
        self.saveButton.setObjectName(u"saveButton")
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)

        self.actionGridLayout.addWidget(self.saveButton, 0, 1, 1, 1)

        self.pushButton = QPushButton(self.actionCard)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        self.actionGridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.actionCard)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)

        self.actionGridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)

        self.actionGridLayout.setColumnStretch(0, 1)
        self.actionGridLayout.setColumnStretch(1, 1)

        self.actionLayout.addLayout(self.actionGridLayout)

        self.headButton = QPushButton(self.actionCard)
        self.headButton.setObjectName(u"headButton")
        sizePolicy.setHeightForWidth(self.headButton.sizePolicy().hasHeightForWidth())
        self.headButton.setSizePolicy(sizePolicy)

        self.actionLayout.addWidget(self.headButton)


        self.verticalLayout_4.addWidget(self.actionCard)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.retranslateUi(Waifu2xTool)
        self.checkBox.clicked.connect(Waifu2xTool.SwithPicture)
        self.saveButton.clicked.connect(Waifu2xTool.SavePicture)
        self.heighEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.pushButton_3.clicked.connect(Waifu2xTool.ReduceScalePic)
        self.heighRadio.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.ttaModel.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.oepnButton.clicked.connect(Waifu2xTool.OpenPicture)
        self.widthEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.pushButton.clicked.connect(Waifu2xTool.AddScalePic)
        self.scaleEdit.textChanged.connect(Waifu2xTool.CheckScaleRadio)
        self.scaleRadio.clicked.connect(Waifu2xTool.CheckScaleRadio)
        self.changeButton.clicked.connect(Waifu2xTool.StartWaifu2x)
        self.headButton.clicked.connect(Waifu2xTool.SetHead)

        QMetaObject.connectSlotsByName(Waifu2xTool)
    # setupUi

    def retranslateUi(self, Waifu2xTool):
        Waifu2xTool.setWindowTitle(QCoreApplication.translate("Waifu2xTool", u"\u56fe\u7247\u67e5\u770b", None))
        self.convertTitleLabel.setText(QCoreApplication.translate("Waifu2xTool", u"Waifu2x \u8f6c\u6362", None))
        self.checkBox.setText(QCoreApplication.translate("Waifu2xTool", u"waifu2x", None))
#if QT_CONFIG(tooltip)
        self.ttaModel.setToolTip(QCoreApplication.translate("Waifu2xTool", u"\u753b\u8d28\u63d0\u5347\uff0c\u8017\u65f6\u589e\u52a0", None))
#endif // QT_CONFIG(tooltip)
        self.ttaModel.setText(QCoreApplication.translate("Waifu2xTool", u"tta\u6a21\u5f0f", None))
        self.scaleRadio.setText(QCoreApplication.translate("Waifu2xTool", u"\u500d\u6570\u653e\u5927", None))
        self.scaleEdit.setText(QCoreApplication.translate("Waifu2xTool", u"2", None))
        self.heighRadio.setText(QCoreApplication.translate("Waifu2xTool", u"\u56fa\u5b9a\u957f\u5bbd", None))
        self.widthEdit.setPlaceholderText(QCoreApplication.translate("Waifu2xTool", u"\u5bbd", None))
        self.label_2.setText(QCoreApplication.translate("Waifu2xTool", u"\u00d7", None))
        self.heighEdit.setPlaceholderText(QCoreApplication.translate("Waifu2xTool", u"\u9ad8", None))
        self.label_5.setText(QCoreApplication.translate("Waifu2xTool", u"\u6a21\u578b\uff1a", None))
        self.modelName.setText("")
        self.label_3.setText(QCoreApplication.translate("Waifu2xTool", u"\u683c\u5f0f\uff1a", None))
        self.fmtComboBox.setItemText(0, QCoreApplication.translate("Waifu2xTool", u"\u81ea\u52a8", None))
        self.fmtComboBox.setItemText(1, QCoreApplication.translate("Waifu2xTool", u"JPG", None))
        self.fmtComboBox.setItemText(2, QCoreApplication.translate("Waifu2xTool", u"PNG", None))
        self.fmtComboBox.setItemText(3, QCoreApplication.translate("Waifu2xTool", u"BMP", None))
        self.fmtComboBox.setItemText(4, QCoreApplication.translate("Waifu2xTool", u"WEBP", None))
        self.fmtComboBox.setItemText(5, QCoreApplication.translate("Waifu2xTool", u"APNG", None))
        self.fmtComboBox.setItemText(6, QCoreApplication.translate("Waifu2xTool", u"JXL", None))

        self.changeButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u8f6c\u6362", None))
        self.infoTitleLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u56fe\u7247\u4fe1\u606f", None))
        self.label_8.setText(QCoreApplication.translate("Waifu2xTool", u"\u5206\u8fa8\u7387\uff1a", None))
        self.resolutionLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u65e0\u4fe1\u606f", None))
        self.label_10.setText(QCoreApplication.translate("Waifu2xTool", u"\u5927\u5c0f\uff1a", None))
        self.sizeLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u65e0\u4fe1\u606f", None))
        self.label.setText(QCoreApplication.translate("Waifu2xTool", u"\u683c\u5f0f\uff1a", None))
        self.format.setText(QCoreApplication.translate("Waifu2xTool", u"-", None))
        self.label_6.setText(QCoreApplication.translate("Waifu2xTool", u"\u8017\u65f6\uff1a", None))
        self.tickLabel.setText(QCoreApplication.translate("Waifu2xTool", u"-", None))
        self.label_9.setText(QCoreApplication.translate("Waifu2xTool", u"\u8f6c\u6362\u6a21\u5f0f\uff1a", None))
        self.gpuLabel.setText(QCoreApplication.translate("Waifu2xTool", u"GPU", None))
        self.actionTitleLabel.setText(QCoreApplication.translate("Waifu2xTool", u"\u56fe\u7247\u64cd\u4f5c", None))
        self.oepnButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u6253\u5f00\u56fe\u7247", None))
        self.saveButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.pushButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u653e\u5927", None))
        self.pushButton_3.setText(QCoreApplication.translate("Waifu2xTool", u"\u7f29\u5c0f", None))
        self.headButton.setText(QCoreApplication.translate("Waifu2xTool", u"\u8bbe\u7f6e\u4e3a\u5934\u50cf", None))
    # retranslateUi

