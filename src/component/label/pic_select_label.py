from PySide6.QtCore import QRect, Qt, QSize, Signal
from PySide6.QtGui import QPainter, QPixmap, QIcon, QFont, QFontMetrics, QImage
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtSvg import QSvgRenderer


class ComicLabel(QLabel):

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.isSelect = None
        self.selectSvg = None

    def SetSelect(self, isSelect):
        self.isSelect = isSelect
        self.update()

    def paintEvent(self, event) -> None:

        if self.isSelect is None:
            QLabel.paintEvent(self)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        targetRect = self.rect()
        m_baseOpacity = 0.5
        if (not self.pixmap().isNull()):
            painter.save()
            painter.setOpacity(m_baseOpacity)

            painter.drawPixmap(targetRect, self.pixmap())
            painter.restore()

        if self.isSelect:
            if not self.selectSvg:
                self.selectSvg = QSvgRenderer(u":/icon/select.svg")
            svgW = 64
            svgH = 64
            x = (self.width() - svgW) / 2
            y = (self.height() - svgH) / 2
            targetRect = QRect(x, y, svgW, svgH)
            self.selectSvg.render(painter, targetRect)