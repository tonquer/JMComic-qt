import re

from server.server import Server
from config import config
from tools.log import Log
from tools.singleton import Singleton


# 推荐
class RelatedInfo(object):
    def __init__(self):
        self.id = ""
        self.author = ""
        self.name = ""
        self.image = ""
        self.coverUrl = ""

# 首页
class IndexInfo(object):
    def __init__(self):
        self.bookList = []
        self.type = ""
        self.id = ""
        self.title = ""
        self.filter_val = ""
        self.slug = ""

# 收藏
class FavoriteInfo(object):
    def __init__(self):

        self.bookList = []
        self.total = 0
        self.count = 0
        self.fold = {}


# 分类
class Category(object):
    def __init__(self, name=""):
        self.id = ""
        self.name = name
        self.slug = ""
        self.type = ""
        self.total = 0
        self.sub_categories = []


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
        self.sort = 0
        self.time = ""

        # self.pages = 0         # 总页数
        self.pictureUrl = {}     # 图片
        self.pictureName = {}     # 图片
        self.allIndex = []
        self.series_id = 0
        self.scrambleId = 0

    @property
    def pages(self):
        return len(self.pictureUrl)

    def GetRealIndex(self, index):
        if index >= len(self.allIndex):
            return index
        return self.allIndex[index]

    def Copy(self, o):
        assert isinstance(o, BookEps)
        if o.index >= 0:
            self.index = o.index
        if o.title:
            self.title = o.title
        if o.epsName:
            self.epsName = o.epsName
        if o.epsUrl:
            self.epsUrl = o.epsUrl
        if o.epsId:
            self.epsId = o.epsId
        if o.sort:
            self.sort = o.sort
        if o.time:
            self.time = o.time
        self.pictureUrl.update(o.pictureUrl)
        self.pictureName.update(o.pictureName)
        self.allIndex = sorted(self.pictureUrl.keys())
        if o.series_id:
            self.series_id = o.series_id
        if o.scrambleId:
            self.scrambleId = o.scrambleId


class BookBaseInfo(object):
    def __init__(self):
        self.bookId = ""
        self.series_id = ""
        self.title = ""
        self.bookUrl = ""
        self.author = ""
        self.likes = ""
        self.views = ""
        self.authorList = []
        self.tagList = []
        self.workList = []
        self.actorList = []
        self.category = []
        self.updateDate = ""
        self.coverUrl = ""
        self.addTime = 0
        # self.tagStr = ""
        self.price = 0
        self.purchased = False

    @property
    def id(self):
        return self.bookId

    @id.setter
    def id(self, value):
        self.bookId = value

    def Copy(self, o):
        if o.bookId:
            self.bookId = o.bookId
        if o.series_id:
            self.series_id = o.series_id
        if o.title:
            self.title = o.title
        if o.author:
            self.author = o.author
        if o.bookUrl:
            self.bookUrl = o.bookUrl
        if o.coverUrl:
            self.coverUrl = o.coverUrl
        if o.likes:
            self.likes = o.likes
        if o.views:
            self.views = o.views
        # self.tagStr = o.tagStr
        if o.authorList:
            self.authorList = o.authorList
        if o.tagList:
            self.tagList = o.tagList
        if o.workList:
            self.workList = o.workList
        if o.actorList:
            self.actorList = o.actorList
        if o.category:
            self.category = o.category
        if o.updateDate:
            self.updateDate = o.updateDate
        if o.addTime:
            self.addTime = o.addTime
        if o.price:
            self.price = o.price
        if o.purchased:
            self.purchased = o.purchased


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
        if o.createDate:
            self.createDate = o.createDate
        if o.pages:
            self.pages = o.pages
        if o.des:
            self.des = o.des
        if o.commentNum:
            self.commentNum = o.commentNum
        for epsId, eps in o.epsInfo.items():
            if epsId in self.epsInfo:
                self.epsInfo[epsId].Copy(eps)
            else:
                self.epsInfo[epsId] = eps


class BookInfo(object):
    def __init__(self):
        self.pageInfo = BookPageInfo()
        self.baseInfo = BookBaseInfo()
        self.related_list = []   # [{id, name, author, image}]
        self.localMaxEps = 0

    @property
    def categories(self):
        return self.baseInfo.tagList

    @property
    def id(self):
        return self.baseInfo.id

    @property
    def epsCount(self):
        return len(self.pageInfo.epsInfo)

    @property
    def title(self):
        return self.baseInfo.title


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
        if not book:
            return
        assert isinstance(book, BookInfo)
        epsInfo = book.pageInfo.epsInfo.get(epsId)
        if not epsInfo:
            return
        assert isinstance(epsInfo, BookEps)
        epsInfo.series_id = aid
        epsInfo.minAid = minAid
        epsInfo.pictureUrl.update(pictureUrl)
        epsInfo.pictureName.update(pictureName)
        epsInfo.allIndex = sorted(epsInfo.pictureUrl.keys())
        return

    def UpdateBookEps(self, bookId, newEps):
        bookId = str(bookId)
        book = self.GetBook(bookId)
        if not book:
            return
        assert isinstance(book, BookInfo)
        epsInfo = None
        if newEps.index >= 0 :
            epsInfo = book.pageInfo.epsInfo.get(newEps.index)
        else:
            for v in book.pageInfo.epsInfo.values():
                if v.epsId == newEps.epsId:
                    epsInfo = v
                    break
        if epsInfo:
            epsInfo.Copy(newEps)
            return
        book.pageInfo.epsInfo[newEps.index] = newEps

    def UpdateBookEpsScrambleId(self, bookId, epsIndex, scrambleId):
        bookId = str(bookId)
        book = self.GetBook(bookId)
        if not book:
            return
        assert isinstance(book, BookInfo)
        epsInfo = book.pageInfo.epsInfo.get(epsIndex)
        if not epsInfo:
            return
        epsInfo.scrambleId = scrambleId