import re

from bs4 import BeautifulSoup

from config import config


class BookWebApi:

    # 解析登录结果
    @staticmethod
    def ParseMsg(data):
        isSuc = True
        msg = ""
        mo = re.search(r"(?<=toastr\[\'error\'\]\(\").*\"", data)
        if mo:
            isSuc = False
            msg = mo.group().strip("\"")

        mo = re.search(r"(?<=toastr\[\'success\'\]\(\").*\"", data)
        if mo:
            isSuc = True
            msg = mo.group().strip("\"")

        if len(data) <= 30:
            isSuc = False
            msg = data

        return isSuc, msg

    @staticmethod
    def ParseIndexBooks(tags):
        from tools.book import BookInfo
        books = []
        for tag in tags:
            info = BookInfo()
            bookUrl = tag.a.attrs.get("href")
            info.baseInfo.bookUrl = bookUrl
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("data-src")
            info.baseInfo.title = tag.img.attrs.get("title")

            authorTag = tag.parent.find("div", {"class": re.compile(r"title-truncate hidden-xs")})
            if authorTag:
                info.baseInfo.author = authorTag.a.text.replace("\n", "").strip()

            tagStrTag = tag.parent.find("div", {"class": re.compile(r"title-truncate tags*")})
            if tagStrTag:
                for v in tagStrTag.find_all("a"):
                    info.baseInfo.tagList.append(v.text.strip())

            books.append(info)
        return books

    @staticmethod
    def ParseSearchBooks(tags):
        from tools.book import BookInfo
        books = []
        for tag in tags:
            info = BookInfo()
            bookUrl = tag.parent.attrs.get("href")
            info.baseInfo.bookUrl = bookUrl
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("data-src")
            info.baseInfo.title = tag.img.attrs.get("title")

            authorTag = tag.parent.parent.find("div", {"class": re.compile(r"title-truncate|title-truncate hidden-xs")})
            if authorTag:
                info.baseInfo.author = authorTag.a.text.replace("\n", "").strip()

            tagStrTag = tag.parent.find("div", {"class": re.compile(r"title-truncate tags*")})
            if tagStrTag:
                for v in tagStrTag.find_all("a"):
                    info.baseInfo.tagList.append(v.text.strip())

            books.append(info)
        return books

    @staticmethod
    def ParseFavoriteBooks(tags):
        from tools.book import BookInfo
        books = []
        for tag in tags:
            info = BookInfo()
            bookUrl = tag.parent.attrs.get("href")
            info.baseInfo.bookUrl = bookUrl
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("data-src")
            info.baseInfo.title = tag.img.attrs.get("title")

            authorTag = tag.parent.parent.find("div", {"class": re.compile(r"title-truncate|title-truncate hidden-xs")})
            if authorTag:
                info.baseInfo.author = authorTag.a.text.replace("\n", "").strip()

            tagStrTag = tag.parent.find("div", {"class": re.compile(r"title-truncate tags*")})
            if tagStrTag:
                for v in tagStrTag.find_all("a"):
                    info.baseInfo.tagList.append(v.text.strip())

            books.append(info)
        return books

    # 解析首页结果
    @staticmethod
    def ParseIndex(data):
        soup = BeautifulSoup(data, features="lxml")
        tags = soup.find_all("div", class_="thumb-overlay-albums")

        return BookWebApi.ParseIndexBooks(tags)

    # 解析搜索结果
    @staticmethod
    def ParseSearch(data):
        soup = BeautifulSoup(data, features="lxml")
        tags = soup.find_all("div", class_="thumb-overlay")
        books = BookWebApi.ParseSearchBooks(tags)
        maxPage = 1

        pageTag = soup.find("ul", class_="pagination pagination-lg")
        if pageTag:
            allPage = pageTag.find_all("option")
            for v in allPage:
                maxPage = max(maxPage, int(v.text))
        return maxPage, books

    # 解析收藏
    @staticmethod
    def ParseFavorite(data):
        from tools.book import FavoriteInfo
        f = FavoriteInfo()
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("span", class_="pull-right")
        text = tag.text.replace("\n", "").replace(" ", "")
        data = re.findall(r"\d+", text)
        f.total = int(data[0])
        maxNum = int(data[1])
        tags = soup.find_all("div", class_="favorites_album_")
        f.bookList = BookWebApi.ParseSearchBooks(tags)
        f.count = len(f.bookList)
        return f