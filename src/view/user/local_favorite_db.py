import json
import os.path
import time

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from tools.book import BookInfo
from tools.langconv import Converter
from tools.log import Log
from view.download.download_item import DownloadItem, DownloadEpsItem


class LocalFavoriteDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "favorite")
        path = os.path.join(Setting.GetConfigPath(), "favorite.db")
        self.db.setDatabaseName(path)
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists favorite(\
            bookId varchar primary key,\
            author varchar,\
            title varchar,\
            coverUrl varchar,\
            category varchar,\
            tagList varchar,\
            description varchar, \
            tick int\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        # self.LoadDownload()

    def DelFavoriteDB(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from favorite where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddBookToDB(self, book):
        assert isinstance(book, BookInfo)
        tick = int(time.time())
        query = QSqlQuery(self.db)
        sql = "INSERT INTO favorite(bookId, author, title, coverUrl, category, " \
              "tagList, description, tick) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{7}', {6}) " \
              "ON CONFLICT(bookId) DO UPDATE SET author='{1}', title='{2}', coverUrl='{3}', " \
              "category = '{4}', tagList = '{5}', description='{7}'".\
            format(book.baseInfo.bookId,
                   Converter('zh-hans').convert(book.baseInfo.author).replace("'", "''"),
                   Converter('zh-hans').convert(book.baseInfo.title).replace("'", "''"),
                   book.baseInfo.coverUrl,
                   Converter('zh-hans').convert(",".join(book.baseInfo.category)).replace("'", "''"),
                   Converter('zh-hans').convert(",".join(book.baseInfo.tagList).replace("'", "''")),
                   tick,
                   Converter('zh-hans').convert(book.pageInfo.des).replace("'", "''"))

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def SearchFavorite(self, page, sortKey=0, sortId=0, searchText=""):
        if not searchText:
            sql = "select bookId, author, title, coverUrl, category, tagList, description, tick  " \
                  "from favorite as book  where 1 "
        else:
            sql = "select bookId, author, title, coverUrl, category, tagList, description, tick  " \
                  "from favorite as book where 1 "
            sql += " and (book.title like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.author like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.description like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.tagList like '%{}%' or ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))
            sql += " book.category like '%{}%')  ".format(Converter('zh-hans').convert(searchText).replace("'", "''"))

        if sortKey == 0:
            sql += "ORDER BY book.tick "

        if sortId == 0:
            sql += "DESC"
        else:
            sql += "ASC"
        if page >= 0:
            sql += "  limit {},{};".format((page - 1) * 20, 20)

        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = {}
        if not suc:
            Log.Warn(query.lastError().text())
        while query.next():
            # bookId, author, title, coverUrl, category, tagList, description, tick
            info = BookInfo()
            bookId = query.value(0)
            info.baseInfo.bookId = bookId
            info.baseInfo.author = query.value(1)
            info.baseInfo.title = query.value(2)
            info.baseInfo.coverUrl = query.value(3)
            info.baseInfo.category = query.value(4).split(",")
            info.baseInfo.tagList = query.value(5).split(",")
            info.pageInfo.des = query.value(6)
            data[bookId] = info
        return data