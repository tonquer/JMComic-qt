# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_download_some.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_DownloadSome(object):
    def setupUi(self, DownloadSome):
        if not DownloadSome.objectName():
            DownloadSome.setObjectName(u"DownloadSome")
        DownloadSome.resize(755, 300)
        self.verticalLayout = QVBoxLayout(DownloadSome)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.totalLabel = QLabel(DownloadSome)
        self.totalLabel.setObjectName(u"totalLabel")

        self.horizontalLayout.addWidget(self.totalLabel)

        self.inputButton = QPushButton(DownloadSome)
        self.inputButton.setObjectName(u"inputButton")

        self.horizontalLayout.addWidget(self.inputButton)

        self.loadInfoButton = QPushButton(DownloadSome)
        self.loadInfoButton.setObjectName(u"loadInfoButton")

        self.horizontalLayout.addWidget(self.loadInfoButton)

        self.cleanButton = QPushButton(DownloadSome)
        self.cleanButton.setObjectName(u"cleanButton")

        self.horizontalLayout.addWidget(self.cleanButton)

        self.nasButton = QPushButton(DownloadSome)
        self.nasButton.setObjectName(u"nasButton")

        self.horizontalLayout.addWidget(self.nasButton)

        self.downButton = QPushButton(DownloadSome)
        self.downButton.setObjectName(u"downButton")

        self.horizontalLayout.addWidget(self.downButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(DownloadSome)
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

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(DownloadSome)

        QMetaObject.connectSlotsByName(DownloadSome)
    # setupUi

    def retranslateUi(self, DownloadSome):
        DownloadSome.setWindowTitle(QCoreApplication.translate("DownloadSome", u"Form", None))
        self.totalLabel.setText("")
        self.inputButton.setText(QCoreApplication.translate("DownloadSome", u"\u6279\u91cf\u8f93\u5165JM\u53f7", None))
        self.loadInfoButton.setText(QCoreApplication.translate("DownloadSome", u"\u83b7\u53d6\u4fe1\u606f", None))
        self.cleanButton.setText(QCoreApplication.translate("DownloadSome", u"\u6e05\u7a7a", None))
        self.nasButton.setText(QCoreApplication.translate("DownloadSome", u"\u4e0a\u4f20", None))
        self.downButton.setText(QCoreApplication.translate("DownloadSome", u"\u4e0b\u8f7d", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DownloadSome", u"JM\u53f7", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DownloadSome", u"\u6807\u9898", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DownloadSome", u"\u7ae0\u8282\u6570", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DownloadSome", u"\u72b6\u6001", None));
    # retranslateUi

