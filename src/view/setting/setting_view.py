import base64
import os
import re
import sys
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QSettings, Qt, QSize, QUrl, QFile, QTranslator, QLocale
from PySide6.QtGui import QDesktopServices, QFontDatabase
from PySide6.QtWidgets import QFileDialog, QScroller, QScrollerProperties

from config import config
from config.setting import Setting, SettingValue
from interface.ui_setting_new import Ui_SettingNew
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from view.tool.doh_dns_view import DohDnsView


class SettingView(QtWidgets.QWidget, Ui_SettingNew):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        Ui_SettingNew.__init__(self)
        self.setupUi(self)

        self.mainSize = None
        self.bookSize = None
        self.readSize = None
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        self.translate = QTranslator()
        for name in QFontDatabase.families():
            self.fontBox.addItem(name)

        # RadioButton:
        self.themeGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ThemeIndex))
        self.languageGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.Language))
        self.logGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.LogIndex))
        self.proxyGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.IsHttpProxy))
        self.saveNameGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.SaveNameType))
        self.showCloseButtonGroup.buttonClicked.connect(partial(self.ButtonClickEvent, Setting.ShowCloseType))

        # CheckButton:
        self.mainScaleBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUseScaleFactor, self.mainScaleBox))
        self.checkBox_IsUpdate.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUpdate, self.checkBox_IsUpdate))
        self.readCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenWaifu, self.readCheckBox))
        self.preDownWaifu2x.clicked.connect(partial(self.CheckButtonEvent, Setting.PreDownWaifu2x, self.preDownWaifu2x))
        self.coverCheckBox.clicked.connect(partial(self.CheckButtonEvent, Setting.CoverIsOpenWaifu, self.coverCheckBox))
        self.downAuto.clicked.connect(partial(self.CheckButtonEvent, Setting.DownloadAuto, self.downAuto))
        # self.titleBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsUseTitleBar, self.titleBox))
        self.openglBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsOpenOpenGL, self.openglBox))
        self.grabGestureBox.clicked.connect(partial(self.CheckButtonEvent, Setting.IsGrabGesture, self.grabGestureBox))

        # LineEdit:
        self.httpEdit.editingFinished.connect(partial(self.LineEditEvent, Setting.HttpProxy, self.httpEdit))
        # self.dohLine.editingFinished.connect(partial(self.LineEditEvent, Setting.DohAddress, self.dohLine))
        # Button:

        # comboBox:
        # self.encodeSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, "LookReadMode"))
        # self.readModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookModel))
        # self.readNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.LookNoise))
        # self.coverModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookModel))
        # self.coverNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.CoverLookNoise))
        # self.downModel.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadModel))
        # self.downNoise.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.DownloadNoise))

        self.readModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.LookModelName, self.readModelName))
        self.coverModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.CoverLookModelName, self.coverModelName))
        self.downModelName.clicked.connect(partial(self.CheckOpenSrSelect, Setting.DownloadModelName, self.downModelName))

        self.encodeSelect.currentTextChanged.connect(partial(self.CheckRadioEvent, Setting.SelectEncodeGpu))
        self.threadSelect.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.Waifu2xCpuCore))
        self.titleLineBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.TitleLine))
        self.categoryBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.NotCategoryShow))
        self.fontBox.currentTextChanged.connect(partial(self.CheckRadioEvent, Setting.FontName))
        self.fontSize.currentTextChanged.connect(partial(self.CheckRadioEvent, Setting.FontSize))
        self.fontStyle.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.FontStyle))
        self.tileComboBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.Waifu2xTileSize))
        self.colorBox.currentIndexChanged.connect(partial(self.CheckRadioEvent, Setting.ThemeColorIndex))

        # spinBox
        # self.preDownNum.valueChanged.connect(partial(self.SpinBoxEvent, "", self.preDownNum))
        self.scaleBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.ScaleFactor))
        self.coverSize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverSize))
        self.categorySize.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CategorySize))
        self.readScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookScale))
        self.coverScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverLookScale))
        self.downScale.valueChanged.connect(partial(self.SpinBoxEvent, Setting.DownloadScale))
        self.lookMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.LookMaxNum))
        self.coverMaxBox.valueChanged.connect(partial(self.SpinBoxEvent, Setting.CoverMaxNum))
        self.threadSpin.valueChanged.connect(partial(self.SpinBoxEvent, Setting.MultiNum))

        self.generalButton.clicked.connect(partial(self.MoveToLabel, self.generalLabel))
        # self.readButton.clicked.connect(partial(self.MoveToLabel, self.readLabel))
        self.proxyButton.clicked.connect(partial(self.MoveToLabel, self.proxyLabel))
        self.waifu2xButton.clicked.connect(partial(self.MoveToLabel, self.waifu2xLabel))
        self.downloadButton.clicked.connect(partial(self.MoveToLabel, self.downloadLabel))

        self.setDirButton.clicked.connect(self.SelectSavePath)
        self.openDownloadDir.clicked.connect(partial(self.OpenDir, self.downloadDir))
        self.openCacheDir.clicked.connect(partial(self.OpenDir, self.cacheDir))
        self.openWaifu2xDir.clicked.connect(partial(self.OpenDir, self.waifu2xDir))

        self.openProxy.clicked.connect(self.OpenProxy)

        self.languageButton3.setVisible(True)
        self.categorySize.setVisible(False)

        self.msgLabel.setVisible(False)

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.ScrollerGestureType.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.VerticalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.ScrollMetric.HorizontalOvershootPolicy, QScrollerProperties.OvershootPolicy.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)

        # self.dohButton.clicked.connect(self.OpenDohView)

        self.InitBackupSection()

    def InitBackupSection(self):
        """在设置页末尾追加「配置备份」区块

        这里用代码追加而不是改 .ui 文件，避免与上游的界面改动冲突。
        """
        frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        frame.setObjectName("backupFrame")
        hLayout = QtWidgets.QHBoxLayout(frame)
        hLayout.setContentsMargins(0, 0, 0, 0)

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
                            zf.write(snapPath, name)
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
        try:
            fd, snapPath = tempfile.mkstemp(suffix=".db")
            os.close(fd)
            src = sqlite3.connect(srcPath)
            dst = sqlite3.connect(snapPath)
            src.backup(dst)
            return snapPath
        except Exception as es:
            Log.Warn("sqlite snapshot failed, fallback to raw copy, {}: {}".format(srcPath, es))
            if snapPath and os.path.isfile(snapPath):
                os.remove(snapPath)
            return None
        finally:
            for con in (dst, src):
                if con is not None:
                    try:
                        con.close()
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
        fileMap = self.GetBackupFileMap()
        backups = {}
        try:
            for name, tmpPath in extracted.items():
                destPath = fileMap[name]
                os.makedirs(os.path.dirname(destPath), exist_ok=True)
                if os.path.isfile(destPath):
                    with open(destPath, "rb") as f:
                        backups[destPath] = f.read()
                shutil.copyfile(tmpPath, destPath)
        except Exception:
            for destPath, data in backups.items():
                try:
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

    def MoveToLabel(self, label):
        p = label.pos()
        self.scrollArea.vScrollBar.ScrollTo(p.y())
        return

    def CheckMsgLabel(self):
        isNeed = False
        for name in dir(Setting):
            setItem = getattr(Setting, name)
            if isinstance(setItem, SettingValue):
                if setItem.isNeedReset:
                    if setItem.value != setItem.setV:
                        isNeed = True
        if isNeed:
            self.msgLabel.setVisible(True)
            QtOwner().ShowErrOne(Str.GetStr(Str.NeedResetSave))
        else:
            self.msgLabel.setVisible(False)
        return

    def ButtonClickEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        mo = re.search(r"\d+", button.objectName())
        if mo:
            value = int(mo.group())
            setItem.SetValue(value)
            if setItem == Setting.ThemeIndex:
                self.SetTheme()
            elif setItem == Setting.LogIndex:
                Log.UpdateLoggingLevel()
            elif setItem == Setting.Language:
                self.SetLanguage()
            elif setItem == Setting.IsHttpProxy:
                pass
                # from server.server import Server
                # Server().UpdateProxy()
            QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def CheckOpenSrSelect(self, setItem, button):
        if button == self.coverModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectCoverBack)
        elif button == self.readModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectReadBack)
        elif button == self.downModelName:
            QtOwner().OpenSrSelectModel(setItem.value, self.CheckOpenSrSelectDownBack)
        pass

    def CheckOpenSrSelectCoverBack(self, modelName):
        Setting.CoverLookModelName.SetValue(modelName)
        self.coverModelName.setText(modelName)
        return modelName

    def CheckOpenSrSelectReadBack(self, modelName):
        Setting.LookModelName.SetValue(modelName)
        self.readModelName.setText(modelName)
        return modelName

    def CheckOpenSrSelectDownBack(self, modelName):
        Setting.DownloadModelName.SetValue(modelName)
        self.downModelName.setText(modelName)
        return modelName

    def CheckRadioEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        if setItem == Setting.IsHttpProxy:
            pass
            # from server.server import Server
            # Server().UpdateProxy()
        elif setItem == Setting.ThemeColorIndex:
            self.SetTheme()
        self.CheckMsgLabel()
        return

    def LineEditEvent(self, setItem, lineEdit):
        assert isinstance(setItem, SettingValue)
        value = lineEdit.text()
        setItem.SetValue(value)
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        # from server.server import Server
        # Server().UpdateProxy()
        return

    def SpinBoxEvent(self, setItem, value):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(value))
        QtOwner().ShowMsgOne(Str.GetStr(Str.SaveSuc))
        self.CheckMsgLabel()
        return

    def OpenDohView(self):
        view = DohDnsView(QtOwner().owner)
        view.show()

    def SwitchCurrent(self, **kwargs):
        self.update()
        refresh = kwargs.get("refresh")
        if refresh:
            self.InitSetting()
        return

    def LoadSetting(self):
        self.InitSetting()
        self.SetTheme()
        self.SetLanguage()
        # from server.server import Server
        # Server().UpdateProxy()
        return

    def ExitSaveSetting(self, mainQsize):
        return

    def InitSetting(self):
        self.checkBox_IsUpdate.setChecked(Setting.IsUpdate.value)
        self.mainScaleBox.setChecked(Setting.IsUseScaleFactor.value)
        self.SetRadioGroup("themeButton", Setting.ThemeIndex.value)
        self.SetRadioGroup("languageButton", Setting.Language.value)
        # self.SetRadioGroup("mainScaleButton", Setting.ScaleLevel.value)
        self.SetRadioGroup("proxy", Setting.IsHttpProxy.value)
        self.SetRadioGroup("saveNameButton", Setting.SaveNameType.value)
        self.SetRadioGroup("showCloseButton", Setting.ShowCloseType.value)
        self.coverSize.setValue(Setting.CoverSize.value)
        self.categorySize.setValue(Setting.CategorySize.value)
        self.SetRadioGroup("logutton", Setting.LogIndex.value)
        self.httpEdit.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)
        # self.titleBox.setChecked(Setting.IsUseTitleBar.value)
        self.openglBox.setChecked(Setting.IsOpenOpenGL.value)
        self.grabGestureBox.setChecked(Setting.IsGrabGesture.value)
        for index in range(self.encodeSelect.count()):
            if Setting.SelectEncodeGpu.value == self.encodeSelect.itemText(index):
                self.encodeSelect.setCurrentIndex(index)

        for index in range(self.fontSize.count()):
            if str(Setting.FontSize.value) == self.fontSize.itemText(index):
                self.fontSize.setCurrentIndex(index)

        self.fontStyle.setCurrentIndex(int(Setting.FontStyle.value))

        for index in range(self.fontBox.count()):
            if str(Setting.FontName.value) == self.fontBox.itemText(index):
                self.fontBox.setCurrentIndex(index)

        self.readCheckBox.setChecked(Setting.IsOpenWaifu.value)
        self.preDownWaifu2x.setChecked(Setting.PreDownWaifu2x.value)
        # self.readNoise.setCurrentIndex(Setting.LookNoise.value)
        self.readScale.setValue(Setting.LookScale.value)
        self.scaleBox.setValue(Setting.ScaleFactor.value)
        # self.readModel.setCurrentIndex(Setting.LookModel.value)

        self.categoryBox.setCurrentIndex(Setting.NotCategoryShow.value)
        self.titleLineBox.setCurrentIndex(Setting.TitleLine.value)
        self.tileComboBox.setCurrentIndex(Setting.Waifu2xTileSize.value)
        self.coverCheckBox.setChecked(Setting.CoverIsOpenWaifu.value)
        # self.coverNoise.setCurrentIndex(Setting.CoverLookNoise.value)
        self.coverScale.setValue(Setting.CoverLookScale.value)
        # self.coverModel.setCurrentIndex(Setting.CoverLookModel.value)
        self.colorBox.setCurrentIndex(Setting.ThemeColorIndex.value)

        self.downAuto.setChecked(Setting.DownloadAuto.value)
        # self.downNoise.setCurrentIndex(Setting.DownloadNoise.value)
        self.downScale.setValue(Setting.DownloadScale.value)
        self.threadSpin.setValue(Setting.MultiNum.value)
        # self.downModel.setCurrentIndex(Setting.DownloadModel.value)
        self.coverModelName.setText(Setting.CoverLookModelName.value)
        self.readModelName.setText(Setting.LookModelName.value)
        self.downModelName.setText(Setting.DownloadModelName.value)

        self.SetDownloadLabel()

    def OpenProxy(self):
        QtOwner().OpenLogin()
        # loginView = LoginView(QtOwner().owner, False)
        # loginView.tabWidget.setCurrentIndex(0)
        # loginView.tabWidget.removeTab(0)
        # loginView.tabWidget.removeTab(0)
        # loginView.tabWidget.removeTab(0)
        # loginView.loginButton.setText(Str.GetStr(Str.Save))
        # loginView.show()
        #
        # loginView.closed.connect(QtOwner().owner.navigationWidget.UpdateProxyName)
        return

    def retranslateUi(self, SettingNew):
        Ui_SettingNew.retranslateUi(self, SettingNew)
        self.SetDownloadLabel()
        self.coverModelName.setText(Setting.CoverLookModelName.value)
        self.readModelName.setText(Setting.LookModelName.value)
        self.downModelName.setText(Setting.DownloadModelName.value)

    def SetRadioGroup(self, text, index):
        radio = getattr(self, text+str(index))
        if radio:
            radio.setChecked(True)

    # def SetSock5Proxy(self):
    #     try:
    #         import socket
    #         import socks
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
                language = 3

        if language == Setting.Language.autoValue:
            return

        Setting.Language.autoValue = language

        if language == 1:
            QtOwner().app.removeTranslator(self.translate)
        elif language == 2:
            success = self.translate.load(":/file/tr/tr_hk.qm")
            if success:
                QtOwner().app.installTranslator(self.translate)
            else:
                Log.Error("Failed to load hk translation.")
        else:
            success = self.translate.load(":/file/tr/tr_en.qm")
            if success:
                QtOwner().app.installTranslator(self.translate)
            else:
                Log.Error("Failed to load en translation.")
        Str.Reload()
        QtOwner().owner.RetranslateUi()

    def SetTheme(self):
        themeId = Setting.ThemeIndex.value
        if themeId == 0:
            themeId = self.GetSysColor()

        # if themeId == Setting.ThemeIndex.autoValue:
        #     return

        Setting.ThemeIndex.autoValue = themeId

        if themeId == 1:
            if Setting.ThemeColorIndex.value == 0:
                f = QFile(":/file/theme/dark_orange.qss")
            else:
                f = QFile(":/file/theme/dark_pink.qss")
        else:
            if Setting.ThemeColorIndex.value == 0:
                f = QFile(":/file/theme/light_orange.qss")
            else:
                f = QFile(":/file/theme/light_pink.qss")
        f.open(QFile.ReadOnly)
        data = str(f.readAll(), encoding='utf-8')
        if Setting.FontName.value:
            data = data.replace("/*replace*/", "font-family: {};".format(Setting.FontName.value))
        QtOwner().app.setStyleSheet(data)
        f.close()
        QtOwner().localReadView.retranslateUi(QtOwner().localReadView)
        QtOwner().bookInfoView.retranslateUi(QtOwner().bookInfoView)
        self.SetSettingTheme(themeId)

    def SetSettingTheme(self, themId):
        if themId != 1:
            qss = """
                .QFrame
                {
                    background-color: rgb(253, 253, 253);
                    
                    border:2px solid rgb(234,234,234);
                    border-radius:5px
                }        
                """
        else:
            qss = """
                .QFrame
                {
                    background-color: rgb(50, 50, 50);

                    border:2px solid rgb(35,35,35);
                    border-radius:5px
                }        
                """
        self.scrollArea.setStyleSheet(qss)

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

    def SetDownloadLabel(self):
        url = Setting.SavePath.value
        if not url:
            url = "./"
        self.downloadDir.setText(os.path.join(url, config.SavePathDir))
        self.cacheDir.setText(Setting.GetCachePath())
        self.waifu2xDir.setText(os.path.join(Setting.GetCachePath(), config.Waifu2xPath))

    def OpenDir(self, label):
        QDesktopServices.openUrl(QUrl.fromLocalFile(label.text()))
        return

    def SetGpuInfos(self, gpuInfo, cpuNum):
        self.gpuInfos = gpuInfo
        config.EncodeGpu = Setting.SelectEncodeGpu.value

        if not self.gpuInfos:
            config.EncodeGpu = "CPU"
            config.Encode = -1
            self.encodeSelect.addItem(config.EncodeGpu)
            self.encodeSelect.setCurrentIndex(0)

        if not config.EncodeGpu or (
                self.gpuInfos and config.EncodeGpu != "CPU" and config.EncodeGpu not in self.gpuInfos):
            config.EncodeGpu = self.gpuInfos[0]
            config.Encode = 0

        index = 0
        if self.gpuInfos:
            for info in self.gpuInfos:
                self.encodeSelect.addItem(info)
                if info == config.EncodeGpu:
                    self.encodeSelect.setCurrentIndex(index)
                    config.Encode = index
                index += 1

            self.encodeSelect.addItem("CPU")

        if config.EncodeGpu == "CPU":
            config.Encode = -1
            self.encodeSelect.setCurrentIndex(index)

        config.UseCpuNum = Setting.Waifu2xCpuCore.value
        if config.UseCpuNum > cpuNum:
            config.UseCpuNum = cpuNum
        for i in range(cpuNum):
            self.threadSelect.addItem(str(i + 1))
        self.threadSelect.setCurrentIndex(config.UseCpuNum)

        Log.Warn("waifu2x GPU: " + str(self.gpuInfos) + ",select: " + str(config.EncodeGpu) + ",use cpu num: " + str(
            config.UseCpuNum))
        return

    def GetGpuName(self):
        return config.EncodeGpu
        # index = config.Encode
        # if index >= len(self.gpuInfos) or index < 0:
        #     return "GPU"
        # return self.gpuInfos[index]