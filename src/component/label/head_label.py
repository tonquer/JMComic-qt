from PySide6.QtGui import QPainterPath, QPixmap, Qt, QPainter
from PySide6.QtWidgets import QLabel


class HeadLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(HeadLabel, self).__init__(*args, **kwargs)
        self.antialiasing = True
        self.radius = 100
        self.target = None

    def SetPicture(self, data, titleData=None):
        radio = self.devicePixelRatio()
        w, h = self.width(), self.height()
        self.target = QPixmap(int(w * radio), int(h * radio))
        self.target.setDevicePixelRatio(radio)
        self.target.fill(Qt.transparent)
        q = QPixmap()
        q.loadFromData(data)

        offset = 0
        if titleData:
            offset = 20

        targetW = max(1, w - offset)
        targetH = max(1, h - offset)
        p = q.scaled(
            int(targetW * radio), int(targetH * radio), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        p.setDevicePixelRatio(radio)

        painter = QPainter(self.target)
        if self.antialiasing:
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(
            offset / 2.0, offset / 2.0, targetW, targetH, targetW / 2.0, targetH / 2.0)
        painter.setClipPath(path)

        srcX = max(0.0, (p.width() / radio - targetW) / 2.0)
        srcY = max(0.0, (p.height() / radio - targetH) / 2.0)
        painter.drawPixmap(int(offset / 2.0 - srcX), int(offset / 2.0 - srcY), p)
        painter.end()
        self.setPixmap(self.target)

        if titleData:
            p = QPixmap()
            p.loadFromData(titleData)
            titleP = p.scaled(
                int(w * radio), int(h * radio), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            titleP.setDevicePixelRatio(radio)
            painter = QPainter()
            painter.begin(titleP)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
            painter.drawPixmap(0, 0, self.target)
            painter.end()

            self.target = titleP
            self.setPixmap(self.target)