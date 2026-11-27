# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_batch_sr.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidgetItem,
    QVBoxLayout, QWidget)

from component.box.wheel_combo_box import WheelComboBox
from component.box.wheel_double_spin_box import WheelDoubleSpinBox
from component.tab.base_table_widget import BaseTableWidget

class Ui_BatchSrTool(object):
    def setupUi(self, BatchSrTool):
        if not BatchSrTool.objectName():
            BatchSrTool.setObjectName(u"BatchSrTool")
        BatchSrTool.resize(920, 560)
        self.verticalLayout = QVBoxLayout(BatchSrTool)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.configCard = QFrame(BatchSrTool)
        self.configCard.setObjectName(u"configCard")
        self.configCard.setProperty(u"role", u"card")
        self.configCardLayout = QVBoxLayout(self.configCard)
        self.configCardLayout.setSpacing(10)
        self.configCardLayout.setObjectName(u"configCardLayout")
        self.configCardLayout.setContentsMargins(14, 12, 14, 12)
        self.label_2 = QLabel(self.configCard)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setProperty(u"role", u"sectionTitle")

        self.configCardLayout.addWidget(self.label_2)

        self.dirGridLayout = QGridLayout()
        self.dirGridLayout.setObjectName(u"dirGridLayout")
        self.dirGridLayout.setHorizontalSpacing(10)
        self.dirGridLayout.setVerticalSpacing(8)
        self.label = QLabel(self.configCard)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")

        self.dirGridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.inputDir = QLineEdit(self.configCard)
        self.inputDir.setObjectName(u"inputDir")

        self.dirGridLayout.addWidget(self.inputDir, 0, 1, 1, 1)

        self.inputDirTool = QPushButton(self.configCard)
        self.inputDirTool.setObjectName(u"inputDirTool")
        self.inputDirTool.setMinimumSize(QSize(72, 0))

        self.dirGridLayout.addWidget(self.inputDirTool, 0, 2, 1, 1)

        self.label_3 = QLabel(self.configCard)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setProperty(u"role", u"muted")

        self.dirGridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.exportDir = QLineEdit(self.configCard)
        self.exportDir.setObjectName(u"exportDir")

        self.dirGridLayout.addWidget(self.exportDir, 1, 1, 1, 1)

        self.exportDirTool = QPushButton(self.configCard)
        self.exportDirTool.setObjectName(u"exportDirTool")
        self.exportDirTool.setMinimumSize(QSize(72, 0))

        self.dirGridLayout.addWidget(self.exportDirTool, 1, 2, 1, 1)

        self.dirGridLayout.setColumnStretch(1, 1)

        self.configCardLayout.addLayout(self.dirGridLayout)

        self.configDivider = QFrame(self.configCard)
        self.configDivider.setObjectName(u"configDivider")
        self.configDivider.setFrameShape(QFrame.Shape.HLine)
        self.configDivider.setFrameShadow(QFrame.Shadow.Sunken)

        self.configCardLayout.addWidget(self.configDivider)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(12)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_25 = QLabel(self.configCard)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setProperty(u"role", u"muted")

        self.horizontalLayout_5.addWidget(self.label_25)

        self.coverModelName = QPushButton(self.configCard)
        self.coverModelName.setObjectName(u"coverModelName")
        self.coverModelName.setMinimumSize(QSize(140, 0))

        self.horizontalLayout_5.addWidget(self.coverModelName)

        self.label_26 = QLabel(self.configCard)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setProperty(u"role", u"muted")

        self.horizontalLayout_5.addWidget(self.label_26)

        self.coverScale = WheelDoubleSpinBox(self.configCard)
        self.coverScale.setObjectName(u"coverScale")
        self.coverScale.setMinimumSize(QSize(96, 0))
        self.coverScale.setMaximumSize(QSize(110, 16777215))
        self.coverScale.setDecimals(1)
        self.coverScale.setMaximum(32.000000000000000)
        self.coverScale.setSingleStep(0.100000000000000)
        self.coverScale.setValue(2.000000000000000)

        self.horizontalLayout_5.addWidget(self.coverScale)

        self.label_5 = QLabel(self.configCard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setProperty(u"role", u"muted")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.fmtBox = WheelComboBox(self.configCard)
        self.fmtBox.setObjectName(u"fmtBox")
        self.fmtBox.setMinimumSize(QSize(92, 0))

        self.horizontalLayout_5.addWidget(self.fmtBox)

        self.label_6 = QLabel(self.configCard)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setProperty(u"role", u"muted")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.threadNum = QComboBox(self.configCard)
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.addItem("")
        self.threadNum.setObjectName(u"threadNum")
        self.threadNum.setMinimumSize(QSize(68, 0))

        self.horizontalLayout_5.addWidget(self.threadNum)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.configCardLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addWidget(self.configCard)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, -1, 2, -1)
        self.label_4 = QLabel(BatchSrTool)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setProperty(u"role", u"muted")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.numLabel = QLabel(BatchSrTool)
        self.numLabel.setObjectName(u"numLabel")
        self.numLabel.setProperty(u"role", u"cardTitle")

        self.horizontalLayout_4.addWidget(self.numLabel)

        self.msgLabel = QLabel(BatchSrTool)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setProperty(u"role", u"muted")

        self.horizontalLayout_4.addWidget(self.msgLabel)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.startImportButton = QPushButton(BatchSrTool)
        self.startImportButton.setObjectName(u"startImportButton")
        self.startImportButton.setMinimumSize(QSize(88, 0))

        self.horizontalLayout_4.addWidget(self.startImportButton)

        self.startConvertButton = QPushButton(BatchSrTool)
        self.startConvertButton.setObjectName(u"startConvertButton")
        self.startConvertButton.setMinimumSize(QSize(88, 0))
        self.startConvertButton.setProperty(u"variant", u"primary")

        self.horizontalLayout_4.addWidget(self.startConvertButton)

        self.cancleButton = QPushButton(BatchSrTool)
        self.cancleButton.setObjectName(u"cancleButton")
        self.cancleButton.setMinimumSize(QSize(76, 0))

        self.horizontalLayout_4.addWidget(self.cancleButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableWidget = BaseTableWidget(BatchSrTool)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
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
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(False)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(BatchSrTool)

        self.threadNum.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(BatchSrTool)
    # setupUi

    def retranslateUi(self, BatchSrTool):
        BatchSrTool.setWindowTitle(QCoreApplication.translate("BatchSrTool", u"\u6279\u91cf\u8d85\u5206", None))
        self.label_2.setText(QCoreApplication.translate("BatchSrTool", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("BatchSrTool", u"\u5bfc\u5165\u76ee\u5f55\uff1a", None))
        self.inputDir.setPlaceholderText(QCoreApplication.translate("BatchSrTool", u"\u8bf7\u9009\u62e9\u9700\u8981\u6279\u91cf\u8d85\u5206\u7684\u56fe\u7247\u76ee\u5f55", None))
        self.inputDirTool.setText(QCoreApplication.translate("BatchSrTool", u"\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("BatchSrTool", u"\u5bfc\u51fa\u76ee\u5f55\uff1a", None))
        self.exportDir.setPlaceholderText(QCoreApplication.translate("BatchSrTool", u"\u8bf7\u9009\u62e9\u8d85\u5206\u7ed3\u679c\u7684\u5bfc\u51fa\u76ee\u5f55", None))
        self.exportDirTool.setText(QCoreApplication.translate("BatchSrTool", u"\u9009\u62e9", None))
        self.label_25.setText(QCoreApplication.translate("BatchSrTool", u"\u6a21\u578b\uff1a", None))
        self.coverModelName.setText("")
        self.label_26.setText(QCoreApplication.translate("BatchSrTool", u"\u653e\u5927\u500d\u6570\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("BatchSrTool", u"\u8f6c\u6362\u683c\u5f0f\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("BatchSrTool", u"\u7ebf\u7a0b\u6570\uff1a", None))
        self.threadNum.setItemText(0, QCoreApplication.translate("BatchSrTool", u"1", None))
        self.threadNum.setItemText(1, QCoreApplication.translate("BatchSrTool", u"2", None))
        self.threadNum.setItemText(2, QCoreApplication.translate("BatchSrTool", u"3", None))
        self.threadNum.setItemText(3, QCoreApplication.translate("BatchSrTool", u"4", None))
        self.threadNum.setItemText(4, QCoreApplication.translate("BatchSrTool", u"5", None))

        self.label_4.setText(QCoreApplication.translate("BatchSrTool", u"\u8fdb\u5ea6\uff08\u6210\u529f / \u5931\u8d25 / \u603b\u8ba1\uff09\uff1a", None))
        self.numLabel.setText(QCoreApplication.translate("BatchSrTool", u"0 / 0 / 0", None))
        self.msgLabel.setText("")
        self.startImportButton.setText(QCoreApplication.translate("BatchSrTool", u"\u5f00\u59cb\u5bfc\u5165", None))
        self.startConvertButton.setText(QCoreApplication.translate("BatchSrTool", u"\u5f00\u59cb\u8f6c\u6362", None))
        self.cancleButton.setText(QCoreApplication.translate("BatchSrTool", u"\u53d6\u6d88", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BatchSrTool", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BatchSrTool", u"\u8017\u65f6", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BatchSrTool", u"\u72b6\u6001", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BatchSrTool", u"\u9519\u8bef\u4fe1\u606f", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("BatchSrTool", u"\u6587\u4ef6\u540d", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("BatchSrTool", u"\u6587\u4ef6\u8def\u5f84", None));
    # retranslateUi

