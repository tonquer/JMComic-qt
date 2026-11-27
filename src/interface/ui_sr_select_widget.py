# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sr_select_widget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import images_rc

class Ui_SrSelect(object):
    def setupUi(self, SrSelect):
        if not SrSelect.objectName():
            SrSelect.setObjectName(u"SrSelect")
        SrSelect.resize(760, 560)
        SrSelect.setMinimumSize(QSize(680, 480))
        self.verticalLayout = QVBoxLayout(SrSelect)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 18, 20, 18)
        self.titleLabel = QLabel(SrSelect)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setProperty(u"role", u"pageTitle")

        self.verticalLayout.addWidget(self.titleLabel)

        self.descLayout = QVBoxLayout()
        self.descLayout.setSpacing(2)
        self.descLayout.setObjectName(u"descLayout")
        self.label_4 = QLabel(SrSelect)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setProperty(u"role", u"muted")
        self.label_4.setWordWrap(True)

        self.descLayout.addWidget(self.label_4)

        self.label = QLabel(SrSelect)
        self.label.setObjectName(u"label")
        self.label.setProperty(u"role", u"muted")
        self.label.setWordWrap(True)

        self.descLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.descLayout)

        self.filterLayout = QHBoxLayout()
        self.filterLayout.setSpacing(8)
        self.filterLayout.setObjectName(u"filterLayout")
        self.searchEdit = QLineEdit(SrSelect)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setClearButtonEnabled(True)

        self.filterLayout.addWidget(self.searchEdit)

        self.algoFilter = QComboBox(SrSelect)
        self.algoFilter.addItem("")
        self.algoFilter.addItem("")
        self.algoFilter.addItem("")
        self.algoFilter.addItem("")
        self.algoFilter.setObjectName(u"algoFilter")
        self.algoFilter.setMinimumSize(QSize(130, 0))

        self.filterLayout.addWidget(self.algoFilter)


        self.verticalLayout.addLayout(self.filterLayout)

        self.tableWidget = QTableWidget(SrSelect)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(34)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tipLabel = QLabel(SrSelect)
        self.tipLabel.setObjectName(u"tipLabel")
        self.tipLabel.setProperty(u"role", u"muted")

        self.horizontalLayout_3.addWidget(self.tipLabel)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.footerSpacer)

        self.closeButton = QPushButton(SrSelect)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(88, 0))

        self.horizontalLayout_3.addWidget(self.closeButton)

        self.saveButton = QPushButton(SrSelect)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(96, 0))

        self.horizontalLayout_3.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(SrSelect)

        QMetaObject.connectSlotsByName(SrSelect)
    # setupUi

    def retranslateUi(self, SrSelect):
        SrSelect.setWindowTitle(QCoreApplication.translate("SrSelect", u"\u9009\u62e9\u8d85\u5206\u6a21\u578b", None))
        self.titleLabel.setText(QCoreApplication.translate("SrSelect", u"\u9009\u62e9\u8d85\u5206\u6a21\u578b", None))
        self.label_4.setText(QCoreApplication.translate("SrSelect", u"\u652f\u6301 Waifu2x\u3001Real-CUGAN\u3001Real-ESRGAN\uff08\u4e0d\u652f\u6301 CPU\uff09", None))
        self.label.setText(QCoreApplication.translate("SrSelect", u"UP2X\uff1a\u91c7\u6837\u500d\u7387\uff08\u5efa\u8bae\u9009 2X\uff09\uff0cDENOISE\uff1a\u964d\u566a\u7b49\u7ea7\uff08\u5efa\u8bae\u9009\u6700\u9ad8\uff09", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("SrSelect", u"\u641c\u7d22\u6a21\u578b\u540d\u3001\u7b97\u6cd5\u6216\u63cf\u8ff0...", None))
        self.algoFilter.setItemText(0, QCoreApplication.translate("SrSelect", u"\u5168\u90e8\u7b97\u6cd5", None))
        self.algoFilter.setItemText(1, QCoreApplication.translate("SrSelect", u"Waifu2x", None))
        self.algoFilter.setItemText(2, QCoreApplication.translate("SrSelect", u"Real-CUGAN", None))
        self.algoFilter.setItemText(3, QCoreApplication.translate("SrSelect", u"Real-ESRGAN", None))

        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SrSelect", u"\u6a21\u578b\u540d", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SrSelect", u"\u7b97\u6cd5", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SrSelect", u"\u8017\u65f6", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SrSelect", u"\u63cf\u8ff0", None));
        self.tipLabel.setText(QCoreApplication.translate("SrSelect", u"\u63d0\u793a\uff1a\u53cc\u51fb\u884c\u53ef\u76f4\u63a5\u786e\u8ba4\u9009\u62e9", None))
        self.closeButton.setText(QCoreApplication.translate("SrSelect", u"\u5173\u95ed", None))
        self.saveButton.setText(QCoreApplication.translate("SrSelect", u"\u786e\u5b9a", None))
#if QT_CONFIG(shortcut)
        self.saveButton.setShortcut(QCoreApplication.translate("SrSelect", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

