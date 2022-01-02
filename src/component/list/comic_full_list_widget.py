from component.list.comic_list_widget import ComicListWidget


class ComicFullListWidget(ComicListWidget):
    def __init__(self, parent):
        ComicListWidget.__init__(self, parent)

    def wheelEvent(self, event):
        event.ignore()
