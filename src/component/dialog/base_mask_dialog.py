# coding:utf-8
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, Signal
from PySide6.QtWidgets import (QDialog, QGraphicsDropShadowEffect,
                               QGraphicsOpacityEffect, QWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QApplication)

from config.setting import Setting


class BaseMaskDialog(QDialog):
    """ 带遮罩的对话框抽象基类 """
    closed = Signal()

    def __init__(self, parent):
        #QDialog.__init__(self, parent=parent)
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.windowMask = QWidget(self)
        # 蒙版中间的对话框，所有小部件以他为父级窗口
        self.widget = QWidget(self, objectName='centerWidget')
        self.widget.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.setGeometry(self.parent().geometry())
        self.windowMask.resize(self.size())

        self._updateMaskStyle()
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vBoxLayout.addItem(self.verticalSpacer)
        self.vBoxLayout.addWidget(self.widget, 0, Qt.AlignHCenter)
        self.verticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vBoxLayout.addItem(self.verticalSpacer2)

        self.__setShadowEffect()

    def _updateMaskStyle(self):
        isDark = Setting.ThemeIndex.autoValue == 1
        maskBg = 'rgba(0, 0, 0, 0.58)' if isDark else 'rgba(15, 23, 42, 0.32)'
        self.windowMask.setStyleSheet(f'background: {maskBg};')

    def reject(self):
        self.close()

    def closeEvent(self, arg__1) -> None:
        self.closed.emit()
        arg__1.accept()

    def __setShadowEffect(self):
        """ 添加阴影 """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(36)
        shadowEffect.setOffset(0, 8)
        self.widget.setGraphicsEffect(shadowEffect)

    def showEvent(self, e):
        """ 淡入 """
        self._updateMaskStyle()
        if self.parent():
            self.setGeometry(self.parent().geometry())
            self.windowMask.resize(self.size())
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(180)
        opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        opacityAni.finished.connect(opacityEffect.deleteLater)
        opacityAni.start()
        super().showEvent(e)

    # def closeEvent(self, e):
    #     """ 淡出 """
    #     self.widget.setGraphicsEffect(None)
    #     opacityEffect = QGraphicsOpacityEffect(self)
    #     self.setGraphicsEffect(opacityEffect)
    #     opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
    #     opacityAni.setStartValue(1)
    #     opacityAni.setEndValue(0)
    #     opacityAni.setDuration(100)
    #     opacityAni.setEasingCurve(QEasingCurve.OutCubic)
    #     opacityAni.finished.connect(self.deleteLater)
    #     opacityAni.start()
    #     e.ignore()
