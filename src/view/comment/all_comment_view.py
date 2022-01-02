from component.widget.comment_widget import CommentWidget
from tools.str import Str


class AllCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.setWindowTitle(Str.GetStr(Str.AllComment))

    def retranslateUi(self, Comment):
        self.setWindowTitle(Str.GetStr(Str.AllComment))
        CommentWidget.retranslateUi(self, Comment)