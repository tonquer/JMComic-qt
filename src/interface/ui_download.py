# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Download(object):
    def setupUi(self, Download):
        if not Download.objectName():
            Download.setObjectName(u"Download")
        Download.resize(1020, 560)
        self.gridLayout_2 = QVBoxLayout(Download)
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(12, 10, 12, 10)
        self.topCard = QFrame(Download)
        self.topCard.setObjectName(u"topCard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topCard.sizePolicy().hasHeightForWidth())
        self.topCard.setSizePolicy(sizePolicy)
        self.topCard.setProperty(u"role", u"card")
        self.topCardLayout = QVBoxLayout(self.topCard)
        self.topCardLayout.setSpacing(10)
        self.topCardLayout.setObjectName(u"topCardLayout")
        self.topCardLayout.setContentsMargins(12, 10, 12, 10)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox = QComboBox(self.topCard)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(96, 0))

        self.horizontalLayout_5.addWidget(self.comboBox)

        self.lineEdit = QLineEdit(self.topCard)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.lineEdit)

        self.formatButton = QPushButton(self.topCard)
        self.formatButton.setObjectName(u"formatButton")
        self.formatButton.setMinimumSize(QSize(84, 0))

        self.horizontalLayout_5.addWidget(self.formatButton)

        self.someDownButton = QPushButton(self.topCard)
        self.someDownButton.setObjectName(u"someDownButton")
        self.someDownButton.setMinimumSize(QSize(84, 0))

        self.horizontalLayout_5.addWidget(self.someDownButton)


        self.topCardLayout.addLayout(self.horizontalLayout_5)

        self.toolbarDivider = QFrame(self.topCard)
        self.toolbarDivider.setObjectName(u"toolbarDivider")
        self.toolbarDivider.setFrameShape(QFrame.Shape.HLine)
        self.toolbarDivider.setFrameShadow(QFrame.Shadow.Sunken)

        self.topCardLayout.addWidget(self.toolbarDivider)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(14)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.redownloadRadio = QCheckBox(self.topCard)
        self.redownloadRadio.setObjectName(u"redownloadRadio")

        self.horizontalLayout_3.addWidget(self.redownloadRadio)

        self.skipPic = QCheckBox(self.topCard)
        self.skipPic.setObjectName(u"skipPic")

        self.horizontalLayout_3.addWidget(self.skipPic)

        self.radioButton = QCheckBox(self.topCard)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(True)
        self.radioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioButton)


        self.horizontalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.topCard)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(82, 0))

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.topCard)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(82, 0))

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.topCard)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(82, 0))

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.topCard)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(82, 0))

        self.horizontalLayout.addWidget(self.pushButton_4)


        self.topCardLayout.addLayout(self.horizontalLayout)


        self.gridLayout_2.addWidget(self.topCard)

        self.tableWidget = QTableWidget(Download)
        if (self.tableWidget.columnCount() < 11):
            self.tableWidget.setColumnCount(11)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)

        self.gridLayout_2.addWidget(self.tableWidget)

        self.gridLayout_2.setStretch(1, 1)

        self.retranslateUi(Download)
        self.pushButton.clicked.connect(Download.StartAll)
        self.pushButton_3.clicked.connect(Download.StopAll)
        self.pushButton_2.clicked.connect(Download.StartConvertAll)
        self.pushButton_4.clicked.connect(Download.StopConvertAll)
        self.radioButton.clicked.connect(Download.SetAutoConvert)

        QMetaObject.connectSlotsByName(Download)
    # setupUi

    def retranslateUi(self, Download):
        Download.setWindowTitle(QCoreApplication.translate("Download", u"\u4e0b\u8f7d", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Download", u"\u5168\u90e8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Download", u"\u672a\u5b8c\u6210", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Download", u"\u5df2\u5b8c\u6210", None))

        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Download", u"\u641c\u7d22\u6807\u9898\u6216 ID\u2026", None))
        self.formatButton.setText(QCoreApplication.translate("Download", u"\u683c\u5f0f\u8f6c\u6362", None))
        self.someDownButton.setText(QCoreApplication.translate("Download", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.redownloadRadio.setText(QCoreApplication.translate("Download", u"\u5931\u8d25\u540e\u81ea\u52a8\u91cd\u8bd5", None))
        self.skipPic.setText(QCoreApplication.translate("Download", u"\u8d85\u5206\u8df3\u8fc7\u635f\u574f", None))
        self.radioButton.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u81ea\u52a8\u8fdb\u884c\u8d85\u5206", None))
        self.pushButton.setText(QCoreApplication.translate("Download", u"\u5168\u90e8\u5f00\u59cb", None))
        self.pushButton_3.setText(QCoreApplication.translate("Download", u"\u5168\u90e8\u6682\u505c", None))
        self.pushButton_2.setText(QCoreApplication.translate("Download", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.pushButton_4.setText(QCoreApplication.translate("Download", u"\u6682\u505c\u8f6c\u6362", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Download", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Download", u"\u65f6\u95f4", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Download", u"\u6807\u9898", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u8fdb\u5ea6", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u7ae0\u8282", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u901f\u5ea6", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Download", u"\u4e0b\u8f7d\u72b6\u6001", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u8fdb\u5ea6", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u7ae0\u8282", None));
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u8017\u65f6", None));
        ___qtablewidgetitem10 = self.tableWidget.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Download", u"\u8f6c\u6362\u72b6\u6001", None));
    # retranslateUi

