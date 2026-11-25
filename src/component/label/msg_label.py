import os
import time

from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRectF, Property
from PySide6.QtGui import QPen, QPainterPath, QPainter, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog

from config.setting import Setting
from tools.log import Log


class MsgLabel(QWidget):
    ShowMsgTick = {}

    def __init__(self, *args, **kwargs):
        super(MsgLabel, self).__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setMinimumWidth(0)
        self.setMinimumHeight(40)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._isError = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 10, 18, 10)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumWidth(420)
        layout.addWidget(self.label)
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.finished.connect(self.close)  # 动画结束时关闭窗口
        self.opacityAnimation = None
        self.moveAnimation = None

    def _applyToastStyle(self, isError: bool):
        self._isError = isError
        isDark = Setting.ThemeIndex.autoValue == 1
        if isError:
            textColor = "#FCA5A5" if isDark else "#B91C1C"
        else:
            textColor = "#E8ECF2" if isDark else "#1E293B"
        self.label.setStyleSheet(f"color: {textColor}; background: transparent; font-weight: 500;")
        self.update()

    def setText(self, text):
        text = "" if text is None else str(text)
        fm = self.label.fontMetrics()
        hasNewline = ("\n" in text) or ("<br" in text.lower())
        needWrap = hasNewline or fm.horizontalAdvance(text) > 420
        self.label.setWordWrap(needWrap)
        self.label.setText(text)
        self.label.adjustSize()
        self.adjustSize()

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.animationGroup.clear()
        self.opacityAnimation = None
        self.moveAnimation = None
        self.close()

    def show(self):
        self.adjustSize()
        super(MsgLabel, self).show()
        if self.parent():
            x = self.parent().geometry().x()
            y = self.parent().geometry().y()
            x2 = self.parent().size().width()
            startPos = QPoint(x + int((x2 - self.width()) / 2), y + 64)
            endPos = QPoint(x + int((x2 - self.width()) / 2), y + 40)
            self.move(startPos)
            self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        self.animationGroup.stop()
        self.animationGroup.clear()
        # 透明度动画
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(0.98)
        opacityAnimation.setKeyValueAt(0.7, 0.98)
        opacityAnimation.setEndValue(0.0)
        opacityAnimation.setEasingCurve(QEasingCurve.InQuad)
        opacityAnimation.setDuration(2600)
        # 轻柔上浮动画
        moveAnimation = QPropertyAnimation(self, b"pos")
        moveAnimation.setStartValue(startPos)
        moveAnimation.setEndValue(endPos)
        moveAnimation.setEasingCurve(QEasingCurve.OutCubic)
        moveAnimation.setDuration(2600)
        self.animationGroup.addAnimation(opacityAnimation)
        self.animationGroup.addAnimation(moveAnimation)
        self.animationGroup.start()
        self.opacityAnimation = opacityAnimation
        self.moveAnimation = moveAnimation

    def paintEvent(self, event):
        super(MsgLabel, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        isDark = Setting.ThemeIndex.autoValue == 1
        bgColor = QColor("#272B35") if isDark else QColor("#FFFFFF")
        if self._isError:
            borderColor = QColor("#991B1B") if isDark else QColor("#FCA5A5")
        else:
            borderColor = QColor("#3D4452") if isDark else QColor("#CBD5E1")

        rect = QRectF(0.5, 0.5, self.width() - 1.0, self.height() - 1.0)
        rectPath = QPainterPath()
        rectPath.addRoundedRect(rect, 10, 10)

        painter.setPen(QPen(borderColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(bgColor)
        painter.drawPath(rectPath)

    def windowOpacity(self):
        return super(MsgLabel, self).windowOpacity()

    def setWindowOpacity(self, opacity):
        super(MsgLabel, self).setWindowOpacity(opacity)

    opacity = Property(float, windowOpacity, setWindowOpacity)

    def ShowMsg(self, text):
        self.stop()
        self.setText(text)
        self._applyToastStyle(False)
        self.show()

    @staticmethod
    def ShowMsgEx(owner, text):
        msgTick = MsgLabel.ShowMsgTick.get(owner.__class__.__name__, 0)
        CurTick = int(time.time())
        if msgTick >= CurTick:
            return
        data = MsgLabel(owner)
        data.setAttribute(Qt.WA_DeleteOnClose, True)
        data.setText(text)
        data._applyToastStyle(False)
        data.show()
        MsgLabel.ShowMsgTick[owner.__class__.__name__] = CurTick

    def ShowError(self, text):
        self.stop()
        self.setText(text)
        self._applyToastStyle(True)
        self.show()

    @staticmethod
    def ShowErrorEx(owner, text):
        msgTick = MsgLabel.ShowMsgTick.get(owner.__class__.__name__, 0)
        CurTick = int(time.time())
        if msgTick >= CurTick:
            return
        data = MsgLabel(owner)
        data.setAttribute(Qt.WA_DeleteOnClose, True)
        data.setText(text)
        data._applyToastStyle(True)
        data.show()
        MsgLabel.ShowMsgTick[owner.__class__.__name__] = CurTick

    @staticmethod
    def OpenPicture(self, path="."):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", path, "Image Files(*.jpg *.png)")
            if filename and len(filename) > 1:
                name = filename[0]
                picFormat = filename[1]
                baseName = os.path.basename(name)
                if baseName[-3:] == "png":
                    picFormat = "png"
                elif baseName[-3:] == "jpg":
                    picFormat = "jpeg"
                elif baseName[-4:] == "webp":
                    picFormat = "webp"
                elif baseName[-3:] == "gif":
                    picFormat = "gif"
                else:
                    return None, None, None

                if os.path.isfile(name):
                    self.cachePath = os.path.dirname(name)

                    f = open(name, "rb")
                    data = f.read()
                    f.close()
                    return data, name, picFormat
                return None, None, None
        except Exception as ex:
            Log.Error(ex)
            return None, None, None
