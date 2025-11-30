from PySide6 import QtWidgets

from component.widget.comment_widget import CommentWidget
from interface.ui_sub_comment import Ui_SubComment
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.log import Log
from tools.status import Status


class SubCommentView(QtWidgets.QWidget, Ui_SubComment, QtTaskBase):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_SubComment.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.commentList.SendCommentBack = self.SendCommentBack

    def SwitchCurrent(self, **kwargs):
        self.update()
        bookId = kwargs.get("bookId")
        if not bookId:
            return
        commentList = kwargs.get("commentList")
        self.bookId = bookId
        self.commentList.ClearCommentList()
        for index, info in enumerate(commentList):
            self.commentList.listWidget.AddUserItem(info, "")

        pass

    def SetWidget(self, widget):
        self.commentList.cid = widget.id
        self.commentList.skipButton.hide()
        self.comment.commentButton.hide()
        self.comment.indexLabel.setText(widget.indexLabel.text())
        self.comment.dateLabel.setText(widget.dateLabel.text())
        self.comment.titleLabel.setText(widget.titleLabel.text())
        self.comment.nameLabel.setText(widget.nameLabel.text())
        self.comment.picIcon.setPixmap(widget.picIcon.pixmap())
        self.comment.commentLabel.setText(widget.commentLabel.text())
        self.comment.levelLabel.setText(widget.levelLabel.text())

    def SendCommentBack(self, raw):
        try:
            QtOwner().CloseLoading()
            st = raw["st"]
            if st == Status.Ok:
                self.commentList.commentLine.setText("")
                QtOwner().CheckShowMsg( raw)
            else:
                QtOwner().CheckShowMsg( raw)

        except Exception as es:
            QtOwner().CloseLoading()
            Log.Error(es)