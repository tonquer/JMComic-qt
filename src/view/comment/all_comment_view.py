from component.widget.comment_widget import CommentWidget
from tools.str import Str


class AllCommentView(CommentWidget):
    def __init__(self, parent=None):
        CommentWidget.__init__(self, parent)
        self.setWindowTitle(Str.GetStr(Str.AllComment))
        self.selectWidget.show()
        self.selectBox.currentIndexChanged.connect(self.SwitchBox)

    def retranslateUi(self, Comment):
        CommentWidget.retranslateUi(self, Comment)
        self.setWindowTitle(Str.GetStr(Str.AllComment))

    def SwitchBox(self, index):
        self.readIndex = index
        self.ClearCommentList()
        self.listWidget.UpdatePage(1, 1)
        self.LoadComment()