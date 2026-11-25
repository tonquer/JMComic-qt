import os
import re
import sys
from contextlib import contextmanager, ExitStack
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, Qt, QUrl, QFile, QTranslator, QLocale, QEvent, QObject, QSignalBlocker
from PySide6.QtGui import QDesktopServices, QFontDatabase
from PySide6.QtWidgets import QFileDialog, QScroller, QScrollerProperties, QToolTip

from config import config
from config.setting import Setting, SettingValue
from interface.ui_setting_new import Ui_SettingNew
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from view.setting.setting_binding import BindCheck, BindRadio, BindLine, BindIndex, BindValue, BindSpin


class SettingView(QtWidgets.QWidget, Ui_SettingNew):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_SettingNew.__init__(self)
        self._settingControlsReady = False
        self._settingBindingsConnected = False
        self._appliedTheme = None
        self.setupUi(self)

        self.mainSize = None
        self.bookSize = None
        self.readSize = None
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        self.translate = QTranslator()
        self.fontBox.setItemData(0, "")
        for name in QFontDatabase.families():
            self.fontBox.addItem(name, name)
        self.fontSize.setItemData(0, "")
        for index in range(1, self.fontSize.count()):
            self.fontSize.setItemData(index, self.fontSize.itemText(index))

        self._settingBindings = self._CreateSettingBindings()
        self._modelBindings = (
            (Setting.LookModelName, self.readModelName),
            (Setting.CoverLookModelName, self.coverModelName),
            (Setting.DownloadModelName, self.downModelName),
        )
        self._ConnectSettingBindings()
        for setting, button in self._modelBindings:
            button.setText(setting.setV)

        self.generalButton.clicked.connect(partial(self.MoveToLabel, self.generalLabel))
        # self.prefetchButton.clicked.connect(partial(self.MoveToLabel, self.prefetchLabel))
        # self.readButton.clicked.connect(partial(self.MoveToLabel, self.readLabel))
        self.proxyButton.clicked.connect(partial(self.MoveToLabel, self.proxyLabel))
        self.waifu2xButton.clicked.connect(partial(self.MoveToLabel, self.waifu2xLabel))
        self.downloadButton.clicked.connect(partial(self.MoveToLabel, self.downloadLabel))

        self.setDirButton.clicked.connect(self.SelectSavePath)
        self.setLogDirButton.clicked.connect(self.SelectSaveLogPath)
        self.openDownloadDir.clicked.connect(partial(self.OpenDir, self.downloadDir))
        self.openChatDir.clicked.connect(partial(self.OpenDir, self.chatDir))
        self.openCacheDir.clicked.connect(partial(self.OpenDir, self.cacheDir))
        self.openWaifu2xDir.clicked.connect(partial(self.OpenDir, self.waifu2xDir))
        self.openLogDir.clicked.connect(partial(self.OpenDir, self.logLabel))

        self.openProxy.clicked.connect(QtOwner().OpenProxy)
        # TODO
        # self.languageButton3.setVisible(False)

        self.msgLabel.setVisible(False)

        self.prefetchHelpLabels = (
            self.prefetchCountHelp,
            # self.crossChapterPrefetchHelp,
            self.prefetchWholeChapterHelp,
            self.showCountHelp
        )
        for label in self.prefetchHelpLabels:
            label.setMouseTracking(True)
            label.setAttribute(Qt.WA_Hover, True)
            label.installEventFilter(self)

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy,
                                          QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy,
                                          QScrollerProperties.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)

        self._settingControlsReady = True
        self.diskRefreshButton.clicked.connect(self.StartUpdateDiskCache)
        self.InitBackupSection()
        #     QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)

    def InitBackupSection(self):
        """在设置页末尾追加「配置备份」区块

        这里用代码追加而不是改 .ui 文件，避免与上游的界面改动冲突。
        """
        frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        frame.setObjectName("backupFrame")
        hLayout = QtWidgets.QHBoxLayout(frame)
        hLayout.setContentsMargins(14, 12, 14, 12)
        hLayout.setSpacing(10)

        self.backupLabel = QtWidgets.QLabel("配置备份", frame)
        self.exportConfigButton = QtWidgets.QPushButton("导出配置", frame)
        self.importConfigButton = QtWidgets.QPushButton("导入配置", frame)
        self.exportConfigButton.setToolTip("把配置、搜索历史和下载记录打包成一个 zip 文件（内含账号登录凭据，请妥善保管）")
        self.importConfigButton.setToolTip("从导出的 zip 文件恢复配置，恢复后需要重启程序")

        self.exportConfigButton.clicked.connect(self.ExportConfig)
        self.importConfigButton.clicked.connect(self.ImportConfig)

        hLayout.addWidget(self.backupLabel)
        hLayout.addWidget(self.exportConfigButton)
        hLayout.addWidget(self.importConfigButton)
        hLayout.addStretch(1)
        self.verticalLayout_4.addWidget(frame)

    @staticmethod
    def GetBackupFileMap():
        """配置备份包含的文件：{归档内路径: 实际路径}"""
        fileMap = {
            "config/config.ini": os.path.join(Setting.GetConfigPath(), "config.ini"),
            "data/cache_word": os.path.join(Setting.GetDataPath(), "cache_word"),
        }
        for name in ("download.db", "favorite.db", "history.db",
                     "local_read.db", "nas.db", "batch_sr_tool.db"):
            fileMap["state/" + name] = os.path.join(Setting.GetStatePath(), name)
        return fileMap

    def ExportConfig(self):
        path, _ = QFileDialog.getSaveFileName(self, "导出配置", "jmcomic-config.zip", "Zip(*.zip)")
        if not path:
            return
        try:
            count = self.WriteBackupTo(path)
            QtOwner().ShowMsgOne("已导出 {} 个配置文件到：\n{}\n\n注意：文件内含账号和代理设置，请妥善保管".format(count, path))
        except Exception as es:
            Log.Error(es)
            QtOwner().ShowErrOne("导出配置失败：{}".format(es))

    def WriteBackupTo(self, path):
        """把配置打包写到 path，返回打包的文件数。

        先写临时文件再替换，避免中途失败留下半截 zip；
        .db 文件用 SQLite backup API 取一致性快照，不复制正在写入的裸文件。
        """
        import zipfile
        tmpPath = path + ".tmp"
        count = 0
        try:
            with zipfile.ZipFile(tmpPath, "w", zipfile.ZIP_DEFLATED) as zf:
                for name, srcPath in self.GetBackupFileMap().items():
                    if not os.path.isfile(srcPath):
                        continue
                    if name.endswith(".db"):
                        snapPath = self.SnapshotSqlite(srcPath)
                        if snapPath:
                            try:
                                zf.write(snapPath, name)
                            finally:
                                if os.path.isfile(snapPath):
                                    os.remove(snapPath)
                            count += 1
                            continue
                    zf.write(srcPath, name)
                    count += 1
            os.replace(tmpPath, path)
        finally:
            if os.path.isfile(tmpPath):
                os.remove(tmpPath)
        return count

    @staticmethod
    def SnapshotSqlite(srcPath):
        """对 SQLite 文件取快照，失败返回 None（由调用方退回普通复制）"""
        import sqlite3
        import tempfile
        snapPath = None
        src = dst = None
        ok = False
        try:
            fd, snapPath = tempfile.mkstemp(suffix=".db")
            os.close(fd)
            src = sqlite3.connect(srcPath)
            dst = sqlite3.connect(snapPath)
            src.backup(dst)
            ok = True
            return snapPath
        except Exception as es:
            Log.Warn("sqlite snapshot failed, fallback to raw copy, {}: {}".format(srcPath, es))
            return None
        finally:
            for con in (dst, src):
                if con is not None:
                    try:
                        con.close()
                    except Exception:
                        pass
            if not ok and snapPath and os.path.isfile(snapPath):
                try:
                    os.remove(snapPath)
                except Exception:
                    pass

    def ReadBackupFrom(self, path):
        """解压并校验备份文件，返回 ({归档内路径: 临时文件路径}, 临时目录)。

        在动任何现有文件之前，先确认压缩包完整、内容合法。
        """
        import zipfile
        import tempfile
        fileMap = self.GetBackupFileMap()
        tmpDir = tempfile.mkdtemp(prefix="jmcomic-import-")
        extracted = {}
        try:
            with zipfile.ZipFile(path, "r") as zf:
                for name in zf.namelist():
                    if name not in fileMap:
                        continue
                    data = zf.read(name)
                    if name.endswith(".db") and data[:16] != b"SQLite format 3\x00":
                        raise ValueError("{} 不是有效的数据库文件".format(name))
                    dest = os.path.join(tmpDir, name.replace("/", "_"))
                    with open(dest, "wb") as f:
                        f.write(data)
                    extracted[name] = dest
            if not extracted:
                raise ValueError("压缩包里没有可导入的配置文件")
            return extracted, tmpDir
        except Exception:
            import shutil
            shutil.rmtree(tmpDir, ignore_errors=True)
            raise

    def RestoreConfig(self, extracted):
        """把解压好的文件替换到位；任一步失败，回滚所有已替换的文件"""
        import shutil
        import sqlite3
        fileMap = self.GetBackupFileMap()
        backups = {}
        created = []
        try:
            for name, tmpPath in extracted.items():
                destPath = fileMap[name]
                os.makedirs(os.path.dirname(destPath), exist_ok=True)
                existed = os.path.isfile(destPath)
                if existed:
                    if name.endswith(".db"):
                        snap = self.SnapshotSqlite(destPath)
                        if snap:
                            try:
                                with open(snap, "rb") as f:
                                    backups[destPath] = f.read()
                            finally:
                                if os.path.isfile(snap):
                                    os.remove(snap)
                        else:
                            with open(destPath, "rb") as f:
                                backups[destPath] = f.read()
                    else:
                        with open(destPath, "rb") as f:
                            backups[destPath] = f.read()
                else:
                    created.append(destPath)
                if name.endswith(".db") and existed:
                    src = dst = None
                    try:
                        src = sqlite3.connect(tmpPath)
                        dst = sqlite3.connect(destPath)
                        src.backup(dst)
                    finally:
                        for con in (dst, src):
                            if con is not None:
                                try:
                                    con.close()
                                except Exception:
                                    pass
                else:
                    shutil.copyfile(tmpPath, destPath)
        except Exception:
            for destPath in created:
                try:
                    if os.path.isfile(destPath):
                        os.remove(destPath)
                except Exception as es:
                    Log.Error(es)
            for destPath, data in backups.items():
                try:
                    if destPath.endswith(".db") and os.path.isfile(destPath):
                        import tempfile
                        fd, rTmp = tempfile.mkstemp(suffix=".db")
                        os.close(fd)
                        src = dst = None
                        try:
                            with open(rTmp, "wb") as f:
                                f.write(data)
                            src = sqlite3.connect(rTmp)
                            dst = sqlite3.connect(destPath)
                            src.backup(dst)
                        finally:
                            for con in (dst, src):
                                if con is not None:
                                    try:
                                        con.close()
                                    except Exception:
                                        pass
                            if os.path.isfile(rTmp):
                                try:
                                    os.remove(rTmp)
                                except Exception:
                                    pass
                    else:
                        with open(destPath, "wb") as f:
                            f.write(data)
                except Exception as es:
                    Log.Error(es)
            raise

    def ImportConfig(self):
        path, _ = QFileDialog.getOpenFileName(self, "导入配置", "", "Zip(*.zip)")
        if not path:
            return
        try:
            # 先完整解压校验，再询问，最后替换；替换失败会自动回滚
            extracted, tmpDir = self.ReadBackupFrom(path)
        except Exception as es:
            Log.Error(es)
            QtOwner().ShowErrOne("导入配置失败：{}".format(es))
            return
        try:
            from PySide6.QtWidgets import QMessageBox
            ret = QMessageBox.question(
                self, "导入配置",
                "导入会覆盖当前配置，程序需要重启。\n\n"
                "注意：压缩包只含配置和记录（账号、收藏、下载清单等），"
                "不含漫画文件本身；如果原来的下载目录在这台电脑上不存在，"
                "导入后请到「下载与缓存」里重新选择。\n\n是否继续？",
                QMessageBox.Yes | QMessageBox.No)
            if ret != QMessageBox.Yes:
                return
            self.RestoreConfig(extracted)
            QtOwner().ShowMsgOne("已导入 {} 个配置文件，请重启程序后生效".format(len(extracted)))
        except Exception as es:
            Log.Error(es)
            QtOwner().ShowErrOne("导入配置失败，已保留原配置：{}".format(es))
        finally:
            import shutil
            shutil.rmtree(tmpDir, ignore_errors=True)

    #     self.grabGestureBox.installEventFilter(self)
    #
    def eventFilter(self, watched, event) -> bool:
        if watched in getattr(self, "prefetchHelpLabels", ()):
            if event.type() in (QEvent.Enter, QEvent.HoverEnter, QEvent.ToolTip):
                position = watched.mapToGlobal(watched.rect().bottomLeft())
                QToolTip.showText(position, watched.toolTip(), watched)
                return event.type() == QEvent.ToolTip
            if event.type() in (QEvent.Leave, QEvent.HoverLeave):
                QToolTip.hideText()
        return super(self.__class__, self).eventFilter(watched, event)

    def MoveToLabel(self, label):
        p = label.pos()
        self.scrollArea.vScrollBar.ScrollTo(p.y())
        return

    def CheckMsgLabel(self, notify=True):
        isNeed = False
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                if setItem.isNeedReset:
                    if setItem.value != setItem.setV:
                        isNeed = True
        if isNeed:
            self.msgLabel.setVisible(True)
            if notify:
                QtOwner().ShowErrOne(Str.GetStr(Str.NeedResetSave))
        else:
            self.msgLabel.setVisible(False)
        return

    def _CreateSettingBindings(self):
        return (
            BindRadio(Setting.ThemeIndex, self.themeGroup,
                      (self.themeButton0, self.themeButton1, self.themeButton2),
                      lambda: self.SetTheme()),
            BindRadio(Setting.Language, self.languageGroup,
                      (self.languageButton0, self.languageButton1, self.languageButton2, self.languageButton3),
                      lambda: self.SetLanguage()),
            BindRadio(Setting.LogIndex, self.logGroup,
                      (self.logutton0, self.logutton1, self.logutton2),
                      lambda: Log.UpdateLoggingLevel()),
            BindRadio(Setting.IsHttpProxy, self.proxyGroup, (self.proxy0, self.proxy1, self.proxy2, self.proxy3)),
            BindRadio(Setting.SaveNameType, self.saveNameGroup,
                      (self.saveNameButton0, self.saveNameButton1, self.saveNameButton2)),
            BindRadio(Setting.ShowCloseType, self.showCloseButtonGroup, (self.showCloseButton0, self.showCloseButton1)),
            BindCheck(Setting.IsUseScaleFactor, self.mainScaleBox),
            BindCheck(Setting.IsUpdate, self.checkBox_IsUpdate),
            # BindCheck(Setting.ChatProxy, self.chatProxy),
            BindCheck(Setting.IsOpenWaifu, self.readCheckBox),
            BindCheck(Setting.PreDownWaifu2x, self.preDownWaifu2x),
            BindCheck(Setting.CoverIsOpenWaifu, self.coverCheckBox),
            BindCheck(Setting.DownloadAuto, self.downAuto),
            BindCheck(Setting.IsOpenOpenGL, self.openglBox),
            # BindCheck(Setting.CrossChapterPrefetch, self.crossChapterPrefetch),
            BindCheck(Setting.PrefetchWholeChapter, self.prefetchWholeChapter),
            BindCheck(Setting.IsGrabGesture, self.grabGestureBox),
            BindCheck(Setting.IsOpenMemCache, self.openMemBox, lambda: self._UpdateTaskCacheSetting()),
            BindCheck(Setting.IsOpenDiskCache, self.openDiskBox, lambda: self._UpdateTaskCacheSetting()),
            BindLine(Setting.HttpProxy, self.httpEdit),
            BindLine(Setting.Sock5Proxy, self.sockEdit),
            # BindIndex(Setting.DownloadCoverLv, self.coverLvBox),
            BindIndex(Setting.Waifu2xCpuCore, self.threadSelect,
                      lambda value: self._SetIndexChoice(self.threadSelect, value, config.UseCpuNum)),
            BindIndex(Setting.TitleLine, self.titleLineBox),
            BindIndex(Setting.NotCategoryShow, self.categoryBox),
            BindIndex(Setting.FontStyle, self.fontStyle, lambda value: self.fontStyle.setCurrentIndex(int(value))),
            BindIndex(Setting.Waifu2xTileSize, self.tileComboBox),
            BindIndex(Setting.ThemeColorIndex, self.colorBox, after_save=lambda: self.SetTheme()),
            BindIndex(Setting.ProcThreadNum, self.procThreadNum),
            BindValue(Setting.SelectEncodeGpu, self.encodeSelect,
                      lambda value: self._SetTextChoice(self.encodeSelect, value, config.EncodeGpu)),
            BindValue(Setting.FontName, self.fontBox,
                      lambda value: self._SetTextChoice(self.fontBox, self._FontChoiceValue(value))),
            BindValue(Setting.FontSize, self.fontSize,
                      lambda value: self._SetTextChoice(self.fontSize, self._FontChoiceValue(value))),
            BindSpin(Setting.MultiNum, self.threadSpin),
            BindSpin(Setting.ScaleFactor, self.scaleBox),
            BindSpin(Setting.CoverSize, self.coverSize),
            BindSpin(Setting.CategorySize, self.categorySize),
            BindSpin(Setting.LookMaxNum, self.lookMaxBox),
            BindSpin(Setting.CoverMaxNum, self.coverMaxBox),
            BindSpin(Setting.PicturePrefetchCount, self.prefetchCount),
            BindSpin(Setting.PicturePrefetchFrontCount, self.prefetchFrontCount),
            BindSpin(Setting.PictureShowCount, self.showCount),
            BindSpin(Setting.PictureShowFrontCount, self.showFrontCount),
            BindSpin(Setting.MemCacheSize, self.memBox, after_save=lambda: self._UpdateTaskCacheSetting()),
            BindSpin(Setting.DiskCacheSize, self.diskBox, after_save=lambda: self._UpdateTaskCacheSetting()),
            BindSpin(Setting.DiskCacheDay, self.diskDayBox, after_save=lambda: self._UpdateTaskCacheSetting()),
            BindSpin(Setting.LookScale, self.readScale, float),
            BindSpin(Setting.CoverLookScale, self.coverScale, float),
            BindSpin(Setting.DownloadScale, self.downScale, float),
        )

    def _ConnectSettingBindings(self):
        if self._settingBindingsConnected:
            return
        for binding in self._settingBindings:
            binding.signal.connect(partial(self._SaveSettingBinding, binding))
        for setting, button in self._modelBindings:
            button.clicked.connect(partial(self._OpenModelSelection, setting, button))
        self._settingBindingsConnected = True

    def _SaveSettingBinding(self, binding, *_):
        value = binding.read()
        if value is None:
            return
        self._SaveSettingValue(binding.setting, value, binding.after_save)

    def _SaveSettingValue(self, setting, value, after_save=None):
        setting.SetValue(value)
        if after_save is not None:
            after_save()
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()

    # 登录代理页仍复用这三个入口，保留兼容并共用保存逻辑。
    def ButtonClickEvent(self, setItem, button):
        match = re.search(r"\d+", button.objectName())
        if match is None:
            self.CheckMsgLabel()
            return
        after_save = next((binding.after_save for binding in self._settingBindings
                           if binding.setting is setItem), None)
        self._SaveSettingValue(setItem, int(match.group()), after_save)

    def CheckButtonEvent(self, setItem, button):
        self._SaveSettingValue(setItem, int(button.isChecked()))

    def LineEditEvent(self, setItem, lineEdit):
        self._SaveSettingValue(setItem, lineEdit.text())

    def _OpenModelSelection(self, setting, button, *_):
        QtOwner().OpenSrSelectModel(setting.value, partial(self._SaveModelSelection, setting, button))

    def _SaveModelSelection(self, setting, button, modelName):
        setting.SetValue(modelName)
        button.setText(modelName)
        return modelName

    def SwitchCurrent(self, **kwargs):
        self.InitSetting()
        self.UpdateCacheLabe()
        return

    @staticmethod
    def _UpdateTaskCacheSetting():
        from task.task_cache import TaskCache
        TaskCache().UpdateSetting()

    def StartUpdateDiskCache(self):
        self.diskRefreshButton.setEnabled(False)
        self.diskLabel.setText(str(-1))
        from task.task_cache import TaskCache
        TaskCache().InitDiskCache()

    def UpdateCacheLabe(self):
        self.diskRefreshButton.setEnabled(True)
        from task.task_cache import TaskCache
        self.memLabel.setText(str(TaskCache().GetMemSize()))
        self.diskLabel.setText(str(TaskCache().GetDiskSize()))

    def LoadSetting(self):
        self.InitSetting()
        self.SetTheme()
        self.SetLanguage()
        # from server.server import Server
        # Server().UpdateProxy()
        # self.SetSock5Proxy()
        return

    def ExitSaveSetting(self, mainQsize):
        return

    @contextmanager
    def _BlockSettingSignals(self):
        controlTypes = (QtWidgets.QAbstractButton, QtWidgets.QButtonGroup,
                        QtWidgets.QComboBox, QtWidgets.QAbstractSpinBox,
                        QtWidgets.QLineEdit)
        with ExitStack() as stack:
            for control in self.findChildren(QObject):
                if isinstance(control, controlTypes):
                    stack.enter_context(QSignalBlocker(control))
            yield

    @staticmethod
    def _FontChoiceValue(value):
        if value in ("", "默认", "默認", "Default"):
            return ""
        return str(value)

    @staticmethod
    def _SetTextChoice(comboBox, value, fallback=""):
        index = comboBox.findData(value)
        if index < 0:
            index = comboBox.findData(fallback)
        if index >= 0:
            comboBox.setCurrentIndex(index)

    @staticmethod
    def _SetIndexChoice(comboBox, value, fallback=0):
        index = value if 0 <= value < comboBox.count() else fallback
        if 0 <= index < comboBox.count():
            comboBox.setCurrentIndex(index)

    def InitSetting(self):
        self._LoadSettingBindings()
        self.SetDownloadLabel()
        self.CheckMsgLabel(notify=False)

    def _LoadSettingBindings(self, controls=None):
        # 回填展示待生效值，不能通过控件信号覆盖用户已经保存的设置。
        with self._BlockSettingSignals():
            for binding in self._settingBindings:
                if controls is None or binding.control in controls:
                    binding.write(binding.setting.setV)
            for setting, button in self._modelBindings:
                if controls is None or button in controls:
                    button.setText(setting.setV)

    def retranslateUi(self, SettingNew):
        with self._BlockSettingSignals():
            Ui_SettingNew.retranslateUi(self, SettingNew)
        if self._settingControlsReady:
            self.InitSetting()
        else:
            self.SetDownloadLabel()

    # def SetSock5Proxy(self):
    #     try:
    #         import socket
    #         if not QtOwner().backSock:
    #             QtOwner().backSock = socket.socket
    #         if Setting.IsHttpProxy.value == 2 and Setting.Sock5Proxy.value:
    #             data = Setting.Sock5Proxy.value.replace("http://", "").replace("https://", "").replace("sock5://", "").replace("socks5://", "")
    #             data = data.split(":")
    #             if len(data) == 2:
    #                 host = data[0]
    #                 port = data[1]
    #                 socks.set_default_proxy(socks.SOCKS5, host, int(port))
    #                 socket.socket = socks.socksocket
    #             else:
    #                 QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))
    #         else:
    #             socks.set_default_proxy()
    #             socket.socket = QtOwner().backSock
    #     except Exception as es:
    #         Log.Error(es)
    #         QtOwner().ShowMsg(Str.GetStr(Str.Sock5Error))

    def SetLanguage(self):
        language = Setting.Language.value

        # Auto
        if language == 0:
            locale = QLocale.system().name()
            Log.Info("Init translate {}".format(locale))
            if locale[:3].lower() == "zh_":
                if locale.lower() == "zh_cn":
                    language = 1
                else:
                    language = 2
            else:
                # TODO
                language = 3
                # language = 2

        if language == Setting.Language.autoValue:
            return

        Setting.Language.autoValue = language

        if language == 1:
            QtOwner().app.removeTranslator(self.translate)
        elif language == 2:
            self.translate.load(":/file/tr/tr_hk.qm")
            QtOwner().app.installTranslator(self.translate)
        else:
            self.translate.load(":/file/tr/tr_en.qm")
            QtOwner().app.installTranslator(self.translate)
        Str.Reload()
        QtOwner().owner.RetranslateUi()

    def SetTheme(self):
        themeId = Setting.ThemeIndex.value
        if themeId == 0:
            themeId = self.GetSysColor()

        colorId = Setting.ThemeColorIndex.value
        if self._appliedTheme == (themeId, colorId):
            return

        self._appliedTheme = (themeId, colorId)
        Setting.ThemeIndex.autoValue = themeId

        if themeId == 1:
            if colorId == 0:
                f = QFile(":/file/theme/dark_orange.qss")
            else:
                f = QFile(":/file/theme/dark_pink.qss")
        else:
            if colorId == 0:
                f = QFile(":/file/theme/light_orange.qss")
            else:
                f = QFile(":/file/theme/light_pink.qss")
        f.open(QFile.ReadOnly)
        data = str(f.readAll(), encoding='utf-8')
        f.close()
        if Setting.FontName.value:
            data = data.replace("/*replace*/", "font-family: {};".format(Setting.FontName.value))
        QtOwner().app.setStyleSheet(data)
        self.SetSettingTheme(themeId)
        QtOwner().navigationWidget.RefrshTheme()
        QtOwner().localReadView.RefreshTheme()
        QtOwner().bookInfoView.RefreshTheme()
        QtOwner().bookInfoView2.RefreshTheme()
        if hasattr(QtOwner().owner, "RefreshTheme"):
            QtOwner().owner.RefreshTheme()

    def SetSettingTheme(self, themId):
        self.scrollArea.setStyleSheet("")

    def GetSysColor(self):
        # TODO KDE如何获取系统颜色
        if sys.platform == "win32":
            return self.GetWinSysColor() + 1
        elif sys.platform == "darwin":
            return self.GetMacOsSysColor()
        return 1

    def GetWinSysColor(self):
        try:
            path = "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            key = "AppsUseLightTheme"
            settings = QSettings(path, QSettings.NativeFormat)
            value = settings.value(key, 0)
            return value
        except Exception as es:
            Log.Error(es)
        return 1

    def GetMacOsSysColor(self):
        try:
            import subprocess
            cmd = "defaults read -g AppleInterfaceStyle"
            results = subprocess.getoutput(cmd)
            if results == "Dark":
                return 1
            else:
                return 2
        except Exception as es:
            Log.Error(es)
        return 1

    def SaveSetting(self):
        return

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            Setting.SavePath.SetValue(url)
        self.SetDownloadLabel()

    def SelectSaveLogPath(self):
        url = QFileDialog.getExistingDirectory(self, Str.GetStr(Str.SelectFold))
        if url:
            Setting.LogDirPath.SetValue(url)
            Log.Init()

        self.SetDownloadLabel()

    def SetDownloadLabel(self):
        url = Setting.SavePath.value
        if not url:
            url = "./"
        self.downloadDir.setText(os.path.join(url, config.SavePathDir))
        self.chatDir.setText(os.path.join(Setting.GetCachePath(), config.ChatSavePath))
        self.cacheDir.setText(Setting.GetCachePath())
        self.waifu2xDir.setText(os.path.join(Setting.GetCachePath(), config.Waifu2xPath))

        self.logLabel.setText(Setting.GetLogPath())

    def OpenDir(self, label):
        QDesktopServices.openUrl(QUrl.fromLocalFile(label.text()))
        return

    def SetGpuInfos(self, gpuInfo, cpuNum):
        self.gpuInfos = gpuInfo
        config.EncodeGpu = Setting.SelectEncodeGpu.value
        if not self.gpuInfos:
            config.EncodeGpu = "CPU"
        elif not config.EncodeGpu or (config.EncodeGpu != "CPU" and config.EncodeGpu not in self.gpuInfos):
            config.EncodeGpu = self.gpuInfos[0]
        config.Encode = -1 if config.EncodeGpu == "CPU" else self.gpuInfos.index(config.EncodeGpu)
        config.UseCpuNum = Setting.Waifu2xCpuCore.value
        if config.UseCpuNum > cpuNum:
            config.UseCpuNum = cpuNum

        # 硬件变化只调整本次运行的选择，不改写用户的待生效偏好。
        with self._BlockSettingSignals():
            self.encodeSelect.clear()
            for info in self.gpuInfos:
                self.encodeSelect.addItem(info, info)
            self.encodeSelect.addItem("CPU", "CPU")

            autoText = self.threadSelect.itemText(0)
            self.threadSelect.clear()
            self.threadSelect.addItem(autoText)
            for i in range(cpuNum):
                self.threadSelect.addItem(str(i + 1))
            self._LoadSettingBindings((self.encodeSelect, self.threadSelect))

        Log.Warn("waifu2x GPU: " + str(self.gpuInfos) + ",select: " + str(config.EncodeGpu) + ",use cpu num: " + str(
            config.UseCpuNum))
        return

    def GetGpuName(self):
        return config.EncodeGpu
        # index = config.Encode
        # if index >= len(self.gpuInfos) or index < 0:
        #     return "GPU"
        # return self.gpuInfos[index]

    def OpenWaifu2xHelp(self):
        QDesktopServices.openUrl(QUrl(config.Waifu2xUrl))
