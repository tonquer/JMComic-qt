import io
import sys
import threading
import time

from PIL import Image, ImageOps
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt

from task.qt_task import TaskBase
from tools.log import Log
from tools.tool import ToolUtil
from view.read.read_perf_probe import Timer

try:
    import pillow_jxl  # noqa: F401
    import pillow_avif  # noqa: F401
except Exception:
    pass


def _decode_bytes_to_qimage(data: bytes, tw: int = 0, th: int = 0) -> QImage:
    """在后台线程用 Pillow 解码并构造 QImage，避免 PySide6 的 QImageReader(QBuffer)
    在后台线程持 Qt QFactoryLoader 锁回调 QBufferWrapper 抢 GIL，与主线程
    QMovie.start()（持 GIL 等 QFactoryLoader 锁）发生 AB-BA 死锁。"""
    if not data:
        return QImage()
    try:
        with io.BytesIO(data) as bio, Image.open(bio) as im:
            is_anim = getattr(im, "is_animated", False)
            if is_anim:
                im.seek(0)
            exif = im.getexif()
            has_exif_rot = bool(exif and exif.get(274, 1) != 1)
            if (not is_anim and not has_exif_rot and im.format == "JPEG"
                    and tw > 0 and (im.width > tw or (th > 0 and im.height > th))):
                draft_h = th if th > 0 else max(1, round(im.height * (tw / im.width)))
                im.draft("RGB", (tw, draft_h))
            if has_exif_rot:
                im = ImageOps.exif_transpose(im)
            has_alpha = (
                im.mode in ("RGBA", "LA", "PA")
                or (im.mode == "P" and "transparency" in im.info)
            )
            im_rgba = im.convert("RGBA") if im.mode != "RGBA" else im
            w, h = im_rgba.width, im_rgba.height
            if sys.byteorder == "little":
                raw = im_rgba.tobytes("raw", "BGRA")
                fmt = QImage.Format_ARGB32 if has_alpha else QImage.Format_RGB32
            else:
                raw = im_rgba.tobytes("raw", "RGBA")
                fmt = QImage.Format_RGBA8888
            return QImage(raw, w, h, w * 4, fmt).copy()
    except Exception:
        # 兜底走 Qt 纯 C++ 内部缓冲的 loadFromData（不经过 Python QBufferWrapper，无死锁风险）
        q = QImage()
        newData = ToolUtil.GetCanUseData(data)
        q.loadFromData(newData)
        return q


class QtQImageTask(object):
    def __init__(self, taskId):
        self.taskId = taskId
        self.callBack = None
        self.backParam = None
        self.cleanFlag = ""
        self.data = ""
        self.radio = 1
        self.toH = 0
        self.toW = 0
        self.model = 0


class TaskQImage(TaskBase):

    def __init__(self):
        TaskBase.__init__(self)
        self.taskObj.imageBack.connect(self.HandlerTask)
        self.threadNum = 4
        self.threadList = []
        for i in range(self.threadNum+1):
            thread = threading.Thread(target=self.Run)
            thread.name = "Task-" + str(self.__class__.__name__)+str(i)
            thread.daemon = True
            thread.start()
            self.threadList.append(thread)

    def Stop(self):
        for i in range(self.threadNum+1):
            self._inQueue.put("")
        return

    def Run(self):
        while True:
            try:
                v = self._inQueue.get(True)
                if v == "":
                    break
                taskId = v
            except Exception as es:
                continue
            self._inQueue.task_done()

            if taskId < 0:
                break

            info = self._GetTask(taskId)
            if not info:
                continue
            newQ = QImage()
            try:
                target_w = round(info.toW * info.radio) if info.toW > 0 else 0
                target_h = round(info.toH * info.radio) if info.toH > 0 else 0
                q = _decode_bytes_to_qimage(info.data, target_w, target_h)
                if not q.isNull():
                    if info.model:
                        model = info.model
                    else:
                        model = Qt.KeepAspectRatio
                    if 0 < target_w < q.width() and target_h == 0:
                        newQ = q.scaledToWidth(target_w, Qt.SmoothTransformation)
                    elif target_w > 0 and target_h > 0:
                        newQ = q.scaled(target_w, target_h, model, Qt.SmoothTransformation)
                    else:
                        newQ = q
                    newQ.setDevicePixelRatio(info.radio)
            except Exception as es:
                Log.Error(es)
            finally:
                self.taskObj.imageBack.emit(taskId, newQ)

    def AddQImageTask(self, data, radio, toW, toH, model, callBack=None, backParam=None, cleanFlag=None):
        info = QtQImageTask(0)
        info.callBack = callBack
        info.backParam = backParam
        info.data = data
        info.radio = radio
        info.toW = toW
        info.toH = toH
        info.model = model

        taskId = self._RegisterTask(info, cleanFlag)
        self._inQueue.put(taskId)
        return taskId

    def ClearQImageTaskById(self, taskId):
        self._TakeTask(taskId)

    def HandlerTask(self, taskId, newData):
        try:
            info = self._TakeTask(taskId)
            if not info:
                return
            assert isinstance(info, QtQImageTask)
            if info.callBack:
                if info.backParam is None:
                    info.callBack(newData)
                else:
                    info.callBack(newData, info.backParam)
        except Exception as es:
            Log.Error(es)
