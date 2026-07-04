# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_proxy_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QCommandLinkButton,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.line_edit.tip_line_edit import TipLineEdit
from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_LoginProxyWidget(object):
    def setupUi(self, LoginProxyWidget):
        if not LoginProxyWidget.objectName():
            LoginProxyWidget.setObjectName(u"LoginProxyWidget")
        LoginProxyWidget.resize(450, 684)
        LoginProxyWidget.setMinimumSize(QSize(450, 0))
        self.gridLayout = QGridLayout(LoginProxyWidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = SmoothScrollArea(LoginProxyWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 413, 682))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.proxy_0 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup = QButtonGroup(LoginProxyWidget)
        self.radioProxyGroup.setObjectName(u"radioProxyGroup")
        self.radioProxyGroup.addButton(self.proxy_0)
        self.proxy_0.setObjectName(u"proxy_0")

        self.horizontalLayout_11.addWidget(self.proxy_0)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxy_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_1)
        self.proxy_1.setObjectName(u"proxy_1")
        self.proxy_1.setMinimumSize(QSize(90, 0))

        self.horizontalLayout.addWidget(self.proxy_1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(self.scrollAreaWidgetContents)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.proxy_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_2)
        self.proxy_2.setObjectName(u"proxy_2")
        self.proxy_2.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_10.addWidget(self.proxy_2)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_10.addWidget(self.line_2)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.sockEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.sockEdit.setObjectName(u"sockEdit")

        self.horizontalLayout_10.addWidget(self.sockEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.proxy_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_3)
        self.proxy_3.setObjectName(u"proxy_3")

        self.horizontalLayout_12.addWidget(self.proxy_3)

        self.checkLabel = QLabel(self.scrollAreaWidgetContents)
        self.checkLabel.setObjectName(u"checkLabel")
        font = QFont()
        font.setBold(False)
        self.checkLabel.setFont(font)
        self.checkLabel.setStyleSheet(u"color:rgb(255, 0, 0)")

        self.horizontalLayout_12.addWidget(self.checkLabel)

        self.proxyLabel = QLabel(self.scrollAreaWidgetContents)
        self.proxyLabel.setObjectName(u"proxyLabel")

        self.horizontalLayout_12.addWidget(self.proxyLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_12 = QLabel(self.scrollAreaWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_4.addWidget(self.label_12)

        self.apiTimeout = WheelComboBox(self.scrollAreaWidgetContents)
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.addItem("")
        self.apiTimeout.setObjectName(u"apiTimeout")

        self.horizontalLayout_4.addWidget(self.apiTimeout)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_4.addWidget(self.label_10)

        self.imgTimeout = WheelComboBox(self.scrollAreaWidgetContents)
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.addItem("")
        self.imgTimeout.setObjectName(u"imgTimeout")

        self.horizontalLayout_4.addWidget(self.imgTimeout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.http3Box = QCheckBox(self.scrollAreaWidgetContents)
        self.http3Box.setObjectName(u"http3Box")

        self.verticalLayout_2.addWidget(self.http3Box)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.echBox = QCheckBox(self.scrollAreaWidgetContents)
        self.echBox.setObjectName(u"echBox")
        self.echBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.echBox)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.dohBox = QCheckBox(self.scrollAreaWidgetContents)
        self.dohBox.setObjectName(u"dohBox")

        self.horizontalLayout_6.addWidget(self.dohBox)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_14.addWidget(self.label_13)

        self.dohLine = TipLineEdit(self.scrollAreaWidgetContents)
        self.dohLine.setObjectName(u"dohLine")

        self.horizontalLayout_14.addWidget(self.dohLine)

        self.dohTool = QToolButton(self.scrollAreaWidgetContents)
        self.dohTool.setObjectName(u"dohTool")

        self.horizontalLayout_14.addWidget(self.dohTool)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.line_8 = QFrame(self.scrollAreaWidgetContents)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.testSpeedButton = QPushButton(self.scrollAreaWidgetContents)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.verticalLayout.addWidget(self.testSpeedButton)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_api_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_3.setObjectName(u"label_api_3")

        self.gridLayout_2.addWidget(self.label_api_3, 4, 1, 1, 1)

        self.radio_img_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup = QButtonGroup(LoginProxyWidget)
        self.radioImgGroup.setObjectName(u"radioImgGroup")
        self.radioImgGroup.addButton(self.radio_img_3)
        self.radio_img_3.setObjectName(u"radio_img_3")

        self.gridLayout_2.addWidget(self.radio_img_3, 4, 2, 1, 1)

        self.label_api_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_4.setObjectName(u"label_api_4")

        self.gridLayout_2.addWidget(self.label_api_4, 5, 1, 1, 1)

        self.radioButton_4 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup = QButtonGroup(LoginProxyWidget)
        self.radioApiGroup.setObjectName(u"radioApiGroup")
        self.radioApiGroup.addButton(self.radioButton_4)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_2.addWidget(self.radioButton_4, 5, 0, 1, 1)

        self.label_api_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_1.setObjectName(u"label_api_1")

        self.gridLayout_2.addWidget(self.label_api_1, 2, 1, 1, 1)

        self.radio_img_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_1)
        self.radio_img_1.setObjectName(u"radio_img_1")
        self.radio_img_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radio_img_1, 2, 2, 1, 1)

        self.label_api_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_2.setObjectName(u"label_api_2")

        self.gridLayout_2.addWidget(self.label_api_2, 3, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.radioButton_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_1, 2, 0, 1, 1)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)

        self.label_img_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_2.setObjectName(u"label_img_2")

        self.gridLayout_2.addWidget(self.label_img_2, 3, 3, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 1, 1, 1, 1)

        self.radio_img_4 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_4)
        self.radio_img_4.setObjectName(u"radio_img_4")

        self.gridLayout_2.addWidget(self.radio_img_4, 5, 2, 1, 1)

        self.radioButton_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridLayout_2.addWidget(self.radioButton_3, 4, 0, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)

        self.label_api_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_5.setObjectName(u"label_api_5")

        self.gridLayout_2.addWidget(self.label_api_5, 7, 1, 1, 1)

        self.label_img_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_4.setObjectName(u"label_img_4")

        self.gridLayout_2.addWidget(self.label_img_4, 5, 3, 1, 1)

        self.radioButton_5 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_5)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.gridLayout_2.addWidget(self.radioButton_5, 7, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_2.addWidget(self.radioButton_2, 3, 0, 1, 1)

        self.radio_img_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_2)
        self.radio_img_2.setObjectName(u"radio_img_2")

        self.gridLayout_2.addWidget(self.radio_img_2, 3, 2, 1, 1)

        self.radio_img_5 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_5)
        self.radio_img_5.setObjectName(u"radio_img_5")

        self.gridLayout_2.addWidget(self.radio_img_5, 7, 2, 1, 1)

        self.label_img_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_5.setObjectName(u"label_img_5")

        self.gridLayout_2.addWidget(self.label_img_5, 7, 3, 1, 1)

        self.label_img_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_3.setObjectName(u"label_img_3")

        self.gridLayout_2.addWidget(self.label_img_3, 4, 3, 1, 1)

        self.label_img_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_1.setObjectName(u"label_img_1")

        self.gridLayout_2.addWidget(self.label_img_1, 2, 3, 1, 1)

        self.radioButton_6 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_6)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.gridLayout_2.addWidget(self.radioButton_6, 6, 0, 1, 1)

        self.radio_img_6 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_6)
        self.radio_img_6.setObjectName(u"radio_img_6")

        self.gridLayout_2.addWidget(self.radio_img_6, 6, 2, 1, 1)

        self.label_api_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_6.setObjectName(u"label_api_6")

        self.gridLayout_2.addWidget(self.label_api_6, 6, 1, 1, 1)

        self.label_img_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_6.setObjectName(u"label_img_6")

        self.gridLayout_2.addWidget(self.label_img_6, 6, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_11 = QLabel(self.scrollAreaWidgetContents)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_11)

        self.cdn_api_ip = QLineEdit(self.scrollAreaWidgetContents)
        self.cdn_api_ip.setObjectName(u"cdn_api_ip")
        self.cdn_api_ip.setMinimumSize(QSize(120, 0))
        self.cdn_api_ip.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.cdn_api_ip)

        self.line_6 = QFrame(self.scrollAreaWidgetContents)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_6)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_2.addWidget(self.label_8)

        self.cdn_img_ip = QLineEdit(self.scrollAreaWidgetContents)
        self.cdn_img_ip.setObjectName(u"cdn_img_ip")
        self.cdn_img_ip.setMinimumSize(QSize(120, 0))
        self.cdn_img_ip.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.cdn_img_ip)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_8.addWidget(self.label_3)

        self.commandLinkButton = QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton.setObjectName(u"commandLinkButton")

        self.horizontalLayout_8.addWidget(self.commandLinkButton)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.line_7 = QFrame(self.scrollAreaWidgetContents)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_7)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_15 = QLabel(self.scrollAreaWidgetContents)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_13.addWidget(self.label_15)

        self.host_api_domain = TipLineEdit(self.scrollAreaWidgetContents)
        self.host_api_domain.setObjectName(u"host_api_domain")
        self.host_api_domain.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_13.addWidget(self.host_api_domain)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_13.addWidget(self.line_5)

        self.label_16 = QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_13.addWidget(self.label_16)

        self.host_img_domain = TipLineEdit(self.scrollAreaWidgetContents)
        self.host_img_domain.setObjectName(u"host_img_domain")
        self.host_img_domain.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_13.addWidget(self.host_img_domain)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_7 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioApiGroup.addButton(self.radioButton_7)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.horizontalLayout_7.addWidget(self.radioButton_7)

        self.label_api_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_7.setObjectName(u"label_api_7")

        self.horizontalLayout_7.addWidget(self.label_api_7)

        self.radio_img_7 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioImgGroup.addButton(self.radio_img_7)
        self.radio_img_7.setObjectName(u"radio_img_7")

        self.horizontalLayout_7.addWidget(self.radio_img_7)

        self.label_img_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_img_7.setObjectName(u"label_img_7")

        self.horizontalLayout_7.addWidget(self.label_img_7)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(LoginProxyWidget)
        self.testSpeedButton.clicked.connect(LoginProxyWidget.SpeedTest)

        QMetaObject.connectSlotsByName(LoginProxyWidget)
    # setupUi

    def retranslateUi(self, LoginProxyWidget):
        LoginProxyWidget.setWindowTitle(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.proxy_0.setText(QCoreApplication.translate("LoginProxyWidget", u"\u65e0\u4ee3\u7406", None))
        self.proxy_1.setText(QCoreApplication.translate("LoginProxyWidget", u"HTTP\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.httpLine.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"http://127.0.0.1:10809", None))
#endif // QT_CONFIG(tooltip)
        self.httpLine.setPlaceholderText("")
        self.proxy_2.setText(QCoreApplication.translate("LoginProxyWidget", u"Sock5\u4ee3\u7406", None))
        self.label_5.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.sockEdit.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"127.0.0.1:10808", None))
#endif // QT_CONFIG(tooltip)
        self.sockEdit.setPlaceholderText("")
        self.proxy_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4f7f\u7528\u7cfb\u7edf\u4ee3\u7406", None))
        self.checkLabel.setText(QCoreApplication.translate("LoginProxyWidget", u"\u672a\u68c0\u6d4b\u5230\u7cfb\u7edf\u4ee3\u7406", None))
        self.proxyLabel.setText("")
        self.label_12.setText(QCoreApplication.translate("LoginProxyWidget", u"API\u8d85\u65f6\u65f6\u95f4  ", None))
        self.apiTimeout.setItemText(0, QCoreApplication.translate("LoginProxyWidget", u"2", None))
        self.apiTimeout.setItemText(1, QCoreApplication.translate("LoginProxyWidget", u"5", None))
        self.apiTimeout.setItemText(2, QCoreApplication.translate("LoginProxyWidget", u"7", None))

        self.label_10.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u8d85\u65f6\u65f6\u95f4 ", None))
        self.imgTimeout.setItemText(0, QCoreApplication.translate("LoginProxyWidget", u"2", None))
        self.imgTimeout.setItemText(1, QCoreApplication.translate("LoginProxyWidget", u"5", None))
        self.imgTimeout.setItemText(2, QCoreApplication.translate("LoginProxyWidget", u"7", None))
        self.imgTimeout.setItemText(3, QCoreApplication.translate("LoginProxyWidget", u"10", None))
        self.imgTimeout.setItemText(4, QCoreApplication.translate("LoginProxyWidget", u"15", None))

        self.http3Box.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528HTTP3\uff08UDP\uff09", None))
        self.echBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528ECH\uff08Encrypted Client Hello\uff09", None))
        self.dohBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528DOH\uff08DNS-over-HTTPS\uff09", None))
        self.label_13.setText(QCoreApplication.translate("LoginProxyWidget", u"DOH\u5730\u5740\uff1a", None))
        self.dohTool.setText("")
        self.testSpeedButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u6d4b\u901f", None))
        self.label_api_3.setText("")
        self.radio_img_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d413", None))
        self.label_api_4.setText("")
#if QT_CONFIG(tooltip)
        self.radioButton_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.radioButton_4.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d414", None))
        self.label_api_1.setText("")
        self.radio_img_1.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d411", None))
        self.label_api_2.setText("")
        self.label_2.setText(QCoreApplication.translate("LoginProxyWidget", u"Api\u5206\u6d41", None))
        self.radioButton_1.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d411", None))
        self.label_4.setText(QCoreApplication.translate("LoginProxyWidget", u"\u901f\u5ea6", None))
        self.label_img_2.setText("")
        self.label_6.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5ef6\u8fdf", None))
#if QT_CONFIG(tooltip)
        self.radio_img_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.radio_img_4.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d414", None))
        self.radioButton_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d413", None))
        self.label_7.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u5206\u6d41", None))
        self.label_api_5.setText("")
        self.label_img_4.setText("")
        self.radioButton_5.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5206\u6d41", None))
        self.radioButton_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d412", None))
        self.radio_img_2.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5206\u6d412", None))
        self.radio_img_5.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5206\u6d41", None))
        self.label_img_5.setText("")
        self.label_img_3.setText("")
        self.label_img_1.setText("")
        self.radioButton_6.setText(QCoreApplication.translate("LoginProxyWidget", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.radio_img_6.setText(QCoreApplication.translate("LoginProxyWidget", u"US\u53cd\u4ee3\u5206\u6d41", None))
        self.label_api_6.setText("")
        self.label_img_6.setText("")
        self.label_11.setText(QCoreApplication.translate("LoginProxyWidget", u" CDN\u5730\u5740:", None))
        self.label_8.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u5730\u5740:", None))
        self.label_3.setText(QCoreApplication.translate("LoginProxyWidget", u"CDN\u8bbe\u7f6e\u8bf7\u770b\u8bf4\u660e\u83b7\u53d6", None))
        self.commandLinkButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u8bf4\u660e", None))
        self.label_15.setText(QCoreApplication.translate("LoginProxyWidget", u"Api\u57df\u540d\uff1a", None))
        self.label_16.setText(QCoreApplication.translate("LoginProxyWidget", u"\u56fe\u7247\u57df\u540d\uff1a", None))
        self.radioButton_7.setText(QCoreApplication.translate("LoginProxyWidget", u"\u81ea\u5b9a\u4e49\u57df\u540d", None))
        self.label_api_7.setText("")
        self.radio_img_7.setText(QCoreApplication.translate("LoginProxyWidget", u"\u81ea\u5b9a\u4e49\u57df\u540d", None))
        self.label_img_7.setText("")
    # retranslateUi

