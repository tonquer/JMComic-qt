from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, QRectF, Property, Signal
from PySide6.QtGui import QPen, QColor, QBrush, Qt, QPainter, QFont
from PySide6.QtWidgets import QWidget

from config.setting import Setting
from qt_owner import QtOwner
from tools.str import Str


class SwitchButton(QWidget):
    """自定义Switch按钮"""
    Switch = Signal(bool)

    def __init__(self, parent=None, state=True):
        super(SwitchButton, self).__init__(parent)

        # 设置无边框和背景透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.PointingHandCursor)

        self.resize(64, 26)
        self.setFixedSize(64, 26)
        self.state = state  # 按钮状态：True表示开，False表示关
        self._knobPos = 1.0 if state else 0.0
        self._ani = QPropertyAnimation(self, b"knobPos", self)
        self._ani.setDuration(150)
        self._ani.setEasingCurve(QEasingCurve.OutCubic)

    def _getKnobPos(self):
        return self._knobPos

    def _setKnobPos(self, value):
        self._knobPos = value
        self.update()

    knobPos = Property(float, _getKnobPos, _setKnobPos)

    def mousePressEvent(self, event):
        """鼠标点击事件：用于切换按钮状态"""
        super(SwitchButton, self).mousePressEvent(event)

        state = not self.state
        self.SetState(state, animate=True)
        self.Switch.emit(self.state)

    def SetState(self, state, animate=False):
        self.state = bool(state)
        target = 1.0 if self.state else 0.0
        if animate:
            self._ani.stop()
            self._ani.setStartValue(self._knobPos)
            self._ani.setEndValue(target)
            self._ani.start()
        else:
            self._ani.stop()
            self._knobPos = target
            self.update()

    def paintEvent(self, event):
        """绘制按钮"""
        super(SwitchButton, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        w, h = self.width(), self.height()
        r = h / 2.0
        isDark = Setting.ThemeIndex.autoValue == 1
        primary = QColor(QtOwner().GetThemeColorList(0))

        font = QFont('Microsoft YaHei UI')
        font.setPixelSize(11)
        font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(font)

        # 背景轨道
        if self.state:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(primary))
            painter.drawRoundedRect(QRectF(0, 0, w, h), r, r)
        else:
            trackBg = QColor('#2E333E') if isDark else QColor('#CBD5E1')
            trackBorder = QColor('#3D4452') if isDark else QColor('#94A3B8')
            painter.setPen(QPen(trackBorder, 1))
            painter.setBrush(QBrush(trackBg))
            painter.drawRoundedRect(QRectF(0.5, 0.5, w - 1, h - 1), r - 0.5, r - 0.5)

        # 滑块圆点
        knobD = h - 6
        knobX = 3 + (w - knobD - 6) * self._knobPos
        painter.setPen(Qt.NoPen)
        knobColor = QColor('#FFFFFF') if (self.state or not isDark) else QColor('#CBD5E1')
        painter.setBrush(QBrush(knobColor))
        painter.drawEllipse(QRectF(knobX, 3, knobD, knobD))

        # 开关文字
        if self.state:
            painter.setPen(QPen(QColor('#FFFFFF')))
            painter.drawText(QRect(8, 0, w - knobD - 10, h), Qt.AlignVCenter | Qt.AlignCenter, Str.GetStr(Str.SwitchOn))
        else:
            offText = QColor('#94A3B8') if isDark else QColor('#475569')
            painter.setPen(QPen(offText))
            painter.drawText(QRect(knobD + 4, 0, w - knobD - 10, h), Qt.AlignVCenter | Qt.AlignCenter, Str.GetStr(Str.SwitchOff))
