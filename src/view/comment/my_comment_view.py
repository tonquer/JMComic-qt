from component.widget.comment_widget import CommentWidget
from qt_owner import QtOwner
from server import req, config
from tools.str import Str


class MyCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.setWindowTitle(Str.GetStr(Str.MyComment))
        self.pushButton.hide()
        self.commentLine.hide()

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if not refresh:
            return
        if not config.LoginUserName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return

        self.bookId = QtOwner().user.uid
        self.ClearCommentList()
        self.listWidget.UpdatePage(1, 1)
        self.LoadComment()

    def retranslateUi(self, Comment):
        CommentWidget.retranslateUi(self, Comment)
        self.setWindowTitle(Str.GetStr(Str.MyComment))

    def LoadComment(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetMyCommentReq2(self.bookId, self.listWidget.page), self.GetCommentBack, self.listWidget.page)
        return

    def LoadNextPage(self):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetMyCommentReq2(self.bookId, self.listWidget.page + 1), self.GetCommentBack, self.listWidget.page+1)
        return