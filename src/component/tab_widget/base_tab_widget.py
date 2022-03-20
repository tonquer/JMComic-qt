from PySide6.QtGui import QMouseEvent, Qt
from PySide6.QtWidgets import QTabWidget


class BaseTabWidget(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            # QtOwner().SwitchWidgetNext()
            if self.currentIndex() >= self.count() - 1:
                event.ignore()
            else:
                self.setCurrentIndex(self.currentIndex() + 1)
        elif event.button() == Qt.BackButton:
            if self.currentIndex() <= 0:
                event.ignore()
            else:
                self.setCurrentIndex(self.currentIndex() - 1)
            # QtOwner().SwitchWidgetLast()
        return QTabWidget.mousePressEvent(self, event)