import re

from server.server import Server
from config import config
from tools.singleton import Singleton

# 一章节
class BookEps(object):
    def __init__(self):
        self.index = 0     # 索引
        self.title = ""    # 章节名
        self.epsName = ""    # 章节名
        self.epsUrl = ""   # 链接
        self.time = ""

        # self.pages = 0         # 总页数
        self.pictureUrl = {}     # 图片
        self.pictureName = {}     # 图片
        self.aid = ""
        self.minAid = ""

    @property
    def pages(self):
        return len(self.pictureUrl)


class BookBaseInfo(object):
    def __init__(self):
        self.bookId = ""
        self.title = ""
        self.bookUrl = ""
        self.author = ""
        self.authorList = []
        self.tagList = []
        self.updateDate = ""
        self.coverUrl = ""
        self.tagStr = ""

    @property
    def id(self):
        return self.bookId

    def Copy(self, o):
        self.bookId = o.bookId
        self.title = o.title
        self.author = o.author
        self.bookUrl = o.bookUrl
        self.coverUrl = o.coverUrl
        self.tagStr = o.tagStr
        self.authorList = o.authorList
        self.tagList = o.tagList


class BookPageInfo(object):
    def __init__(self):
        self.kv = {}
        self.createDate = ""       # 上传日期
        self.pages = 0        # 分页
        self.des = ""         # 描述
        self.epsInfo = {}     # 章节信息

    def Copy(self, o):
        self.kv.update(o.kv)
        self.createDate = o.createDate
        self.pages = o.pages
        self.des = o.des
        self.epsInfo.update(o.epsInfo)

class BookInfo(object):
    def __init__(self):
        self.baseInfo = BookBaseInfo()
        self.pageInfo = BookPageInfo()


# 书的管理器
class BookMgr(Singleton):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.books = {}

    @property
    def server(self):
        return Server()

    def GetBook(self, bookId) -> BookInfo:
        return self.books.get(bookId)

    def UpdateBookInfoList(self, bookList):
        for info in bookList:
            assert isinstance(info, BookInfo)
            if info.baseInfo.id in self.books:
                # TODO
                continue
            self.books[info.baseInfo.id] = info

    def UpdateBookInfo(self, bookId, info):
        book = self.GetBook(bookId)
        assert isinstance(info, BookInfo)
        if not book:
            self.books[bookId] = info
            return
        book.baseInfo.Copy(info.baseInfo)
        book.pageInfo.Copy(info.pageInfo)
        return

    def UpdateBookPicture(self, bookId, epsId, aid, minAid, pictureUrl, pictureName):
        book = self.GetBook(bookId)
        assert isinstance(book, BookInfo)
        if not book:
            return
        epsInfo = book.pageInfo.epsInfo.get(epsId)
        if not epsInfo:
            return
        epsInfo.aid = aid
        epsInfo.minAid = minAid
        epsInfo.pictureUrl.update(pictureUrl)
        epsInfo.pictureName.update(pictureName)
        return
