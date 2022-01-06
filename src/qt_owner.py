import weakref

from PySide6.QtCore import QFile

from component.label.msg_label import MsgLabel
from tools.singleton import Singleton
from tools.str import Str


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None
        self._app = None
        self.isUseDb = True
        from tools.user import User
        self.user = User()

    def SetLogin(self):
        self.user.isLogin = True

    def SetUser(self, user):
        self.user = user

    def CheckShowMsg(self, raw):
        msg = raw.get("st")
        errorMsg = raw.get("errorMsg")
        if errorMsg:
            return self.ShowError(errorMsg)
        message = raw.get("message")
        if message:
            return self.ShowMsg(message)
        elif isinstance(msg, int):
            return self.ShowError(Str.GetStr(msg))
        else:
            return self.ShowError(msg)

    def ShowError(self, msg):
        return MsgLabel.ShowErrorEx(self.owner, msg)

    def ShowMsg(self, msg):
        return MsgLabel.ShowMsgEx(self.owner, msg)

    def ShowMsgOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowMsg(msg)

    def ShowErrOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowError(msg)

    def ShowLoading(self):
        self.owner.loadingDialog.Show()
        return

    def CloseLoading(self):
        self.owner.loadingDialog.close()
        return

    @property
    def owner(self):
        from view.main.main_view import MainView
        assert isinstance(self._owner(), MainView)
        return self._owner()

    @property
    def app(self):
        return self._app()

    @property
    def downloadView(self):
        return self.owner.downloadView

    @property
    def loginWebView(self):
        return self.owner.loginWebView

    @property
    def historyView(self):
        return self.owner.historyView

    @property
    def gameInfoView(self):
        return self.owner.gameInfoView

    @property
    def bookInfoView(self):
        return self.owner.bookInfoView

    @property
    def favoriteView(self):
        return self.owner.favorityView

    @property
    def indexView(self):
        return self.owner.indexView

    @property
    def settingView(self):
        return self.owner.settingView

    @property
    def searchView(self):
        return self.owner.searchView

    def SetSubTitle(self, text):
        return self.owner.setSubTitle(text)

    def GetFileData(self, fileName):
        f = QFile(fileName)
        f.open(QFile.ReadOnly)
        data = f.readAll()
        f.close()
        return bytes(data)

    def OpenFavoriteFold(self, bookId="", fid="", moveBack=None, foldChangeBack=None):
        from view.user.favorite_fold_view import FavoriteFoldView
        w = FavoriteFoldView(QtOwner().owner, bookId, fid)
        w.show()
        if moveBack:
            w.MoveOkBack.connect(moveBack)
        if foldChangeBack:
            w.FoldChange.connect(foldChangeBack)

    def OpenComment(self, bookId, commentNum):
        arg = {"bookId": bookId, "commentNum": commentNum}
        self.owner.SwitchWidget(self.owner.commentView, **arg)

    def OpenGameComment(self, commentId):
        arg = {"bookId": commentId}
        self.owner.SwitchWidget(self.owner.gameCommentView, **arg)

    def OpenRank(self):
        arg = {"refresh": True}
        self.owner.SwitchWidget(self.owner.rankView, **arg)

    def OpenIndex(self):
        arg = {"refresh": True}
        self.owner.SwitchWidget(self.owner.indexView, **arg)

    def OpenSubComment(self, commentId, widget, commentList):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": commentId, "commentList": commentList}
        self.owner.subCommentView.SetWidget(widget)
        self.owner.SwitchWidget(self.owner.subCommentView, **arg)

    def OpenSearch(self, text):
        arg = {"text": text}
        if text.isdigit() and len(text) == 6:
            return self.OpenBookInfo(int(text))
        self.owner.SwitchWidget(self.owner.searchView, **arg)

    def OpenSearchByText(self, text):
        self.owner.searchView.lineEdit.setText(text)
        self.owner.searchView.lineEdit.Search()

    def OpenReadView(self, bookId, index, name, pageIndex):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenPage(bookId, index, name, pageIndex=pageIndex)

    def CloseReadView(self):
        self.owner.totalStackWidget.setCurrentIndex(0)

    def OpenSearchByCategory(self, categories):
        arg = {"categories": categories}
        self.owner.SwitchWidget(self.owner.searchView, **arg)

    def OpenBookInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.bookInfoView, **arg)

    def OpenEpsInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.bookEpsView, **arg)

    def OpenGameInfo(self, bookId):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId}
        self.owner.SwitchWidget(self.owner.gameInfoView, **arg)

    def OpenWaifu2xTool(self, data):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"data": data}
        self.owner.SwitchWidget(self.owner.waifu2xToolView, **arg)

    def SwitchWidgetLast(self):
        self.owner.SwitchWidgetLast()
        return

    def SwitchWidgetNext(self):
        self.owner.SwitchWidgetNext()
        return

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    def SetApp(self, app):
        self._app = weakref.ref(app)

    def SetDirty(self):
        pass
    
    # def ShowMsg(self, data):
    #     return self.owner.msgForm.ShowMsg(data)
    #
    # def ShowError(self, data):
    #     return self.owner.msgForm.ShowError(data)

    # def ShowMsgBox(self, type, title, msg):
    #     msg = QMessageBox(type, title, msg)
    #     msg.addButton("Yes", QMessageBox.AcceptRole)
    #     if type == QMessageBox.Question:
    #         msg.addButton("No", QMessageBox.RejectRole)
    #     if config.ThemeText == "flatblack":
    #         msg.setStyleSheet("QWidget{background-color:#2E2F30}")
    #     return msg.exec_()