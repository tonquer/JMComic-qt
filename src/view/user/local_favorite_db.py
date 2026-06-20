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
        sqlList = [ """\
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
            """,
            """\
                        create table if not exists favorite_fold(\
                        fid INTEGER primary key autoincrement,\
                        name varchar,\
                        tick int,\
                        UNIQUE(name)
                        )\
                        """,
            """\
                        create table if not exists favorite_fid(\
                        fid int,\
                        bookId varchar\
                        )\
                        """
        ]
        for sql in sqlList:
            query = QSqlQuery(self.db)
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
        sql = "delete from favorite_fid where bookId='{}'".format(bookId)
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

    def AddFavoriteFid(self, name):
        query = QSqlQuery(self.db)
        sql = "INSERT INTO favorite_fold(name, tick) " \
              "VALUES ('{0}', {1})". \
            format(name, str(int(time.time())))

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def DelFavoriteFid(self, fid):
        query = QSqlQuery(self.db)
        sql = "delete from favorite_fold where fid={}".format(fid)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return True

    def AddBookFavoriteFid(self, bookId, fid):
        query = QSqlQuery(self.db)
        self.DelBookFavoriteFid(bookId)
        if fid == 0:
            return True
        sql = "INSERT INTO favorite_fid(fid, bookId) " \
              "VALUES ({0}, '{1}')". \
            format(fid, bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def UpdateBookFavoriteFid(self, bookId, fids):
        query = QSqlQuery(self.db)
        self.DelBookFavoriteFid(bookId)
        if fids == [0]:
            return True
        for fid in fids:
            if fid == 0:
                continue

            sql = "INSERT INTO favorite_fid(fid, bookId) " \
                  "VALUES ({0}, '{1}')". \
                format(fid, bookId)
            suc = query.exec_(sql)
            if not suc:
                Log.Warn(query.lastError().text())
                return False
        return True

    def DelBookFavoriteFid(self, book_id):
        query = QSqlQuery(self.db)
        sql = "delete from favorite_fid where bookId='{}'".format(book_id)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
            return False
        return True

    def LoadFold(self):
        sql = "select fid, name from favorite_fold where 1"
        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = {}
        if not suc:
            Log.Warn(query.lastError().text())
            return data
        while query.next():
            fid = query.value(0)
            name = query.value(1)
            data[int(fid)] = name
        return data

    def LoadBookFold(self):
        sql = "select fid, bookId from favorite_fid where 1"
        self.db.exec()
        query = QSqlQuery(self.db)
        suc = query.exec_(sql)
        data = {}
        if not suc:
            Log.Warn(query.lastError().text())
            return data
        while query.next():
            fid = query.value(0)
            bookId = query.value(1)
            data.setdefault(int(fid), set())
            data[int(fid)].add(bookId)
        return data

    def SearchFavorite(self, page, sortKey=0, sortId=0, fid=0, searchText=""):
        if not searchText:
            sql = "select bookId, author, title, coverUrl, category, tagList, description, tick  " \
                  "from favorite as book  where 1 "
            if fid != 0:
                sql += f" and bookId in (select bookId from favorite_fid where fid={fid}) "
        else:
            sql = "select bookId, author, title, coverUrl, category, tagList, description, tick  " \
                  "from favorite as book where 1 "
            if fid != 0:
                sql += f" and bookId in (select bookId from favorite_fid where fid={fid}) "
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