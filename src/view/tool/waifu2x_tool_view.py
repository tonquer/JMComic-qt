import io
import os
import sys
import time

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QSize, QEvent, QPoint, QByteArray, QBuffer, QIODevice, QTimer
from PySide6.QtGui import QPainter, QPixmap, QDoubleValidator, \
    QIntValidator, QMouseEvent, QImage, QMovie, QImageReader
from PySide6.QtWidgets import QFrame, QGraphicsItem, QGraphicsScene, QApplication, QFileDialog, QGraphicsView

from config import config
from config.setting import Setting
from interface.ui_waifu2x_tool import Ui_Waifu2xTool
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from task.task_qimage import _decode_bytes_to_qimage
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil


class Waifu2xGraphicsItem(QGraphicsItem):
    """支持静态图与动图（GIF/WebP/AVIF/JXL 走 QMovie，APNG 等走 Pillow 逐帧）的绘制项。"""

    def __init__(self, host_widget):
        super().__init__()
        self._host = host_widget
        self._w = 0.0
        self._h = 0.0
        self._src_w = 0
        self._src_h = 0
        self._dpr = 1.0
        self._pixmap = QPixmap()

        # QMovie 播放状态
        self._movie = None
        self._movie_buf = None

        # Pillow 逐帧播放状态（用于 Qt QMovie 不支持的动图，例如 APNG）
        self._pil_bio = None
        self._pil_img = None
        self._pil_frame = 0
        self._pil_n_frames = 0
        self._pil_timer = QTimer(host_widget)
        self._pil_timer.setSingleShot(True)
        self._pil_timer.timeout.connect(self._next_pil_frame)

        self._paused = False

    def boundingRect(self) -> QRectF:
        return QRectF(0.0, 0.0, self._w, self._h)

    def pixmap(self) -> QPixmap:
        if self._movie is not None:
            pm = self._movie.currentPixmap()
            if not pm.isNull():
                return pm
        return self._pixmap

    def _calc_movie_scaled_size(self) -> QSize:
        """物理像素目标尺寸：只缩不放，避免放大时 QMovie 解码爆内存。"""
        if self._src_w <= 0 or self._src_h <= 0:
            return QSize()
        phys_w = max(1, int(round(self._w * self._dpr)))
        phys_h = max(1, int(round(self._h * self._dpr)))
        if phys_w < self._src_w or phys_h < self._src_h:
            scale = min(phys_w / self._src_w, phys_h / self._src_h)
            return QSize(max(1, int(round(self._src_w * scale))),
                         max(1, int(round(self._src_h * scale))))
        return QSize(self._src_w, self._src_h)

    def ClearAnimation(self):
        if self._pil_timer.isActive():
            self._pil_timer.stop()
        if self._pil_img is not None:
            try:
                self._pil_img.close()
            except Exception:
                pass
            self._pil_img = None
        if self._pil_bio is not None:
            try:
                self._pil_bio.close()
            except Exception:
                pass
            self._pil_bio = None
        self._pil_frame = 0
        self._pil_n_frames = 0

        mv = self._movie
        buf = self._movie_buf
        self._movie = None
        self._movie_buf = None
        if mv is not None:
            mv.stop()
            mv.setDevice(None)
        if buf is not None:
            buf.close()
            buf.setData(QByteArray())
            if mv is None:
                buf.deleteLater()
        if mv is not None:
            mv.deleteLater()

    def IsAnimatedActive(self) -> bool:
        return self._movie is not None or self._pil_img is not None

    def SetStaticPixmap(self, pixmap: QPixmap, disp_w: float, disp_h: float):
        self.ClearAnimation()
        self.prepareGeometryChange()
        self._w = float(disp_w)
        self._h = float(disp_h)
        self._src_w = pixmap.width()
        self._src_h = pixmap.height()
        self._pixmap = pixmap
        self.update()

    def SetDisplaySize(self, disp_w: float, disp_h: float, dpr: float):
        self.prepareGeometryChange()
        self._w = float(disp_w)
        self._h = float(disp_h)
        self._dpr = max(1.0, float(dpr))
        if self._movie is not None:
            sz = self._calc_movie_scaled_size()
            if sz.isValid() and self._movie.scaledSize() != sz:
                self._movie.setScaledSize(sz)
        self.update()

    def SetAnimationData(self, data: bytes, src_w: int, src_h: int, disp_w: float, disp_h: float, dpr: float, fallback_pixmap: QPixmap = None):
        self.ClearAnimation()
        self.prepareGeometryChange()
        self._w = float(disp_w)
        self._h = float(disp_h)
        self._src_w = int(src_w)
        self._src_h = int(src_h)
        self._dpr = max(1.0, float(dpr))
        self._pixmap = fallback_pixmap if (fallback_pixmap is not None and not fallback_pixmap.isNull()) else QPixmap()

        if self._init_qmovie(data):
            self.update()
            return

        if self._init_pil_anim(data):
            self.update()
            return

        self.update()

    def _init_qmovie(self, data: bytes) -> bool:
        mv = QMovie(self._host)
        buf = QBuffer(mv)
        buf.setData(QByteArray(data))
        if not buf.open(QIODevice.ReadOnly):
            buf.deleteLater()
            mv.deleteLater()
            return False

        reader = QImageReader(buf)
        supports_anim = reader.supportsAnimation()
        buf.seek(0)
        if not supports_anim:
            buf.close()
            buf.setData(QByteArray())
            mv.deleteLater()
            return False

        mv.setCacheMode(QMovie.CacheNone)
        mv.setDevice(buf)
        if not mv.isValid():
            mv.setDevice(None)
            buf.close()
            buf.setData(QByteArray())
            mv.deleteLater()
            return False

        sz = self._calc_movie_scaled_size()
        if sz.isValid():
            mv.setScaledSize(sz)
        mv.frameChanged.connect(lambda _n=0, _mv=mv: self._movie is _mv and self.update())
        self._movie = mv
        self._movie_buf = buf
        if self._paused:
            mv.jumpToFrame(0)
        else:
            mv.start()
        return True

    def _init_pil_anim(self, data: bytes) -> bool:
        try:
            try:
                import pillow_jxl  # noqa: F401
                import pillow_avif  # noqa: F401
            except Exception:
                pass
            from PIL import Image
            bio = io.BytesIO(data)
            im = Image.open(bio)
            n_frames = getattr(im, "n_frames", 1)
            if not getattr(im, "is_animated", False) or n_frames <= 1:
                im.close()
                bio.close()
                return False
            self._pil_bio = bio
            self._pil_img = im
            self._pil_n_frames = n_frames
            self._pil_frame = 0
            self._render_pil_frame(0, schedule_next=not self._paused)
            return True
        except Exception as ex:
            Log.Error(ex)
            return False

    def _pil_frame_to_pixmap(self, im) -> QPixmap:
        im_rgba = im.convert("RGBA") if im.mode != "RGBA" else im
        w, h = im_rgba.width, im_rgba.height
        if sys.byteorder == "little":
            raw = im_rgba.tobytes("raw", "BGRA")
            qimg = QImage(raw, w, h, w * 4, QImage.Format_ARGB32).copy()
        else:
            raw = im_rgba.tobytes("raw", "RGBA")
            qimg = QImage(raw, w, h, w * 4, QImage.Format_RGBA8888).copy()
        return QPixmap.fromImage(qimg)

    def _render_pil_frame(self, idx: int, schedule_next: bool = True):
        if self._pil_img is None:
            return
        try:
            self._pil_img.seek(idx)
            self._pil_frame = idx
            pm = self._pil_frame_to_pixmap(self._pil_img)
            if not pm.isNull():
                self._pixmap = pm
            raw_dur = self._pil_img.info.get("duration", 100)
            try:
                dur = int(round(float(raw_dur)))
            except Exception:
                dur = 100
            if dur <= 0:
                dur = 100
            dur = max(16, dur)
            self.update()
            if schedule_next and not self._paused:
                self._pil_timer.start(dur)
        except Exception as ex:
            Log.Error(ex)

    def _next_pil_frame(self):
        if self._pil_img is None or self._pil_n_frames <= 1 or self._paused:
            return
        next_idx = (self._pil_frame + 1) % self._pil_n_frames
        self._render_pil_frame(next_idx, schedule_next=True)

    def SetPaused(self, paused: bool):
        self._paused = bool(paused)
        if self._movie is not None:
            if self._paused:
                if self._movie.state() == QMovie.Running:
                    self._movie.setPaused(True)
            else:
                if self._movie.state() == QMovie.NotRunning:
                    self._movie.start()
                elif self._movie.state() == QMovie.Paused:
                    self._movie.setPaused(False)
        elif self._pil_img is not None:
            if self._paused:
                if self._pil_timer.isActive():
                    self._pil_timer.stop()
            else:
                if not self._pil_timer.isActive():
                    self._pil_timer.start(16)

    def paint(self, painter: QPainter, option, widget=None):
        pm = self._movie.currentPixmap() if self._movie is not None else None
        if pm is None or pm.isNull():
            pm = self._pixmap
        if pm is not None and not pm.isNull() and self._w > 0 and self._h > 0:
            painter.drawPixmap(QRectF(0.0, 0.0, self._w, self._h), pm, QRectF(pm.rect()))


class Waifu2xToolView(QtWidgets.QWidget, Ui_Waifu2xTool, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Waifu2xTool.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookId = ""
        self.epsId = 0
        self.curIndex = 0
        # self.resize(800, 900)
        self.checkBox.setChecked(True)
        from config.setting import Setting
        self.modelName.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.modelName.setToolTip(Setting.LookModelName.value)

        # self.comboBox.setCurrentIndex(self.index)
        validator = QIntValidator(0, 9999999)
        self.heighEdit.setValidator(validator)
        self.widthEdit.setValidator(validator)
        exp = QDoubleValidator(0.1, 64, 1)
        exp.setNotation(QDoubleValidator.StandardNotation)
        self.scaleEdit.setValidator(exp)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.setAcceptDrops(True)
        self.graphicsView.setFrameStyle(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setAcceptDrops(False)
        self.graphicsView.viewport().setAcceptDrops(False)
        # self.graphicsView.setBackgroundBrush(QColor(Qt.white))
        self.graphicsView.setCursor(Qt.OpenHandCursor)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setRenderHints(QPainter.Antialiasing |
                                         QPainter.SmoothPixmapTransform)
        self.graphicsView.setCacheMode(QGraphicsView.CacheNone)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.graphicsItem = Waifu2xGraphicsItem(self)
        self.graphicsItem.setFlags(QGraphicsItem.ItemIsFocusable |
                                   QGraphicsItem.ItemIsMovable)
        self.graphicsView.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.CopyPicture)
        self.graphicsScene = QGraphicsScene(self)  # 场景
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.graphicsItem)
        self.graphicsItem.setPos(QPointF(0, 0))
        self.graphicsView.setMinimumSize(10, 10)
        # self.pixMapData = None
        self.pixMap = QImage(Str.GetStr(Str.LoadingPicture))
        # self.graphicsItem.setPixmap(self.pixMap)
        # self.radioButton.setChecked(True)
        self.isStripModel = False

        # self.radioButton.installEventFilter(self)
        # self.radioButton_2.installEventFilter(self)
        # self.graphicsItem.installSceneEventFilter(self.graphicsItem)
        # self.graphicsView.installEventFilter(self)
        self.graphicsScene.installEventFilter(self)
        self.graphicsView.setWindowFlag(Qt.FramelessWindowHint)

        self._delta = 0.1
        self.scaleCnt = 0

        self.data = b""
        self.waifu2xData = b""
        self._curDisplayData = None
        self._curW = 0
        self._curH = 0
        self._curMat = ""
        self._curIsAnima = False
        self.backStatus = ""
        self.modelName.clicked.connect(self.OpenSrSelect)
        self.fmtComboBox.currentIndexChanged.connect(self.CheckStatus)

    def retranslateUi(self, SettingNew):
        oldName = self.modelName.toolTip()
        Ui_Waifu2xTool.retranslateUi(self, SettingNew)
        self.modelName.setText(ToolUtil.GetShowModelName(oldName))
        self.modelName.setToolTip(oldName)

    def OpenSrSelect(self):
        QtOwner().OpenSrSelectModel(self.modelName.toolTip(), self.OpenSrSelectBack)

    def OpenSrSelectBack(self, newModName):
        self.modelName.setText(ToolUtil.GetShowModelName(newModName))
        self.modelName.setToolTip(newModName)
        self.CheckStatus()

    def CheckStatus(self):
        data = self.GetStatus()
        if self.backStatus != data:
            self.changeButton.setText(Str.GetStr(Str.Convert))
            self.changeButton.setEnabled(True)

    def SwitchCurrent(self, **kwargs):
        data = kwargs.get("data")
        self.gpuLabel.setText(config.EncodeGpu)
        if data:
            self.data = data
            self.waifu2xData = None
            self.scaleCnt = 0
            self.tickLabel.setText("-")
            self.ClearConvert()
            if config.CanWaifu2x:
                self.modelName.setEnabled(True)
                self.changeButton.setEnabled(True)
            self.changeButton.setText(Str.GetStr(Str.Convert))
            self.backStatus = ""
            self.CheckScaleRadio()

        else:
            return

        self.ShowImg(self.data)

    def ShowImg(self, data):
        if not data:
            return

        self.gpuLabel.setText(config.EncodeGpu)
        dpr = max(1.0, self.graphicsView.devicePixelRatioF())
        same_data = (data is self._curDisplayData)

        if not same_data:
            self._curDisplayData = data
            width, height, mat, isAnima = ToolUtil.GetPictureSize(data)
            if not isAnima:
                # 主线程兜底：对 Pillow 无法识别动图标志的格式（如 JXL 等），直接以 Qt 插件结果为准
                probe_buf = QBuffer()
                probe_buf.setData(QByteArray(data))
                if probe_buf.open(QIODevice.ReadOnly):
                    probe_reader = QImageReader(probe_buf)
                    if probe_reader.supportsAnimation() and probe_reader.imageCount() != 1:
                        isAnima = True
                    if (not width or not height) and probe_reader.size().isValid():
                        width = probe_reader.size().width()
                        height = probe_reader.size().height()
                    probe_buf.close()
            self._curW = width
            self._curH = height
            self._curMat = mat
            self._curIsAnima = isAnima

            self.pixMap = QImage()
            self.pixMap.loadFromData(data)
            if self.pixMap.isNull():
                self.pixMap = _decode_bytes_to_qimage(data)
            self.pixMap.setDevicePixelRatio(dpr)

            size = ToolUtil.GetDownloadSize(len(data))
            self.sizeLabel.setText(size)
            self.format.setText(mat)
            self.resolutionLabel.setText(str(width) + "x" + str(height))
        else:
            width = self._curW
            height = self._curH
            isAnima = self._curIsAnima
            self.pixMap.setDevicePixelRatio(dpr)

        srcW = width if width > 0 else self.pixMap.width()
        srcH = height if height > 0 else self.pixMap.height()

        viewW = max(1, self.graphicsView.viewport().width())
        viewH = max(1, self.graphicsView.viewport().height())
        scale = max(0.1, 1.0 + self.scaleCnt * 0.1)
        toW = max(1, int(viewW * scale))
        toH = max(1, int(viewH * scale))

        if srcW > 0 and srcH > 0:
            ratio = min(toW / srcW, toH / srcH)
            dispW = max(1, int(round(srcW * ratio)))
            dispH = max(1, int(round(srcH * ratio)))
        else:
            dispW, dispH = toW, toH

        pos = QPointF(max(0.0, (viewW - dispW) / 2.0), max(0.0, (viewH - dispH) / 2.0))
        self.graphicsItem.setPos(pos)
        self.graphicsScene.setSceneRect(0, 0, max(viewW, dispW), max(viewH, dispH))

        if isAnima:
            if same_data and self.graphicsItem.IsAnimatedActive():
                self.graphicsItem.SetDisplaySize(dispW, dispH, dpr)
            else:
                fallback_pm = QPixmap.fromImage(self.pixMap) if not self.pixMap.isNull() else QPixmap()
                self.graphicsItem.SetPaused(not self.isVisible())
                self.graphicsItem.SetAnimationData(data, srcW, srcH, dispW, dispH, dpr, fallback_pixmap=fallback_pm)
        else:
            data2 = QPixmap.fromImage(self.pixMap)
            data2.setDevicePixelRatio(dpr)
            newData = data2.scaled(int(round(dispW * dpr)), int(round(dispH * dpr)), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            newData.setDevicePixelRatio(dpr)
            self.graphicsItem.SetStaticPixmap(newData, dispW, dispH)

        self.CheckScaleRadio()
        self.graphicsView.update()

    # def ScalePicture(self, data):
    #
    #     radio = data.devicePixelRatio()
    #     toW, toH = QtFileData.GetReadScale(self.qtTool.stripModel, self.scaleCnt, self.width(), self.height(), False)
    #     data2 = QPixmap(data)
    #     newData = data2.scaled(toW * radio, toH * radio, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     label.setPos(pos)
    #     # print("set index, {}".format(index))
    #     label.setPixmap(newData)

        # rect = QRectF(self.graphicsItem.pos(), QSizeF(
        #     self.pixMap.size()))
        # unity = self.graphicsView.transform().mapRect(QRectF(0, 0, 1, 1))
        # width = unity.width()
        # height = unity.height()
        # if width <= 0 or height <= 0:
        #     return
        # self.graphicsView.scale(1 / width, 1 / height)
        # viewRect = self.graphicsView.viewport().rect()
        # sceneRect = self.graphicsView.transform().mapRect(rect)
        # if sceneRect.width() <= 0 or sceneRect.height() <= 0:
        #     return
        # x_ratio = viewRect.width() / sceneRect.width()
        # y_ratio = viewRect.height() / sceneRect.height()
        # x_ratio = y_ratio = min(x_ratio, y_ratio)
        #
        # self.graphicsView.scale(x_ratio, y_ratio)
        # # if self.readImg.isStripModel:
        # #     height2 = self.pixMap.size().height() / 2
        # #     height3 = self.graphicsView.size().height()/2
        # #     height3 = height3/x_ratio
        # #     p = self.graphicsItem.pos()
        # #     self.graphicsItem.setPos(p.x(), p.y()+height2-height3)
        # self.graphicsView.centerOn(rect.center())
        #
        # for _ in range(abs(self.scaleCnt)):
        #     if self.scaleCnt > 0:
        #         self.graphicsView.scale(1.1, 1.1)
        #     else:
        #         self.graphicsView.scale(1/1.1, 1/1.1)

    def keyReleaseEvent(self, ev):
        if ev.key() == Qt.Key_Escape:
            # self.hide()
            ev.ignore()
            return
        if ev.key() == Qt.Key_Plus or ev.key() == Qt.Key_Equal:
            self.zoomIn()
            return
        if ev.key() == Qt.Key_Minus:
            self.zoomOut()
            return
        super(self.__class__, self).keyReleaseEvent(ev)

    def resizeEvent(self, event) -> None:
        super(self.__class__, self).resizeEvent(event)
        self.CheckShowImg()

    def showEvent(self, event) -> None:
        super(self.__class__, self).showEvent(event)
        self.graphicsItem.SetPaused(False)

    def hideEvent(self, event) -> None:
        super(self.__class__, self).hideEvent(event)
        self.graphicsItem.SetPaused(True)

    def closeEvent(self, event) -> None:
        self.graphicsItem.ClearAnimation()
        super(self.__class__, self).closeEvent(event)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:

            return True
        elif ev.type() == QEvent.GraphicsSceneMousePress:
            if ev.button() == Qt.ForwardButton:
                return True
            elif ev.button() == Qt.BackButton:
                return True
            return False
        elif ev.type() == QEvent.GraphicsSceneMouseRelease:
            if ev.button() == Qt.ForwardButton:
                return True
            elif ev.button() == Qt.BackButton:
                return True
            return False
        else:
            return super(self.__class__, self).eventFilter(obj, ev)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.ForwardButton:
            # QtOwner().SwitchWidgetNext()
            event.ignore()
        elif event.button() == Qt.BackButton:
            event.ignore()
            # QtOwner().SwitchWidgetLast()
        return super(self.__class__, self).mousePressEvent(event)

    def wheelEvent(self, event):
        if (QApplication.keyboardModifiers() == Qt.ControlModifier):
            if event.angleDelta().y() < 0:
                self.zoomOut()
                # self.Scale(1/1.1)
            #     self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() - 10)
            else:
                self.zoomIn()
                # self.frame.scaleCnt += 1
                # self.Scale(1.1)
            #     self.qtTool.zoomSlider.setValue(self.qtTool.zoomSlider.value() + 10)
            # print("scale:{}".format(self.frame.scaleCnt))
            return
        # if event.angleDelta().y() > 0:
        #     self.zoomIn()
        # else:
        #     self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1.1)

    def zoomOut(self):
        """缩小"""
        self.zoom(1/1.1)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        # _factor = self.graphicsView.transform().scale(
        #     factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        # if _factor < 0.07 or _factor > 100:
        #     # 防止过大过小
        #     return
        if factor >= 1:
            self.scaleCnt += 1
        else:
            self.scaleCnt = max(-9, self.scaleCnt - 1)
        self.CheckShowImg()
        # self.graphicsView.scale(factor, factor)

    def CopyPicture(self):
        clipboard = QApplication.clipboard()
        clipboard.setImage(self.pixMap)
        QtOwner().ShowMsg(Str.GetStr(Str.CopySuc))
        return

    def ReduceScalePic(self):
        self.zoom(1/1.1)
        return

    def AddScalePic(self):
        self.zoom(1.1)
        return


    def _hasSupportedDropData(self, mimeData) -> bool:
        if mimeData is None:
            return False
        if mimeData.hasUrls():
            for url in mimeData.urls():
                if url.isLocalFile() and os.path.isfile(url.toLocalFile()):
                    return True
        if mimeData.hasImage():
            return True
        return False

    def dragEnterEvent(self, event):
        if self._hasSupportedDropData(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._hasSupportedDropData(event.mimeData()):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        try:
            if mimeData.hasUrls():
                for url in mimeData.urls():
                    if url.isLocalFile():
                        path = url.toLocalFile()
                        if os.path.isfile(path):
                            self.LoadPictureFile(path)
                            event.acceptProposedAction()
                            return
            if mimeData.hasImage():
                imgData = mimeData.imageData()
                if isinstance(imgData, QPixmap):
                    qimg = imgData.toImage()
                elif isinstance(imgData, QImage):
                    qimg = imgData
                else:
                    qimg = QImage()
                if not qimg.isNull():
                    ba = QByteArray()
                    buf = QBuffer(ba)
                    buf.open(QIODevice.WriteOnly)
                    qimg.save(buf, "PNG")
                    buf.close()
                    self.LoadPictureData(bytes(ba.data()))
                    event.acceptProposedAction()
                    return
        except Exception as ex:
            Log.Error(ex)
        event.ignore()

    def LoadPictureData(self, data: bytes) -> bool:
        try:
            if not data:
                return False
            data2 = ToolUtil.GetCanUseData(data)
            width, height, mat, isAnima = ToolUtil.GetPictureSize(data2)
            if not width or not height:
                QtOwner().ShowError(Str.GetStr(Str.NotSupportFmt))
                return False
            self.data = data2
            self.waifu2xData = None
            self.scaleCnt = 0
            self.tickLabel.setText("-")
            self.ClearConvert()
            self.backStatus = ""
            self.ShowImg(data2)
            return True
        except Exception as ex:
            Log.Error(ex)
        return False

    def LoadPictureFile(self, filePath: str) -> bool:
        try:
            if filePath and os.path.isfile(filePath):
                with open(filePath, "rb") as f:
                    data = f.read()
                return self.LoadPictureData(data)
        except Exception as ex:
            Log.Error(ex)
        return False

    def OpenPicture(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "Open Image", ".", "Image Files(*)")
            if filename and len(filename) >= 1:
                self.LoadPictureFile(filename[0])
        except Exception as ex:
            Log.Error(ex)
        return

    def StartWaifu2x(self):
        if not self.data:
            return
        if not config.CanWaifu2x:
            return
        from sr_vulkan import sr_vulkan as sr
        self.modelName.setEnabled(False)
        # self.comboBox.setEnabled(False)
        self.changeButton.setEnabled(False)
        self.SetStatus(False)
        if self.fmtComboBox.currentIndex() == 0:
            fmt = ""
        else:
            fmt = str(self.fmtComboBox.currentText()).lower()
        # self.index = self.modelName.text()
        # self.index = self.comboBox.currentIndex()
        # index = self.comboBox.currentIndex()
        # noise = int(self.noiseCombox.currentText())

        modelInsence = self.modelName.toolTip()
        if self.ttaModel.isChecked():
            modelInsence += "_TTA"

        model = {
            "model":  getattr(sr, modelInsence),
            "format": fmt
        }
        if self.scaleRadio.isChecked():
            model['scale'] = round(float(self.scaleEdit.text()), 1)
        else:
            model['width'] = int(self.widthEdit.text())
            model['high'] = int(self.heighEdit.text())
        # _, _, mat = ToolUtil.GetPictureSize(self.data)
        # model["format"] = mat
        self.backStatus = self.GetStatus()
        self.AddConvertTask("", self.data, model, self.AddConvertBack)
        self.changeButton.setText(Str.GetStr(Str.Converting))
        return

    def AddConvertBack(self, data, waifuId, backParam, tick):
        if data:
            self.waifu2xData = data
            if self.checkBox.isChecked():
                self.ShowImg(data)
            self.changeButton.setText(Str.GetStr(Str.ConvertSuccess))
            self.tickLabel.setText(str(round(tick, 3)) + "s")
            self.changeButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)
        self.SetStatus(True)
        self.modelName.setEnabled(True)
        # self.comboBox.setEnabled(True)
        return

    def SavePicture(self):
        data = self.waifu2xData if self.waifu2xData else self.data
        if not data:
            return
        try:
            today = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            filepath = QFileDialog.getSaveFileName(self, Str.GetStr(Str.Save), "{}.{}".format(today, self.format.text()))
            if filepath and len(filepath) >= 1:
                name = filepath[0]
                if not name:
                    return
                f = open(name, "wb")
                f.write(data)
                f.close()
        except Exception as es:
            Log.Error(es)
        return

    def SwithPicture(self):
        if self.checkBox.isChecked() and self.waifu2xData:
            self.ShowImg(self.waifu2xData)
        else:
            self.ShowImg(self.data)
        return

    def CheckShowImg(self):
        if self.checkBox.isChecked() and self.waifu2xData:
            self.ShowImg(self.waifu2xData)
        else:
            self.ShowImg(self.data)
        return

    # def ChangeModel(self, index):
    #     if self.comboBox.currentIndex() == self.index:
    #         return
    #     # self.index = self.comboBox.currentIndex()
    #     self.changeButton.setText(Str.GetStr(Str.Convert))
    #     self.changeButton.setEnabled(True)
    #     return

    def GetStatus(self):
        data = \
            str(self.buttonGroup_2.checkedId()) + \
            str(self.scaleEdit.text()) + \
            str(self.heighEdit.text()) + \
            str(int(self.ttaModel.isChecked())) + \
            str(self.widthEdit.text()) + \
            str(self.modelName.toolTip()) + str(self.fmtComboBox.currentText())
        return data

    def SetStatus(self, status):
        self.scaleRadio.setEnabled(status)
        self.heighRadio.setEnabled(status)
        self.scaleEdit.setEnabled(status)
        self.widthEdit.setEnabled(status)
        self.heighEdit.setEnabled(status)
        self.fmtComboBox.setEnabled(status)
        # self.noiseCombox.setEnabled(status)
        # self.radioButton_4.setEnabled(status)
        # self.radioButton_5.setEnabled(status)
        # self.radioButton_6.setEnabled(status)
        # self.radioButton_7.setEnabled(status)
        # self.radioButton_8.setEnabled(status)
        # self.ttaModel.setEnabled(status)
        self.CheckScaleRadio()

    def SetEnable(self):
        self.SetStatus(True)

    def SetDisEnable(self):
        self.SetStatus(False)

    def CheckScaleRadio(self):
        if self.scaleRadio.isChecked() and self.scaleRadio.isEnabled():
            self.scaleEdit.setEnabled(True)
            self.widthEdit.setEnabled(False)
            self.heighEdit.setEnabled(False)
        elif self.heighRadio.isChecked() and self.heighRadio.isEnabled():
            self.scaleEdit.setEnabled(False)
            self.widthEdit.setEnabled(True)
            self.heighEdit.setEnabled(True)
        data = self.GetStatus()
        if self.backStatus != data:
            self.changeButton.setEnabled(True)
            self.changeButton.setText(Str.GetStr(Str.Convert))
        else:
            self.changeButton.setEnabled(False)
            self.changeButton.setText(Str.GetStr(Str.Convert))

    def SetHead(self):
        data = self.waifu2xData if self.waifu2xData else self.data
        if not data:
            return
        QtOwner().owner.navigationWidget.SetPicture(data)
        QtOwner().ShowMsg(Str.GetStr(Str.HeadUpload))
        # QtImgMgr().SetHeadStatus(not self.isHeadUp)