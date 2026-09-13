from PySide6.QtCore import QRect, Qt, QSize, Signal
from PySide6.QtGui import QPainter, QPixmap, QIcon, QFont, QFontMetrics, QImage
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtSvg import QSvgRenderer

SelectSvg = """<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1788426398229" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7113" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#F15C58" p-id="7114"></path><path d="M732.48 351.712a48 48 0 0 1 74.144 60.8l-3.104 3.776-320 352a48 48 0 0 1-68.48 2.592l-3.488-3.648-192-224a48 48 0 0 1 69.504-66.048l3.392 3.584 156.608 182.688 283.424-311.744z" fill="#FFFFFF" p-id="7115"></path></svg>"""


class ComicLabel(QLabel):

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.isSelect = None
        self.selectSvg = None

    def SetSelect(self, isSelect):
        if not self.selectSvg:
            self.selectSvg = QSvgRenderer(SelectSvg.encode())
        self.isSelect = isSelect
        self.update()

    def paintEvent(self, event) -> None:
        if self.isSelect is None or not self.selectSvg:
            QLabel.paintEvent(self, event)
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
            # if not self.selectSvg:
            #     self.selectSvg = QSvgRenderer(SelectSvg.encode())
            svgW = 16
            svgH = 16
            x = (self.width() - svgW)
            y = svgH
            targetRect = QRect(x, y, svgW, svgH)
            self.selectSvg.render(painter, targetRect)