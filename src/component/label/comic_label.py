from PySide6.QtCore import QRect, QRectF, Qt, QSize, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPixmap, QIcon, QFont, QFontMetrics, QImage
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtSvg import QSvgRenderer

from config.setting import Setting

SelectSvg = """<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1788426398229" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7113" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200"><path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z" fill="#F15C58" p-id="7114"></path><path d="M732.48 351.712a48 48 0 0 1 74.144 60.8l-3.104 3.776-320 352a48 48 0 0 1-68.48 2.592l-3.488-3.648-192-224a48 48 0 0 1 69.504-66.048l3.392 3.584 156.608 182.688 283.424-311.744z" fill="#FFFFFF" p-id="7115"></path></svg>"""


class ComicLabel(QLabel):

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.isSelect = None
        self.selectSvg = None
        self._cornerRadius = 8.0

    def SetSelect(self, isSelect):
        if not self.selectSvg:
            self.selectSvg = QSvgRenderer(SelectSvg.encode())
        self.isSelect = isSelect
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        rect = QRectF(self.rect())
        isDark = Setting.ThemeIndex.autoValue == 1
        pm = self.pixmap()

        if not pm.isNull():
            dpr = pm.devicePixelRatio() or 1.0
            pmW = pm.width() / dpr
            pmH = pm.height() / dpr
            if pmW > 0 and pmH > 0:
                scale = min(rect.width() / pmW, rect.height() / pmH)
                drawW = pmW * scale
                drawH = pmH * scale
                drawX = (rect.width() - drawW) / 2.0
                drawY = (rect.height() - drawH) / 2.0
                drawRect = QRectF(drawX, drawY, drawW, drawH)

                clipPath = QPainterPath()
                clipPath.addRoundedRect(drawRect, self._cornerRadius, self._cornerRadius)
                painter.save()
                painter.setClipPath(clipPath)
                if self.isSelect is not None:
                    painter.setOpacity(0.55)
                painter.drawPixmap(drawRect, pm, QRectF(pm.rect()))
                painter.restore()

                if self.isSelect and self.selectSvg:
                    svgW = 22
                    svgH = 22
                    x = int(drawX + drawW - svgW - 8)
                    y = int(drawY + 8)
                    self.selectSvg.render(painter, QRect(x, y, svgW, svgH))
                return

        # 仅在未加载完成/空态时绘制圆角占位卡片
        clipPath = QPainterPath()
        clipPath.addRoundedRect(rect, self._cornerRadius, self._cornerRadius)
        placeholderBg = QColor("#22252D") if isDark else QColor("#EEF1F5")
        painter.fillPath(clipPath, placeholderBg)
        if self.text():
            painter.save()
            painter.setClipPath(clipPath)
            textColor = QColor("#94A3B8") if isDark else QColor("#64748B")
            painter.setPen(textColor)
            painter.drawText(self.rect(), Qt.AlignCenter | Qt.TextWordWrap, self.text())
            painter.restore()