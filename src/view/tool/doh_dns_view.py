from PySide6.QtWidgets import QTableWidgetItem

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_doh_dns import Ui_DohDns
from server.dns_resolver import DnsResolver


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
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

        row = 0
        # DoH 兜底解析出来并固定住的域名，正常解析的域名不会出现在这里
        for host, ip in DnsResolver().GetPins().items():
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(host))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(ip))
            row += 1
        return
