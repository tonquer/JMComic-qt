from PySide6.QtWidgets import QTableWidgetItem

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_doh_dns import Ui_DohDns
from tools.qt_domain import QtDomainMgr


class DohDnsView(BaseMaskDialog, Ui_DohDns):
    def __init__(self, param=None):
        super(self.__class__, self).__init__(param)
        Ui_DohDns.__init__(self)
        self.widget.setMinimumWidth(500)
        self.setupUi(self.widget)
        self.pushButton.clicked.connect(self.close)

    def show(self):
        self.LoadDns()
        return super(self.__class__, self).show()

    def LoadDns(self):
        for row in range(0, self.tableWidget.rowCount()):
            row = self.tableWidget.rowCount()
            self.tableWidget.removeRow(row-1)

        row = 0
        for host, ip in QtDomainMgr().cache_dns.items():
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(host))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(ip))
            row += 1

        for host in QtDomainMgr().fail_dns:
            if host in QtDomainMgr().cache_dns:
                continue
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(host))
            self.tableWidget.setItem(row, 1, QTableWidgetItem("Fail"))
            row += 1
        return
