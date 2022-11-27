from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsProxyWidget, QGraphicsPixmapItem, QLabel

from tools.log import Log
from tools.singleton import Singleton
from view.read.read_qgraphics_proxy_widget import ReadQGraphicsProxyWidget


class QtReadImgPoolManager(Singleton):
    def __init__(self):
        self.proxyNum = 1000    # QGraphicsProxyWidget
        self.pixMapNum = 3     # QGraphicsPixmapItem

        self.proxyItem = []
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.MakePool)

    def Init(self):
        self.timer.start()

    def Stop(self):
        self.timer.stop()

    def MakePool(self):
        if len(self.proxyItem) >= self.proxyNum:
            self.timer.stop()
            Log.Info("ReadImgPool create success !")
            return

        for i in range(1, 5):
            a = ReadQGraphicsProxyWidget()
            a.setWidget(QLabel())
            a.setPixmap(QPixmap())
            self.AddProxyItem(a)

    def GetProxyItem(self):
        if not self.proxyItem:
            a = ReadQGraphicsProxyWidget()
            a.setWidget(QLabel())
            a.setPixmap(QPixmap())
            return a
        return self.proxyItem.pop()

    def AddProxyItem(self, item):
        assert isinstance(item, ReadQGraphicsProxyWidget)
        # if item.widget():
        #     item.widget().setParent(None)
            # item.setWidget(None)
        item.setPos(0, 0)
        self.proxyItem.append(item)
