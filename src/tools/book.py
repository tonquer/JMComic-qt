import re

from server.server import Server
from config import config
from tools.singleton import Singleton

# 收藏
class FavoriteInfo(object):
    def __init__(self):

        self.bookList = []
        self.total = 0
        self.count = 0
        self.fold = {}


# 分类
class Category(object):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.slug = ""
        self.type = ""
        self.total = 0


# 评论
class CommentInfo(object):
    def __init__(self):
        self.id = ""
        self.uid = ""
        self.name = ""
        self.level = ""
        self.title = ""
        self.date = ""
        self.content = ""
        self.headUrl = ""
        self.like = 0
        self.linkBookId = ""   # 链接
        self.linkBookName = ""   # 链接

        self.subComments = []   # 子评论


# 一章节
class BookEps(object):
    def __init__(self):
        self.index = 0      # 索引
        self.title = ""     # 章节名
        self.epsName = ""    # 章节名
        self.epsUrl = ""    # 链接
        self.epsId = ""     # 章节Id，和bookId类似
        self.time = ""

        # self.pages = 0         # 总页数
        self.pictureUrl = {}     # 图片
        self.pictureName = {}     # 图片
        self.aid = 0
        self.scrambleId = 0

    @property
    def pages(self):
        return len(self.pictureUrl)

    def Copy(self, o):
        assert isinstance(o, BookEps)
        self.index = o.index
        self.epsName = o.epsName
        self.epsId = o.epsId
        self.pictureUrl.update(o.pictureUrl)
        self.pictureName.update(o.pictureName)
        self.aid = o.aid


class BookBaseInfo(object):
    def __init__(self):
        self.bookId = ""
        self.title = ""
        self.bookUrl = ""
        self.author = ""
        self.likes = ""
        self.views = ""
        self.authorList = []
        self.tagList = []
        self.category = []
        self.updateDate = ""
        self.coverUrl = ""
        self.tagStr = ""
        self.price = 0
        self.purchased = False

    @property
    def id(self):
        return self.bookId

    @id.setter
    def id(self, value):
        self.bookId = value

    def Copy(self, o):
        self.bookId = o.bookId
        self.title = o.title
        self.author = o.author
        self.bookUrl = o.bookUrl
        self.coverUrl = o.coverUrl
        self.tagStr = o.tagStr
        self.authorList = o.authorList
        self.tagList = o.tagList
        self.category = o.category


class BookPageInfo(object):
    def __init__(self):
        self.kv = {}
        self.createDate = ""       # 上传日期
        self.pages = 0        # 分页
        self.des = ""         # 描述
        self.commentNum = 0   #
        self.epsInfo = {}     # 章节信息

    def maxEps(self):
        if not self.epsInfo:
            return 0
        return max(self.epsInfo.keys())

    def nextEps(self, index):
        nextIndex = index + 1
        while True:
            if nextIndex >= self.maxEps():
                return nextIndex
            if nextIndex in self.epsInfo:
                return nextIndex
            nextIndex += 1

    def lastEps(self, index):
        lastEps = index - 1
        while True:
            if lastEps < 0:
                return 0
            if lastEps in self.epsInfo:
                return lastEps
            lastEps -= 1

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
        if not bookId:
            return
        return self.books.get(str(bookId))

    def UpdateBookInfoList(self, bookList):
        for info in bookList:
            assert isinstance(info, BookInfo)
            if info.baseInfo.id in self.books:
                # TODO
                continue
            self.books[info.baseInfo.id] = info

    def UpdateBookInfo(self, bookId, info):
        bookId = str(bookId)
        book = self.GetBook(bookId)
        assert isinstance(info, BookInfo)
        if not book:
            self.books[bookId] = info
            return
        book.baseInfo.Copy(info.baseInfo)
        book.pageInfo.Copy(info.pageInfo)
        return

    def UpdateBookPicture(self, bookId, epsId, aid, minAid, pictureUrl, pictureName):
        bookId = str(bookId)
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

    def UpdateBookEps(self, bookId, newEps):
        bookId = str(bookId)
        book = self.GetBook(bookId)
        assert isinstance(book, BookInfo)
        if not book:
            return
        epsInfo = book.pageInfo.epsInfo.get(newEps.index)
        if epsInfo:
            epsInfo.Copy(newEps)
            return
        book.pageInfo.epsInfo[newEps.index] = newEps

    def UpdateBookEpsScrambleId(self, bookId, epsIndex, scrambleId):
        bookId = str(bookId)
        book = self.GetBook(bookId)
        assert isinstance(book, BookInfo)
        if not book:
            return
        epsInfo = book.pageInfo.epsInfo.get(epsIndex)
        if not epsInfo:
            return
        epsInfo.scrambleId = scrambleId