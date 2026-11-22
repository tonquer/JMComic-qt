from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from view.read.read_new_frame import ReadNewFrame
    from view.read.read_new_view import ReadNewView
    from view.read.read_new_task import ReadNewTask

import sys
import weakref

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel

from component.label.msg_label import MsgLabel
from config import config
from config.setting import Setting
from interface.ui_read_tool import Ui_ReadImg
from qt_owner import QtOwner
from tools.str import Str
from tools.tool import CTime, ToolUtil
from view.read.read_enum import ReadMode, QtFileData
from view.read.read_new_graphics import ReadNewGraphics


class QtCustomSlider(QtWidgets.QSlider):
    def __init__(self, parent):
        QtWidgets.QSlider.__init__(self)
        self.label = QLabel(self)
        self._qtTool = weakref.ref(parent)
        self.label.setFixedSize(QSize(20, 20))
        self.label.setAutoFillBackground(True)
        self.label.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, Qt.white)
        # self.label.setPalette(palette)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setVisible(False)
        self.label.move(0, 3)
        self.setMaximum(100)
        self.setOrientation(Qt.Horizontal)
        self.setPageStep(0)

    @property
    def qtTool(self) -> ReadNewTool:
        return self._qtTool()

    def mousePressEvent(self, event):
        if not self.label.isVisible():
            self.label.setVisible(True)
        x = event.pos().x()
        w = max(1, self.width())
        pos = min(1.0, max(0.0, x / w))

        span = max(1, self.maximum() - self.minimum())
        size = int(w * (self.value() - self.minimum()) / span)

        if not (size - 5 <= x <= size + 5):
            self.setValue(int(round(pos * (self.maximum() - self.minimum()) + self.minimum())))
            self.label.setText(str(self.value()))
            size = int((self.width() - self.label.width()) * (self.value() - self.minimum()) / span)
            self.label.move(size, 3)
        super(self.__class__, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.label.isVisible():
            self.label.setVisible(False)
            self.qtTool.SkipPicture(self.value() - 1)
        super(self.__class__, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.label.setText(str(self.value()))
        span = max(1, self.maximum() - self.minimum())
        size = int((self.width() - self.label.width()) * (self.value() - self.minimum()) / span)
        self.label.move(size, 3)
        super(self.__class__, self).mouseMoveEvent(event)

    def leaveEvent(self, event):
        super(self.__class__, self).leaveEvent(event)

    def keyPressEvent(self, event):
        return

    def keyReleaseEvent(self, event) -> None:
        return


class ReadNewTool(QtWidgets.QWidget, Ui_ReadImg):

    def __init__(self, imgFrame):
        QtWidgets.QWidget.__init__(self, imgFrame)
        Ui_ReadImg.__init__(self)
        self.setupUi(self)
        self.resize(100, 400)
        self._imgFrame = weakref.ref(imgFrame)
        self.downloadMaxSize = 0
        self.downloadSize = 0
        self.slider = QtCustomSlider(self)
        self.horizontalLayout_7.addWidget(self.slider)
        self.SetWaifu2xCancle()
        self.scaleBox.installEventFilter(self)
        self.zoomSlider.setMinimum(int(100*ReadNewGraphics.MIN_ZOOM))
        self.zoomSlider.setMaximum(int(100*ReadNewGraphics.MAX_ZOOM))

        self.isMaxFull = False
        self.gpuLabel.setMaximumWidth(250)
        self.curWaifu2x.clicked.connect(self.OpenCurWaifu)
        self.preDownWaifu2x.clicked.connect(self.OpenPreDownloadWaifu2x)
        self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.modelNameButton.setToolTip(Setting.LookModelName.value)
        self.modelNameButton.clicked.connect(self.OpenSrSelect)
        self.modelNameButton.setEnabled(False)
        self.openGLBox.setChecked(bool(Setting.IsOpenOpenGL.value))
        self.openGLBox.clicked.connect(self.SwitchOpenGL)
        self.animeBox.setChecked(bool(Setting.IsOpenReadAnime.value))
        self.animeBox.clicked.connect(self.SwitchAnime)
        self.switchDouble.clicked.connect(self.SwitchDouble)

    def SwitchDouble(self):
        self.scrollArea.change_double_page()
        self.switchDouble.setChecked(self.scrollArea._is_cover_mode)

    def SwitchAnime(self):
        Setting.IsOpenReadAnime.SetValue(int(self.animeBox.isChecked()))
        self.scrollArea.set_page_animation_enabled(self.animeBox.isChecked())

    def SwitchOpenGL(self, value):
        Setting.IsOpenOpenGL.SetValue(int(value))
        self.scrollArea.set_opengl(bool(value))

    def OpenSrSelect(self):
        QtOwner().OpenSrSelectModel(self.modelNameButton.toolTip(), self.OpenSrSelectBack)

    def OpenSrSelectBack(self, newModName):
        Setting.LookModelName.SetValue(newModName)
        self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
        self.modelNameButton.setToolTip(Setting.LookModelName.value)
        self.UpdateText(None)
        self.scrollArea.reset_waifu2x_results()

    @property
    def imgFrame(self) -> ReadNewFrame:
        return self._imgFrame()

    @property
    def scrollArea(self) -> ReadNewGraphics:
        return self.readImg.scrollArea

    @property
    def readImg(self) -> ReadNewView:
        return self.imgFrame.readImg

    @property
    def readTask(self) -> ReadNewTask:
        return self.scrollArea.read_task

    @property
    def curIndex(self):
        return self.scrollArea._cur_idx

    @property
    def maxPic(self):
        return self.readImg.maxPic

    @property
    def stripModel(self):
        return self.scrollArea._mode

    def Show(self, size):
        self.show()

    def Close(self, size):
        self.hide()

    @property
    def scaleCnt(self):
        return self.imgFrame.scaleCnt

    @scaleCnt.setter
    def scaleCnt(self, value):
        self.imgFrame.scaleCnt = value

    def NextPage(self):
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._LastPage()
        else:
            self._NextPage()
        # self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

    def _NextPage(self):
        epsId = self.readImg.epsId
        if not ReadMode.isScroll(self.stripModel):
            next_page = self.scrollArea._page + 1
            at_end = self.maxPic <= 0 or next_page > self.scrollArea._max_page()
            index = self.scrollArea._page_first_index(next_page) if not at_end else self.maxPic
        else:
            index = self.scrollArea._cur_idx + 1
            at_end = index >= self.maxPic

        if at_end:
            if self.readImg.isLocal:
                self.OpenNextEps()
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                return
            elif self.readImg.isOffline:
                if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId + 1):
                    QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                    return
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                self.OpenNextEps()
            else:
                if not self.readTask.IsMaxBookEps(epsId+1):
                    QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipNext))
                    self.OpenNextEps()
                return
            # QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextPage))
            return

        self.scrollArea.jump_to_index(index)
        return

    def LastPage(self):
        if self.stripModel in [ReadMode.RightLeftDouble, ReadMode.RightLeftScroll]:
            self._NextPage()
        else:
            self._LastPage()
        # self.curWaifu2x.setChecked(bool(self.readImg.GetIsWaifu2x()))

    def _LastPage(self):
        epsId = self.readImg.epsId
        if not ReadMode.isScroll(self.stripModel):
            prev_page = self.scrollArea._page - 1
            at_start = self.maxPic <= 0 or prev_page < 0
            index = self.scrollArea._page_first_index(prev_page) if not at_start else 0
        else:
            at_start = self.curIndex <= 0
            index = self.scrollArea._cur_idx - 1

        if at_start:
            if self.readImg.isLocal:
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipLast))
                self.OpenLastEps()
                return
            elif self.readImg.isOffline:
                if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId - 1):
                    QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                    return
            if epsId - 1 >= 0:
                QtOwner().ShowMsg(Str.GetStr(Str.AutoSkipLast))
                self.OpenLastEps()
                return
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastPage))
            return

        self.scrollArea.jump_to_index(index)
        return

    def ReturnPage(self):
        # self.readImg.hide()
        # self.hide()
        # QtOwner().owner.bookInfoForm.show()
        self.readImg.Close()
        # QtOwner().owner.bookInfoForm.LoadHistory()
        # self.readImg.Clear()
        return

    def SetData(self, pSize=None, dataLen=0, state="",
                waifuSize=None, waifuDataLen=0,
                waifuState="", waifuTick=0,
                isInit=False):
        if self.readImg.epsName:
            QtOwner().SetSubTitle(self.readImg.epsName + "（{}/{}）".format(self.slider.value(), self.slider.maximum()))

        self.epsLabel2.setText("{}/{}({}_{})".format(self.slider.value(), self.slider.maximum(), self.readImg.epsId+1, self.readImg.epsName))
        if pSize or isInit:
            if not pSize:
                pSize = QSize(0, 0)
            self.resolutionLabel2.setText("{}x{}".format(str(pSize.width()), str(pSize.height())))

        if dataLen or isInit:
            self.sizeLabel2.setText(ToolUtil.GetDownloadSize(dataLen))

        if waifuSize or isInit:
            if not waifuSize:
                waifuSize = QSize(0, 0)
            self.waifu2xRes.setText("{}x{}".format(str(waifuSize.width()), str(waifuSize.height())))
        if waifuDataLen or isInit:
            self.waifu2xSize.setText("" + ToolUtil.GetDownloadSize(waifuDataLen))

        if state or isInit:
            self.stateLable2.setText(Str.GetStr(state))

        if waifuState or isInit:
            if waifuState == QtFileData.WaifuStateStart:
                self.waifu2xStatus.setStyleSheet("color:red;")
            elif waifuState == QtFileData.WaifuStateEnd:
                self.waifu2xStatus.setStyleSheet("color:green;")
            elif waifuState == QtFileData.WaifuStateFail:
                self.waifu2xStatus.setStyleSheet("color:red;")
            else:
                self.waifu2xStatus.setStyleSheet("color:dark;")
            if config.CanWaifu2x:
                self.waifu2xStatus.setText(Str.GetStr(waifuState))
        if waifuTick or isInit:
            self.waifu2xTick.setText(str(waifuTick) + "s")

    # def CopyPicture(self):
    #     owner = self.readImg
    #     p = owner.pictureData.get(owner.curIndex)
    #     if not p or not p.data:
    #         MsgLabel.ShowErrorEx(owner, Str.GetStr(Str.DownloadNot))
    #         return
    #     # TODO
    #     # QtOwner().OpenWaifu2xTool(p.data)
    #     return

    def OpenCurWaifu(self):
        if self.curWaifu2x.isChecked():
            self.scrollArea.open_waifu2x_state(self.scrollArea._cur_idx)
        else:
            self.scrollArea.close_waifu2x_state(self.scrollArea._cur_idx)
        # if self.curWaifu2x.isChecked():
        #     self.readImg.SetIsWaifu2x(1)
        # else:
        #     self.readImg.SetIsWaifu2x(0)
        # # self.scrollArea.changeScale.emit(self.scaleCnt)
        # self.readImg.ShowImgAll()
        # self.readImg.CheckLoadPicture()
        return

    def OpenPreDownloadWaifu2x(self):
        Setting.PreDownWaifu2x.SetValue(int(self.preDownWaifu2x.isChecked()))
        return

    def OpenWaifu(self):
        if self.checkBox.isChecked():
            Setting.IsOpenWaifu.SetValue(1)
            if config.EncodeGpu == "CPU":
                QtOwner().ShowMsg(Str.GetStr(Str.NotRecommendWaifu2x))
        else:
            Setting.IsOpenWaifu.SetValue(0)

        # self.readImg.ShowImgAll()
        self.scrollArea.check_waifu2x_state()
        return

    def UpdateText(self, model):
        if not model:
            self.scaleLabel.setText(str(Setting.LookScale.value))
            self.modelNameButton.setText(ToolUtil.GetShowModelName(Setting.LookModelName.value))
            self.modelNameButton.setToolTip(Setting.LookModelName.value)
        else:
            scale = model.get('scale', 0)
            modelName = model.get('model_name', "")
            self.scaleLabel.setText(str(scale))
            self.modelNameButton.setText(ToolUtil.GetShowModelName(modelName))
            self.modelNameButton.setToolTip(modelName)
        self.gpuLabel.setText(QtOwner().settingView.GetGpuName())

    def OpenLastEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId

        lasEps = epsId - 1
        if self.readImg.isLocal:
            if lasEps < 0:
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastChapter))
                return
            self.readImg.OpenLocalPage(self.readImg._cacheBook, lasEps, 9999)
            return
        elif self.readImg.isOffline:
            if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId - 1):
                QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                return
        else:
            if self.readTask.IsMaxBookEps(lasEps):
                return

        if lasEps < 0:
            QtOwner().ShowMsg(Str.GetStr(Str.AlreadyLastChapter))
            return

        self.readImg.AddHistory()
        QtOwner().ReloadBookInfoHistory()
        self.readImg.OpenPage(bookId, lasEps, 9999, self.readImg.isOffline)
        return

    def OpenNextEps(self):
        epsId = self.readImg.epsId
        bookId = self.readImg.bookId
        nextEps = epsId + 1
        if self.readImg.isLocal:
            if nextEps >= len(self.readImg._cacheBook.eps):
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextChapter))
                return
            self.readImg.OpenLocalPage(self.readImg._cacheBook, nextEps, 0)
            return
        elif self.readImg.isOffline:
            if not QtOwner().downloadView.IsDownloadEpsId(self.readImg.bookId, self.readImg.epsId + 1):
                QtOwner().ShowMsg(Str.GetStr(Str.NotDownload))
                return
        else:
            if self.readTask.IsMaxBookEps(nextEps):
                QtOwner().ShowMsg(Str.GetStr(Str.AlreadyNextChapter))
                return

        # title = bookInfo.GetEpsTitle(epsId)
        self.readImg.AddHistory()
        QtOwner().ReloadBookInfoHistory()
        self.readImg.OpenPage(bookId, nextEps, isOffline=self.readImg.isOffline)
        return

    def SkipPicture(self, index=0):
        self.scrollArea.jump_to_index(index)

    def InitSlider(self, maxIndex):
        self.slider.setMinimum(1)
        self.slider.setMaximum(max(1, maxIndex))

    def UpdateSlider(self):
        return
        # self.slider.setValue(self.readImg.curIndex + 1)

    def FullScreen(self, isClear=False):
        if QtOwner().owner.windowState() == Qt.WindowFullScreen:
            if not sys.platform == "darwin":
                if QtOwner().isMaxSize:
                    QtOwner().owner.showMaximized()
                else:
                    QtOwner().owner.showNormal()
            else:
                pass
                # QtOwner().owner.showNormal()
            self.fullButton.setText(Str.GetStr(Str.FullScreen))
            if not isClear:
                Setting.LookReadFull.SetValue(0)
        else:
            QtOwner().owner.BackOldSize()
            # self.isMaxFull = self.window().isMaximized()
            if QtOwner().isMaxSize:
                QtOwner().owner.showNormal()
            QtOwner().owner.showFullScreen()
            self.fullButton.setText(Str.GetStr(Str.ExitFullScreen))
            Setting.LookReadFull.SetValue(1)

    def Waifu2xSave(self):
        self.scaleBox.setValue(Setting.LookScale.value)
        self.SetWaifu2xCancle(True)

    def Waifu2xCancle(self):
        oldModel = Setting.LookModelName.value
        oldScale = Setting.LookScale.value
        if self.modelNameButton.toolTip():
            Setting.LookModelName.SetValue(self.modelNameButton.toolTip())
        # Setting.LookNoise.SetValue(self.noiseBox.currentIndex() -1)
        Setting.LookScale.SetValue(self.scaleBox.value())
        self.UpdateText(None)
        self.SetWaifu2xCancle(False)
        if oldModel != Setting.LookModelName.value or oldScale != Setting.LookScale.value:
            self.scrollArea.reset_waifu2x_results()

    def SetWaifu2xCancle(self, isVisibel=False):
        self.waifu2xSave.setVisible(not isVisibel)
        # self.noiseLabel.setVisible(not isVisibel)
        self.scaleLabel.setVisible(not isVisibel)
        # self.modelLabel.setVisible(not isVisibel)
        # self.modelNameButton.setVisible(isVisibel)
        self.modelNameButton.setEnabled(isVisibel)
        self.waifu2xCancle.setVisible(isVisibel)
        # self.noiseBox.setVisible(isVisibel)
        self.scaleBox.setVisible(isVisibel)
        # self.modelBox.setVisible(isVisibel)

    def ScalePicture2(self, value):
        self.zoomSlider.setValue(value)

    def ScalePicture(self, value):
        self.zoomLabel.setText(Str.GetStr(Str.Scale) + f"({value}%)")
        self.scrollArea.set_zoom(value/100, None)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyRelease:
            return True
        elif ev.type() == QEvent.KeyPress:
            return True
        return False

    def ChangeReadMode(self, index):
        self.comboBox.setCurrentIndex(index)
        self.imgFrame.InitHelp()
        self.imgFrame.ShowHelp()

    def ChangeReadMode2(self, index):
        Setting.LookReadMode.SetValue(index)
        self.scrollArea.set_mode(index)
        return

    def SwitchScrollAndTurn(self):
        if self.IsStartScrollAndTurn():
            self.CloseScrollAndTurn()
        else:
            self.StartScrollAndTurn()
        return

    def StartScrollAndTurn(self):
        self.CloseScrollAndTurn()
        if ReadMode.isScroll(self.scrollArea._mode):
            self.scrollArea.set_auto_scroll(Setting.ScrollSpeed.value)
        else:
            self.scrollArea.set_auto_scroll(Setting.TurnSpeed.value/ 1000)

    def CloseScrollAndTurn(self):
        if self.IsStartScrollAndTurn():
            QtOwner().ShowMsg(Str.GetStr(Str.StopAutoScroll))
            self.scrollArea.stop_auto()
        pass

    def IsStartScrollAndTurn(self):
        return self.scrollArea.is_auto

