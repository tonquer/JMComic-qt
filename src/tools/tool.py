import base64
import hashlib
import json
import math
import os
import re
import time
from urllib.parse import quote

from Cryptodome.Cipher import AES
from bs4 import BeautifulSoup, Tag

from config import config
from config.setting import Setting
from tools.langconv import Converter
from tools.log import Log
from tools.status import Status


class CTime(object):
    def __init__(self):
        self._t1 = time.time()

    def Refresh(self, clsName, des='', checkTime=100):
        t2 = time.time()
        diff = int((t2 - self._t1) * 1000)
        if diff >= checkTime:
            text = 'CTime consume:{} ms, {}.{}'.format(diff, clsName, des)
            Log.Warn(text)
        self._t1 = t2
        return diff


def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.time()
        rt = fn(*args, **kwargs)
        diff = int((time.time() - start) * 1000)
        if diff >= 100:
            clsName = args[0]
            strLog = 'time_me consume,{} ms, {}.{}'.format(diff, clsName, fn.__name__)
            # Log.w(strLog)
            Log.Warn(strLog)
        return rt

    return _wrapper


class ToolUtil(object):

    @classmethod
    def GetHeader(cls, _url: str, method: str) -> dict:
        param = "{}{}".format(config.Now, "18comicAPP")
        token = hashlib.md5(param.encode("utf-8")).hexdigest()

        header = {
            "tokenparam": "{},1.4.2".format(config.Now),
            "token": token,
            "user-agent": "okhttp/3.12.12",
            "accept-encoding": "gzip",
        }
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
        return header

    @classmethod
    def GetHeader2(cls, _url: str, method: str) -> dict:
        param = "{}{}".format(config.Now, "18comicAPPContent")
        token = hashlib.md5(param.encode("utf-8")).hexdigest()

        header = {
            "tokenparam": "{},1.4.2".format(config.Now),
            "token": token,
            "user-agent": "okhttp/3.12.12",
            "accept-encoding": "gzip",
        }
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
        return header

    @classmethod
    def ParseData(cls, data) -> str:
        param = "{}{}".format(config.Now, "18comicAPPContent")
        key = hashlib.md5(param.encode("utf-8")).hexdigest()
        aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        byteData = base64.b64decode(data.encode("utf-8"))
        result = aes.decrypt(byteData)
        unpad = lambda s: s[0:-s[-1]]
        result2 = unpad(result)
        newData = result2.decode()
        return newData

    @staticmethod
    def DictToUrl(paramDict):
        assert isinstance(paramDict, dict)
        data = ''
        for k, v in paramDict.items():
            data += quote(str(k)) + '=' + quote(str(v))
            data += '&'
        return data.strip('&')

    @staticmethod
    def ParseFromData(desc, src):
        try:
            if not src:
                return
            if isinstance(src, str):
                src = json.loads(src)
            for k, v in src.items():
                setattr(desc, k, v)
        except Exception as es:
            Log.Error(es)

    @staticmethod
    def GetUrlHost(url):
        host = url.replace("https://", "")
        host = host.replace("http://", "")
        host = host.split("/")[0]
        host = host.split(":")[0]
        return host

    @staticmethod
    def GetDateStr(createdTime):
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        tick = int(time.mktime(timeArray) - time.timezone)
        now = int(time.time())
        day = int((int(now - time.timezone) / 86400) - (int(tick - time.timezone) / 86400))
        return time.localtime(tick), day

    @staticmethod
    def GetUpdateStr(createdTime):
        timeArray = time.strptime(createdTime, "%Y-%m-%dT%H:%M:%S.%f%z")
        now = int(time.time())
        tick = int(time.mktime(timeArray) - time.timezone)
        day = (now - tick) // (24 * 3600)
        hour = (now - tick) // 3600
        minute = (now - tick) // 60
        second = (now - tick)
        if day > 0:
            return "{}天前".format(day)
        elif hour > 0:
            return "{}小时前".format(hour)
        elif minute > 0:
            return "{}分钟前".format(minute)
        else:
            return "{}秒前".format(second)

    @staticmethod
    def GetDownloadSize(downloadLen):
        kb = downloadLen / 1024.0
        if kb <= 0.1:
            size = str(downloadLen) + "bytes"
        else:
            mb = kb / 1024.0
            if mb <= 0.1:
                size = str(round(kb, 2)) + "kb"
            else:
                size = str(round(mb, 2)) + "mb"
        return size


    @staticmethod
    def GetLookScaleModel(category, mat="jpg"):
        return ToolUtil.GetModelByIndex(Setting.LookNoise.value, Setting.LookScale.value, ToolUtil.GetLookModel(category), mat)

    @staticmethod
    def GetDownloadScaleModel(w, h, mat):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        return ToolUtil.GetModelByIndex(Setting.DownloadNoise.value, Setting.DownloadScale.value, Setting.DownloadModel.value, mat)

    @staticmethod
    def GetPictureSize(data):
        if not data:
            return 0, 0, "jpg"
        from PIL import Image
        from io import BytesIO
        a = BytesIO(data)
        img = Image.open(a)
        a.close()
        if img.format == "PNG":
            mat = "png"
        else:
            mat = "jpg"
        return img.width, img.height, mat

    @staticmethod
    def GetLookModel(category):
        if Setting.LookModel.value == 0:
            if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
                return 2
            return 3
        else:
            return Setting.LookModel.value

    @staticmethod
    def GetModelAndScale(model):
        if not model:
            return "cunet", 1, 1
        index = model.get('index', 0)
        scale = model.get('scale', 0)
        noise = model.get('noise', 0)
        if index == 0:
            model = "anime_style_art_rgb"
        elif index == 1:
            model = "cunet"
        elif index == 2:
            model = "photo"
        else:
            model = "anime_style_art_rgb"
        return model, noise, scale

    @staticmethod
    def GetModelByIndex(noise, scale, index, mat="jpg"):
        if not config.CanWaifu2x:
            return {}
        if noise < 0:
            noise = 3
        data = {"format": mat, "noise": noise, "scale": scale, "index": index}
        from waifu2x_vulkan import waifu2x_vulkan
        if index == 0:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        elif index == 1:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        elif index == 2:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_PHOTO_NOISE" + str(noise))
        elif index == 3:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE"+str(noise))
        else:
            data["model"] = getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE"+str(noise))
        return data

    @staticmethod
    def GetCanSaveName(name):
        return re.sub('[\\\/:*?"<>|\0\r\n]', '', name).rstrip(".").strip(" ")

    @staticmethod
    def LoadCachePicture(filePath):
        try:
            c = CTime()
            if not os.path.isfile(filePath):
                return None
            with open(filePath, "rb") as f:
                data = f.read()
                c.Refresh("LoadCache", filePath)
                return data
        except Exception as es:
            Log.Error(es)
        return None

    @staticmethod
    def IsHaveFile(filePath):
        try:
            if os.path.isfile(filePath):
                return True
            return False
        except Exception as es:
            Log.Error(es)
        return False

    @staticmethod
    def DiffDays(d1, d2):
        return (int(d1 - time.timezone) // 86400) - (int(d2 - time.timezone) // 86400)

    @staticmethod
    def GetCurZeroDatatime(tick):
        from datetime import timedelta
        from datetime import datetime
        now = datetime.fromtimestamp(tick)
        delta = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        zeroDatetime = now - delta
        return int(time.mktime(zeroDatetime.timetuple()))

    @staticmethod
    def GetTimeTickEx(strDatetime):
        if not strDatetime:
            return 0
        timeArray = time.strptime(strDatetime, "%Y-%m-%d %H:%M:%S")
        tick = int(time.mktime(timeArray))
        return tick

    # @staticmethod
    # def ParseBookInfo(data, bookId):
    #     soup = BeautifulSoup(data, features="lxml")
    #     from tools.book import BookInfo
    #     book = BookInfo()
    #     book.baseInfo.bookId = bookId
    #     infos = soup.find_all("div", class_="p-t-5 p-b-5")
    #     for tag in infos:
    #         data = tag.text.replace("\n", "").strip()
    #         data = re.split('[:：]', data, maxsplit=1)
    #         if len(data) < 2:
    #             continue
    #         data[0] = data[0].strip()
    #         data[1] = data[1].strip()
    #         if ToolUtil.IsSameName(data[0], "叙述"):
    #             book.pageInfo.des = data[1]
    #         elif ToolUtil.IsSameName(data[0], "頁數"):
    #             book.pageInfo.pages = int(data[1])
    #         elif ToolUtil.IsSameName(data[0], "上架日期"):
    #             mo = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data[1])
    #             book.pageInfo.createDate = mo.group()
    #         elif ToolUtil.IsSameName(data[0], "更新日期"):
    #             mo = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data[1])
    #             book.pageInfo.updateDate = mo.group()
    #         # print(data[0], data[1])
    #     tag = soup.find("img", class_="lazy_img img-responsive")
    #     book.baseInfo.coverUrl = tag.attrs.get("src", "")
    #     tag = soup.find("div", itemprop="name")
    #     if tag:
    #         book.baseInfo.title = tag.h1.text
    #
    #     tag = soup.find("li", class_="p-t-5 p-b-5", id="")
    #     mo = re.search(r"\d+", tag.text)
    #     if mo:
    #         book.pageInfo.commentNum = int(mo.group())
    #
    #     isFavorite = False
    #     tag = soup.find("span", class_="col btn collect-btn btn-primary")
    #     if tag:
    #         isFavorite = True
    #
    #     infos = soup.find_all("div", class_="tag-block")
    #     for tag in infos:
    #         data = re.split('[:：]', tag.text.strip("\n"))
    #         if len(data) < 2:
    #             continue
    #         if ToolUtil.IsSameName(data[0], "作者"):
    #             book.baseInfo.authorList = data[1].strip().strip("\n").split("\n")
    #         elif ToolUtil.IsSameName(data[0], "标签"):
    #             book.baseInfo.tagList = data[1].strip().strip("\n").split("\n")
    #     epsTag = soup.find("ul", class_="btn-toolbar")
    #     from tools.book import BookEps
    #     if not epsTag:
    #         # 不分章节
    #         epsInfo = BookEps()
    #         epsInfo.title = "第一章"
    #         epsInfo.epsUrl = "/photo/{}".format(bookId)
    #         book.pageInfo.epsInfo[0] = epsInfo
    #     else:
    #         infos = epsTag.find_all("a")
    #         index = 0
    #         for tag in infos:
    #             epsUrl = tag.attrs.get("href")
    #             text = tag.li.text.strip("\n")
    #             epsText = text.split("\n")
    #             epsInfo = BookEps()
    #             epsInfo.epsUrl = epsUrl
    #             if len(epsText) == 3:
    #                 epsIndex = epsText[0]
    #                 epsTitle = epsText[1]
    #                 epsTime = epsText[2]
    #                 epsInfo.title = epsIndex
    #                 epsInfo.epsName = epsTitle
    #                 epsInfo.time = epsTime
    #
    #                 book.pageInfo.epsInfo[index] = epsInfo
    #                 index += 1
    #             elif len(epsText) == 4:
    #                 epsIndex = epsText[0]
    #                 epsTitle = epsText[1] + epsText[2]
    #                 epsTime = epsText[3]
    #                 epsInfo.title = epsIndex
    #                 epsInfo.epsName = epsTitle
    #                 epsInfo.time = epsTime
    #                 book.pageInfo.epsInfo[index] = epsInfo
    #                 index += 1
    #
    #     return isFavorite, book

    @staticmethod
    def ParseBookInfo(v):
        from tools.book import BookInfo
        b = BookInfo()
        b.baseInfo.id = v.get("id")
        b.baseInfo.author = v.get("author")
        b.baseInfo.title = v.get("name")
        b.baseInfo.coverUrl = "/media/albums/{}_3x4.jpg".format(b.baseInfo.id)
        category = v.get("category", {}).get("title")
        if category:
            b.baseInfo.tagList.append(category)
        category = v.get("category_sub", {}).get("title")
        if category:
            b.baseInfo.tagList.append(category)
        return b

    @staticmethod
    def ParseBookList(rawList):
        data = []
        for v in rawList:
            data.append(ToolUtil.ParseBookInfo(v))
        return data

    # 解析首页结果
    @staticmethod
    def ParseIndex2(data):
        parseData = {}
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        for v in raw:
            bookList = ToolUtil.ParseBookList(v.get("content", []))
            parseData[v.get("title")] = bookList

        return parseData

    # 解析最近更新
    @staticmethod
    def ParseLatest2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        bookList = ToolUtil.ParseBookList(raw)
        return bookList

    @staticmethod
    def ParseFavoritesReq2(data):
        bookList = []
        from tools.book import FavoriteInfo
        f = FavoriteInfo()
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        f.total = int(raw.get("total"))
        f.count = int(raw.get("count"))
        f.bookList = ToolUtil.ParseBookList(raw.get("list", []))
        folderDict = {}
        f.fold = folderDict
        for v in raw.get("folder_list", []):
            folderDict[v.get("name")] = v.get("FID")
        return f

    @staticmethod
    def ParseMsgReq2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        status = raw.get("status")
        msg = raw.get("msg")
        if status == "ok":
            return Status.Ok, msg
        return Status.Error, msg

    @staticmethod
    def ParseLogin2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        from tools.user import User
        u = User()
        u.uid = raw.get("uid")
        u.userName = raw.get("username")
        u.title = raw.get("level_name")
        u.level = raw.get("level")
        u.coin = raw.get("coin")
        u.gender = raw.get("gender")
        u.favorites = raw.get('album_favorites')
        u.canFavorites = raw.get('album_favorites_max')
        return u

    # 解析搜索结果
    @staticmethod
    def ParseSearch2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        total = int(raw.get("total"))
        bookList = ToolUtil.ParseBookList(raw.get("content", []))
        return total, bookList

    # 解析搜索结果
    @staticmethod
    def ParseCategory2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        categoryList = []
        for v in raw.get("categories", []):
            from tools.book import Category
            b = Category()
            categoryId = v.get("id")
            b.id = categoryId
            b.name = v.get("name")
            b.slug = v.get("slug")
            b.type = v.get("type")
            b.total = v.get("total_albums")
            categoryList.append(b)

        return categoryList

    # 解析搜索结果
    @staticmethod
    def ParseSearchCategory2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        total = int(raw.get("total"))
        bookList = ToolUtil.ParseBookList(raw.get("content", []))
        return total, bookList

    @staticmethod
    def ParseBookInfo2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        from tools.book import BookInfo
        b = BookInfo()
        bookId = raw["id"]
        b.baseInfo.coverUrl = "/media/albums/{}_3x4.jpg".format(bookId)
        b.baseInfo.bookId = bookId
        b.baseInfo.title = raw.get('name')
        b.baseInfo.likes = raw.get('likes')
        b.baseInfo.views = raw.get('total_views')
        b.baseInfo.authorList = raw.get("author")
        b.baseInfo.tagList = raw.get("tags", [])
        b.pageInfo.des = raw.get("description")
        b.pageInfo.commentNum = int(raw.get("comment_total"))
        isFavorite = raw.get("is_favorite")

        from tools.book import BookEps
        series = raw.get("series", [])
        if series:
            for v in series:
                epsInfo = BookEps()
                epsInfo.index = int(v.get("sort")) - 1
                epsInfo.title = "第{}章".format(epsInfo.index+1)
                epsInfo.epsId = v.get('id')
                epsInfo.epsName = v.get("name")
                b.pageInfo.epsInfo[epsInfo.index] = epsInfo
        else:
            epsInfo = BookEps()
            epsInfo.title = "第1章"
            epsInfo.epsUrl = "/photo/{}".format(bookId)
            epsInfo.epsId = bookId
            b.pageInfo.epsInfo[0] = epsInfo
        return b, isFavorite

    @staticmethod
    def ParseBookEpsScramble(data):
        mo = re.search(r"(?<=var scramble_id = )\w+", data)
        return int(mo.group())

    @staticmethod
    def ParseBookEpsInfo2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        from tools.book import BookEps
        epsInfo = BookEps()
        epsInfo.epsId = raw.get("id")
        epsInfo.aid = raw.get("series_id")
        epsInfo.epsName = raw.get("name")
        for info in raw.get("series", []):
            if str(info.get("id")) == str(epsInfo.epsId):
                epsInfo.index = int(info.get("sort")) - 1
        for name in raw.get("images", []):
            picId = re.search(r"\d+", name).group()
            epsInfo.pictureName[int(picId)-1] = name.split(".")[0]
            epsInfo.pictureUrl[int(picId)-1] = "/media/photos/{}/{}".format(epsInfo.epsId, name)
        return epsInfo

    @staticmethod
    def ParseBookComment(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        from tools.book import CommentInfo
        commentList = []
        total = int(raw.get("total", 0))
        for v in raw.get("list", []):
            b = CommentInfo()
            b.id = v.get("CID")
            b.uid = v.get("UID")
            b.title = v.get("expinfo", {}).get("level_name")
            b.level = v.get("expinfo", {}).get("level")
            b.name = v.get("username")
            photo = v.get("photo")
            if photo != "nopic-Male.gif" and photo != "nopic-Female.gif":
                b.headUrl = "/media/users/" + photo
            b.content = v.get("content")
            b.like = v.get("likes")
            b.date = v.get("addtime")
            b.linkBookName = v.get("name")
            b.linkBookId = v.get("AID")
            for v2 in v.get("replys", []):
                b2 = CommentInfo()
                b2.id = v2.get("CID")
                b2.uid = v2.get("UID")
                b2.title = v2.get("expinfo", {}).get("level_name")
                b2.level = v2.get("expinfo", {}).get("level")
                b2.name = v2.get("username")
                photo = v2.get("photo")
                if photo != "nopic-Male.gif" and photo != "nopic-Female.gif":
                    b2.headUrl = "/media/users/" + photo
                b2.content = v2.get("content")
                b2.like = v2.get("likes")
                b2.date = v2.get("addtime")
                b.linkBookName = v2.get("name")
                b.linkBookId = v2.get("AID")
                b.subComments.append(b2)
            commentList.append(b)
        return commentList, total

    @staticmethod
    def ParseSendBookComment(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        return raw.get("msg", "")

    @staticmethod
    def MergeUrlParams(url, data: dict):
        if not data:
            return url
        if url[-1] != "/":
            url += "/?"
        for key, value in data.items():
            url += "{}={}".format(key, value)
            url += "&"
        return url.strip("&")

    # 解析登录结果
    @staticmethod
    def ParseMsg(data):
        isSuc = False
        msg = ""
        mo = re.search(r"(?<=toastr\[\'error\'\]\(\").*\"", data)
        if mo:
            msg = mo.group().strip("\"")

        mo = re.search(r"(?<=toastr\[\'success\'\]\(\").*\"", data)
        if mo:
            isSuc = True
            msg = mo.group().strip("\"")
        return isSuc, msg

    @staticmethod
    def ParseHistoryReq2(data):
        result = ToolUtil.ParseData(data)
        raw = json.loads(result)
        bookList = ToolUtil.ParseBookList(raw.get("list", []))
        total = int(raw.get("total", 0))
        return bookList, total

    # 解析用户信息
    # @staticmethod
    # def ParseUserInfo(data):
    #     from tools.user import User
    #     user = User()
    #     user.isLogin = True
    #     soup = BeautifulSoup(data, features="lxml")
    #     tag = soup.find("img", class_="header-personal-avatar")
    #     user.imgUrl = tag.attrs.get("src", "")
    #     tag = soup.find("div", class_="header-right-username")
    #     user.userName = tag.text
    #
    #     infos = soup.find_all("div", class_="header-profile-row")
    #     userAttr = {}
    #     for tag in infos:
    #         pass
    #         nameTag = tag.find("div", class_="header-profile-row-name")
    #         nameValue = tag.find("div", class_="header-profile-row-value")
    #         if nameTag and nameValue:
    #             name = nameTag.text.replace(" ", "").replace("\n", "")
    #             value = nameValue.text.replace(" ", "").replace(
    #                 "\n", "")
    #             userAttr[name] = value
    #     user.userAttr = userAttr
    #     return user

    # 解析收藏
    # @staticmethod
    # def ParseFavorite(data):
    #     soup = BeautifulSoup(data, features="lxml")
    #     tag = soup.find("div", class_="pull-left m-l-20")
    #     text = tag.text.replace("\n", "").replace(" ", "")
    #     data = re.findall(r"\d+", text)
    #     curNum = int(data[0])
    #     maxNum = int(data[1])
    #     tags = soup.find_all("div", class_="thumb-overlay")
    #     books = []
    #     for tag in tags:
    #         from tools.book import BookInfo
    #         info = BookInfo()
    #         info.baseInfo.bookUrl = tag.parent.attrs.get("href")
    #         if not info.baseInfo.bookUrl:
    #             continue
    #         info.baseInfo.bookId = re.search(r"(?<=/album/)\w*", info.baseInfo.bookUrl).group()
    #         info.baseInfo.coverUrl = tag.img.attrs.get("src", "")
    #         if info.baseInfo.coverUrl and "http" not in info.baseInfo.coverUrl:
    #             info.baseInfo.coverUrl = config.Url + info.baseInfo.coverUrl
    #         info.baseInfo.title = tag.img.attrs.get("title")
    #         for tag2 in tag.find_next_siblings():
    #             className = " ".join(tag2.attrs.get('class', []))
    #             if className == "video-title title-truncate":
    #                 info.baseInfo.title = tag2.text.replace("\n", "").strip()
    #                 pass
    #         books.append(info)
    #     return curNum, maxNum, books

    # 解析首页结果
    # @staticmethod
    # def ParseIndex(data):
    #     soup = BeautifulSoup(data, features="lxml")
    #     tags = soup.find_all("div", class_="thumb-overlay-albums")
    #     from tools.book import BookInfo
    #     books = []
    #     for tag in tags:
    #         info = BookInfo()
    #         info.baseInfo.bookUrl = tag.parent.attrs.get("href")
    #         info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
    #         info.baseInfo.coverUrl = tag.img.attrs.get("data-src")
    #         info.baseInfo.title = tag.img.attrs.get("title")
    #         for tag2 in tag.parent.find_next_siblings():
    #             className = " ".join(tag2.attrs.get('class', []))
    #             if className == "title-truncate hidden-xs":
    #                 info.baseInfo.author = tag2.a.text.replace("\n", "").strip()
    #             elif className == "title-truncate tags":
    #                 info.baseInfo.tagStr = tag2.text.replace("標籤: ", "").replace("\n", "").strip()
    #             elif className == "video-views pull-left hidden-xs":
    #                 info.baseInfo.date = tag2.text.replace("\n", "").strip()
    #         books.append(info)
    #     return books

    # 解析评论
    # @staticmethod
    # def ParseComment(data):
    #     soup = BeautifulSoup(data, features="lxml")
    #
    #     allComment = []
    #     ToolUtil.ParseCommentData(soup, allComment)
    #     return allComment

    # @staticmethod
    # def ParseCommentData(tag, allComment, isSubComment=False):
    #     from tools.book import CommentInfo
    #     tags = tag.find_all("div", class_="timeline")
    #     for tag in tags:
    #         info = CommentInfo()
    #         index = tag.attrs.get("data-cid")
    #         if not index:
    #             continue
    #         if not isSubComment and "{" in index:
    #             continue
    #         info.id = index
    #         userTag = tag.find("div", class_="timeline-left")
    #         info.headUrl = userTag.a.img.attrs.get("src", "")
    #         info.level = userTag.div.text.strip("\n ")
    #
    #         rightTag = tag.find("div", class_="timeline-right")
    #         nameTag = rightTag.find("span", class_="timeline-username")
    #         info.name = nameTag.text.strip("\n ")
    #
    #         titleTag = rightTag.find("div", class_="timeline-user-title")
    #         info.title = titleTag.text.strip("\n ")
    #
    #         commentTag = rightTag.find("div", class_="timeline-content")
    #         info.content = commentTag.text.strip("\n ")
    #
    #         timeTag = rightTag.find("div", class_="timeline-date")
    #         info.date = timeTag.text.strip("\n ")
    #
    #         commentLinkTag = rightTag.find("div", class_="timeline-ft")
    #         if commentLinkTag:
    #             linkBookUrl = commentLinkTag.a.attrs.get("href").replace("\\/", "/")
    #             info.linkBookId = re.search(r"(?<=/album/)\w*", linkBookUrl).group()
    #             info.linkBookName = linkBookUrl.replace("/album/{}/".format(info.linkBookId), "").strip("\n ")
    #         allComment.append(info)
    #         otherTag = tag.find("div", class_="other-timelines")
    #         if otherTag:
    #             ToolUtil.ParseCommentData(otherTag, info.subComments, True)

    # 解析搜索结果
    # @staticmethod
    # def ParseSearch(data):
    #     soup = BeautifulSoup(data, features="lxml")
    #     tags = soup.find_all("div", class_="thumb-overlay")
    #     from tools.book import BookInfo
    #     books = []
    #     for tag in tags:
    #         info = BookInfo()
    #         info.baseInfo.bookUrl = tag.parent.attrs.get("href")
    #         info.baseInfo.bookId = re.search(r"(?<=/album/)\w*", info.baseInfo.bookUrl).group()
    #         info.baseInfo.coverUrl = tag.img.attrs.get("data-original")
    #         info.baseInfo.title = tag.img.attrs.get("title")
    #         for tag2 in tag.parent.find_next_siblings():
    #             className = " ".join(tag2.attrs.get('class', []))
    #             if className == "title-truncate hidden-xs":
    #                 info.baseInfo.author = tag2.a.text.replace("\n", "").strip()
    #             elif className == "title-truncate tags":
    #                 info.baseInfo.tagStr = tag2.text.replace("標籤: ", "").replace("\n", "").strip()
    #             elif className == "video-views pull-left hidden-xs":
    #                 info.baseInfo.date = tag2.text.replace("\n", "").strip()
    #         books.append(info)
    #     maxPage = 1
    #
    #     pageTag = soup.find("ul", class_="pagination pagination-lg")
    #     if pageTag:
    #         allPage = pageTag.find_all("option")
    #         for v in allPage:
    #             maxPage = max(maxPage, int(v.text))
    #     return maxPage, books

    # 解析图片Url地址
    # @staticmethod
    # def ParsePictureUrl(data):
    #     soup = BeautifulSoup(data, features="lxml")
    #     infos = soup.find_all("div", id=re.compile(r"page_\d+"))
    #     # infos = soup.find_all("div")
    #     mo = re.search(r"(?<=var scramble_id = )\w+", data)
    #     minAid = int(mo.group())
    #     mo = re.search(r"(?<=var aid = )\w+", data)
    #     aid = int(mo.group())
    #     pictureUrl = {}
    #     pictureName = {}
    #     for tag in infos:
    #         tag2 = tag.find_next_sibling()
    #         url = tag2.get("data-original")
    #         id = re.search(r"\d+", tag2.get("id")).group()
    #         pictureName[int(id)-1] = id
    #         pictureUrl[int(id)-1] = url
    #     return aid, minAid, pictureUrl, pictureName

    # 获得图片分割数
    @staticmethod
    def GetSegmentationNum(epsId, scramble_id, pictureName):
        scramble_id = int(scramble_id)
        epsId = int(epsId)
        if epsId < scramble_id:
            num = 0
        elif epsId < 268850:
            num = 10
        else:
            string = str(epsId) + pictureName
            string = string.encode()
            string = hashlib.md5(string).hexdigest()
            num = ord(string[-1])
            num %= 10
            num = num * 2 + 2
        return num

    # 图片分割合成
    @staticmethod
    def SegmentationPicture(imgData, epsId, scramble_id, bookId):
        num = ToolUtil.GetSegmentationNum(epsId, scramble_id, bookId)
        if num <= 1:
            return imgData

        from PIL import Image
        from io import BytesIO
        src = BytesIO(imgData)
        srcImg = Image.open(src)

        size = (width, height) = srcImg.size
        desImg = Image.new(srcImg.mode, size)
        format = srcImg.format

        rem = height % num
        copyHeight = math.floor(height / num)
        block = []
        totalH = 0
        for i in range(num):
            h = copyHeight * (i + 1)
            if i == num - 1:
                h += rem
            block.append((totalH, h))
            totalH = h

        h = 0
        for start, end in reversed(block):
            coH = end - start
            temp_img = srcImg.crop((0, start, width, end))
            desImg.paste(temp_img, (0, h, width, h + coH))
            h += coH

        srcImg.close()
        src.close()

        des = BytesIO()
        desImg.save(des, format)
        value = des.getvalue()
        desImg.close()
        des.close()
        return value

    @staticmethod
    def IsSameName(name1, name2):
        return Converter('zh-hans').convert(name1) == Converter('zh-hans').convert(name2)


if __name__ == "__main__":
    # ToolUtil.ParseData(1640933310, "wV60pmqKsG5SWYgofUhsBQVFHVvxowZJ+Hp3GooM8NoZsL8g9klKHgeiNlXqVw9IXviwHxceBOQCYmkLulZNYEk6G\/rdv5Zif644m6s1EAcbdTpia1PqD3kOuCV9ny6AjmWGitpopiHs6OD+PWVASX28VD33Vh0ngIC1L2HX+gGqeDGtB5jboRoNyodsZe21aWVFP9FwYRvCT\/iTivjUrZ40ByRad1nFfuxqn5OHkWq983jFtsIeUCnJTFBjWOGq5XMA7XmxHmz9OJKT2PR5E0gD+HHcihbGfzMeck\/RSJtwZmospTfJL\/\/WFGzR993VpSbXNLANgd1x1dlkVWp7swQhhewQM\/uVgBNIW\/HIWfB9vFQ991YdJ4CAtS9h1\/oBE3qSo+F5szfGb7iWpKINeSyHzlYWMZDCCcFfz0EHG5iE2SsxtVz7Mm+66Gz4zT30V9vW46V9L4NL+D+kuLq8++VzAO15sR5s\/TiSk9j0eRNIA\/hx3IoWxn8zHnJP0UibLLdWv0yHvy2VJm1bFinjaBrK1pG9BZc6VigqnRGY4nh6eOfPcq\/r61rtT82EdmNpfbxUPfdWHSeAgLUvYdf6ARN6kqPhebM3xm+4lqSiDXmq5h0gTnH\/3xhi\/dFtGzydwXzuoPWzF9knUNkagjG8UXYZRRDP2IcQOYvkGz7ef119vFQ991YdJ4CAtS9h1\/oB+OqsJhSzDRAaElXmoPbbJlWWD4v2Ak8bImrFw29qy3uc2DYJF3Tr7BOEx+9YzMUTFiMWl5PFnV1QfWXIpnj3wk3KfxMefHAjKD7nnsv8tNdSTlAgBpC8fN0XhSC15b7kuRVrutJMShlFEwOG5LMu57exmt5PLtON\/51Oc7GHuW72D8xT4FVV9\/Rm0zUAjTpHn9bG7C\/aFfT9GKCcoxJxsljEn8suqOayO0s1o8RmcDbqO9+sKf3y3qZCHjK4BCJMBG8nPlEsniGb1ixZVJ9yBzhYxJrSMVXtOKVcmDeHM4qObRVLIOqAq+3OHjQYjVstCl2n6Fj5O+VvRU35tJNUB3pa7THCoIHXj\/kvW+fvabkl9fNqJb\/\/dCklWVg\/KAXtBo1wq+G5R9wu7ZfE7fnW4Gm+m8oVTTC0UTAkeFga+bIgT95r2+3biocmK3MiiafE9k7e3c94Ne+fL8jeSTjewvbtLHglDAM2GGb1cDcALEvGyH+AtmsTbz+l6UqZifXEiABBK\/6zaBkSw\/AWZVWUGpS7Pcgo5FRsUUkCvMRclRg0hMLqtQAh6JK2fFzZJYhX+8JmlmmAno63LodrXvE\/l9R5CysTMpRg+4QJ5G5wj0eKVE0dw6Qw8TS7ghhFENruLNLpTS0tH7LUKSS4APnuTDzwmWnFgTzhDHOcOzQNPH7SxJgqRHCLOoevbf9rkfHoDYhrhvhNiZhsYQ3fR1vvJ18Q2vFOkDuWcIm0+ngV10T3UgduENf3ob3hZeJdW2wUxYdDcXxvsIn\/CBOF+9k5Xi7s8AuhbNuUngXYQQVpY0cLjyiabMkckPW\/UewlY4pgBCRm4ZWkMZGQDzdNXLtZ2ZoGvp6pAGbRrLCFQZolndQe\/6DhvKirsmSdYUF+2UOZ2GlRrqW3C3VCp4OjiMpHF9Ds26eSlB5AhqQp\/f+f\/96iQTOJtwHpcsIRsuoKHXNBpKBxfuALnOqv9xwpOXC2OpjHKSP9CJdVDoPaWOUpAT5o181L5RWCvhsEzY8OIsm1A+S3dIHfeZPVcV8hwXBeaQ==")
    config.Now = 1640933310
    ToolUtil.ParseData("MgC0uSqNs+mVlPUftp8bxMF3C5K+ZV0C5NjH+jzjGbFpFvK4qs\/xpjqGyD81SNRxwN6t6BGOxO4qIKa+1r29xl7K0lxtxo+yRkddu89tjYhaR9kg5qniNyQyq8ZFbuJeMDRzSJMkxaj17LmPuCp2a6SFrCNzcXDRG552pAA0aweRgIz7EZdw5uRu\/jFAtqybjWbs+Ocy86HwvV2RdhLqlNxh8mQgoQR+9lrRs4437BP2JXSPVdtIVe0TOu7Gnxl2bUPvpcdREPsw3s7B4ArR9NxBdLe9EYxt16fR20zSGZsx7oeiZegzWQP2qfULATjNXUbxwKcb0B8i4Ebv6YrViocghVg80puwWXpswlI66cblv43Db\/2vHnSKDtD2JmcP\/4dOkBhGnIAagx78gp0uuyPm3WGkbZEs3YnYg9M1gInXo3mUcBLLOUQhHz1HE6FTSK+CG6Cdnh3wX7vpF1To10jbZUhec0Mk+O5D\/4kcAbkpBAnE2vxo8dLodkFV5WkO\/0WW11S46ceEboBF2CZik6TOTroT7gL+Mx1OBMI+dtPGSWPOGCvU43Izi9lk2Hlr49ruA0DaNPdOH15ypcuuG6PQ9xgTWBjlQ69rsYnF8+7gu3PBJYCZhPAgBDYx+ZLV2lzUVQrXhnT5Kh5yCAlRUEnWcc4\/n+qS\/RdR2kMF2XdDvBE\/oEnUOsfUSB65RHjGjksCKUhcoMbyBxIP+GJwHKVjJ6BlruHH0GGY\/mH7PbMGDqkaqv+sgSijXjzgkfs2s5WyRxsW8oNjjPUHDPWRbcEBIzoQ6\/MvOMI84ONs3j+cRU6qbnfQXHFqYrb03wUASc2v8199rmBKCE0Nwj7gRbBdBtt0WQ9N4WmHdxUxlyiuUMQfb5K4M\/tr1VqkIaNIexh\/9vGwRDEVjoNopJrgXf6Dy6qvbsfYz\/3KVtgRdPcLolUFPjYqyBiDzimZ+iWFeSxzBqYyDGwgDdBgB224YrtdqE5N7EJvolcU2j14kf3lxomzGfioBVpyTDz6bxp\/JUAxO0ZmC1SVqziXAkXxvbcDEiMX0\/Gpcw3NocVCE\/9iv9cLg7c+obXz2RVLYkyJeaMKgYsHxDURRSLrU3+by5HEHwSg9wJrPPQfMCiJ7t7eGoRTVo29yPmayBVWiysLjz3U6TVk3+frXIIYlQ\/\/L+eDzhvUXNrOYrKGGD9BN4HF1wdGw+BadxBXBLhM\/W4dnEPfMibAG1BoPClxnhYDI5FqEYXzeDZ9e2NVwvOUsXcas31sP30FQZCT0BwEGP9plpZOJ\/gJ983fblgyngcXttn7tbZLd8MG2lDW8e5OemfrktYlkzPUHO84HCrPhyDi3btrWqb\/LJ3Qd4lSw3Pt8wzg6PsLzdpbLJtXcEbf+BHwymxdh6XZL8LU1oK+opVJqiJODJnVwQM4e6YT1Dh+BujQr9AtBlhItZHPnWaT6gfUK2upHnmdpYd3ywXKkt7Yyjs2UOeSwDTO6JbjTXJWSVd2HYUGiiQfRvpKmTvy6ya8VKe1FpHI+dsUYGKbMDBcDKEMmO6HMp4lhq97dah3CuhS4Gzrg\/4qLsFmP2EiejmR5LAcsFFyE8EKje7s8y1SoYjxpMo4coI+ihQ0hSy6RsWSxzP3BeX20imWeeTcKoCBy\/k9tY6Btdw\/J4\/0Cb5KIQrwJS7Mya\/CWWS\/\/yYCoJ51JeK0pLjArbzdOIx3KtzoK\/saT5sSJ82PZhCD+5kDSKTu0EljDOvsc5rL3BpEAsP1+PNPcYFweKsYD9JCO3mZL75sRyZFXKvLss2lguceVMXuZJ07Hy4musL1jBcire0atnYa3ntO3\/PBPFkn9VYmrvo9eWfqNiLN3GRb6CEp+IbSvDEpb6P4\/EWaM+dZITAZQUW7pF5B2JVDYMkirGDCcrt1gcowdKYaY3lHTEe+agzXNKV+AEF3og8YsMNgWkcOGcLF5yCARMD1MpOgEOFNM9Zx5jvNZtQ8vviMmznWoE2KY+Rz5gOcPgnbe4162JvaLAy0R1djhATw6L\/\/E2DqiaAsJgZsNkSZK4\/D65n0l0rNHaPWFd4qMCCyc9wLwhR1Ly92GDuLaRPlErEcHz8uqp7+\/zpFWPZ5QiLgJdAFq5SQ6LVA7WlV3YncdWeMxlZLYmDD4U9JSZ4XiTvyWjnJH3HUfI+lsvDsJwFLSE0NAGexpVLTJPU9aP65BaeCYEmaiRjbffmCqvV\/ONUwYKCtdIgs8+x0U6t2xN89Gbks2KJDdeRO0Ba7+JeBNTGyiidUYv3LICF+BgL+SWPM0NfrlClwxCDWc\/jCUrEMlg3gO3Up4\/nvfk2JZ+Jjwu87+VY4lwajw6qMtBtJSCWv+Q\/aMhPa8ekoUqDZEstZLtjQllWcBEgfchoCJQg1pLxJPBvG9U3so0gDBvnvKm893GBqWCyfhBZxRZ95n7oBhPXwtl\/wcplDyhsXF21KBnF8eyOskkG+1q+BUKtahjLl9QDCQxS+xGSHe1rk20+xMQCs40DRrARDeC7qqhAcThoEHCgsI7955zA6bJJEgF36B85JzcRdUFbJ2SYMq6NxSFyKpXR6d2CvhE5\/0zVHBH++r9a8kTIhAjdUt8kigF9bAmGfk1JQtaKyMmaiOmq9GGl8ZPGl2iJdTxrgVB9oQgcm7yNC5eJ7upadcR8kmw1+rgWIqIbciCZYGzHkI\/dHZ3yDKPwUhhzaLO\/jn5qZ73pXW4kKDmSdPBAojUI5ye\/+yAEW7n4a+\/2VGj3H4sBIWE62tLFjRIzf7yzh50gg7RHSBMxEjUT0JTTfFRCrRNFFkmHxUqn+If\/pnMvcaWZCeoXUeWQa80J8lbYMYllyXXTB+TWsq3l61VyGmRoRH2QNH+bVxVtuQJzocCljhsbHvXYkyyjfVC\/xWmrOutBUElXL5wM+cDiJXXxsWg3tdVE7vsxozwdb+A7ChemoKNeVwrROkxvoOZBlMfdHPMi+K5GmjE2efDeMTWEefS+oBfbY10222Qj\/UdfcoZfQiUlOUQvofoLqMR1hjrWDrx3vql0mTDAls4KNnKwJApKdOcFCyRBO9BjDprSLerEY4MItQBcGDmDfhTcvRPNgfZ\/qYos8Stpc1FUK14Z0+SoecggJUVBjLHC3AirolaeX8jcg+SE2wWs49Z60+Qn5t1WUTFRxlY5LAilIXKDG8gcSD\/hicByUqCqVeDtPp6Fdziy3r0MBPUWGUnPgFa\/RB9HGVwkrEJY1PMzwR8YXVL5S6\/tpNc5mRAfgwbaeOtTywEq\/mOuO2Yx4kan1eFcEQzBxCpbzmi0wtLBUw8WomExJGghlNUTgkXmqr1MjWqhmkT27w865MKH+wpcVob3WRFqRvNpFW+N8LIrWg503tWEvs\/5rszQf38spFZ73DWM4HCqY2UOV1JoBfJqpg+0ZyLrfPaoM7xoc91FAhOBq3+mG6zQfhTz474iN2DIOWm7LClWZgkAYuOgUmleSI0wSyKEQX6AMeZgeewzUe\/y439FfunKSKK870H1QX\/Hpc1AUPCcHhT1huxwhfWY36jBmd5Ikw1\/4bUhdJoZIf3Piaa6MhrkUaeLs3Qrgv5ZBoI+\/RNA14TL4nNw8Ej4OJch\/JAumgF\/r06rtyS9Uxh4ChkjXpOEsJwLjUbmbQoGWgmQ+2LEr2pskpi0hkqY4TLrCVRP3pLwYUkNQhJK9\/mfz2oFHeRX1ibcM+0wFxwhr984M9Z4UGiu4iyp1XSRB+a3Db8Fcl\/yCv38jdcMtYAsSeC4k1R0xe\/F+5ckKqddRy8\/fBAVczgP2ZkXkne6lS1bPbC7j2jI2kIrARwdPwnNr61+dUVy\/di9TbxeWCMdx+0N37eUNdqp+T1JvliH78CnX3OUqFXoJpJx532dkGeQcLev4bDpNKgTnbuotQgtLEdZpScYFlGVm\/A1i+DzKpns59Ly4v7oXN+rzwtfneyF4dCSWg3aR3jS7N8+wLc38Mvp32N+WQLXwxTee6mPBl+20VFyt5DWweWhd7AD8EFMAdjYV3WUYom+17\/Y6pnHRkmQOk+EY8gF26ib3h5CWINZCuexWe9GCse1LlEHfHwC2QlBzyUoe64xz17hSThifHdwY0Z2Fx1ROFtrZI+Tej1FjWMM\/KhwCtW0nEl2qWrbGWHtqO0SzFitOzYwbblQndTcEpxM+XWx8wnK7dYHKMHSmGmN5R0xHvinC6jrtolmhFpNR9t5z2UDmTF5Z\/i9dpJMG0t8FIEFCTTPWceY7zWbUPL74jJs51hY2835L4zZ\/lAumaJedLlGlfwge48iWe3FfKq5EkaXbXo1vxSs6RoDUggLk+3NMQLkonEVZcLmmweGSR+0q8BR5nABw9AibUQP8uyTyFheYvLCydMSvJUeJiiB7DUEfNLquSIl8aEEFctD1aUu3jMbBpnVc9f\/veKcwgiZycwkMyh2CuaDlq9RkXUyawI\/KiH2bms5aIYO0PWHlu0\/xDg3hlDrz5KOQZ2VLWbLvd5lF6HX5tRTcHHykhd9ybqXkEy+h88lnvqQlvUGmMGEqvI1fwH4gcOaIbUFvycxbnL2GSBNazI84Rp2A9blqzMoDcIOHu+CJ8boH7\/Cq1acgvoar9c2y7S\/LzdeHKjtD79Fbuz1eCPK8MGC1BgtLfrfoa82CMeqvMkaXgCOjIH7PmSWs715C6SzqYyT0axQBAgog1bLHEaNT\/z0CWGy9LZSTwNWiVeWlu8lzDWn490R9NHDMdPAi0OygUQBt\/LF3F7qy3r3xubUnHQABFBnexZl8kO\/2oRXrf7seor3zU8UpMARblK5R8oX93VwtxnJyPlHyrdkDDam6ZHbVSnQH0aK1ZXIpNOoqbuHy4Pq45QHHZylSLpcHGo+kkVj3iJHLHhdAad7jq6pMRBoccO7GhEwzf+BkWg0j6MTC4UJgd3tXnIPP2V8bif6W+5nG+oEfju8Dx5C8Hzx6LZeL7nAM2Sy4XbIT6JuKIomrgjWSmpJqXG9moyKM2nDKkjU\/t10aRxE65hZmDBSuY+eErZgDJf9R8hbufhr7\/ZUaPcfiwEhYTrbUuuuEcgVPdFVRSP9F3H03y\/Trym7yYeubP+HVdz0LY6ONk5ZzgO5m5qoNXEcnCnernFvuojaPpWnQdalNmw7UEyvxS00pBMj3dWtYzOmx9TpbFyAuCCnnjIA4UADY51buN\/2oWqvNFuTew3u2N66FzZk056t\/jX2Q59iWbbIl88u\/pPIn4gA7wrn5r2RlqRAXnSckkD92p\/Xb8b7awJr2WEYSD0km3QNN\/obqp2kWDWaoLAcHH88a5oddWUsiSFpLzi37A5H1emoy60sxmJiZVCGZTuHQ6NpGxj09tT89\/FnVaHO7yJSLZ0c6k5EPVVQz5TBh0Ytn4LzXJxlIfgZBpCHIq5PKBzyrum9GdHzue2MscLcCKuiVp5fyNyD5ITYdvTLL3oTGmF9foOi+rPDLQ59S\/Qp519s1+r01PrHjSp9oMSrLxy14l95tD27XhXx+wkADz6GFUjA5NOK4I4TqMDRzSJMkxaj17LmPuCp2a6a9Nb7dhZvEpo0Hv1oFPSXfIDCibZAQOY1mmbuwDaFPlNqZuSAbhRhgFvEq9pG+2NA02rsfWWt+nHXY6UD\/FKSJDs2MxyD20eob+5VyCcCAHnZVCpHCl0C0x4iqBHhh\/9+q6diPRD3YHW6M50ZDnnyUwp5f7exriMPpz0zk5Tg++2BDcJbwvUfbRTgdDfz6Vz1Sjkz1HHWWSXgpO5C7M3B7T3pKWf4srXrlmTbrFNQpN5ETc5To+mzYeNKt6QWtH0XaJnWb7NPXlkPnTPDqOj9lIOggBZW36xljopuhoy6KxR+CRs08ijiT7vh5ExIc1rOvVJ8hAY24q6AudvCJjHcWS9ALSPSy4E+mzDgdGSv9Qu7aF0EPoWNvPGfaOLKvAt\/xqVr\/ZzlmAvA4Evx7kJIp2SwwFa56tLYXzXZi3Ly7dfekMoKn4hW0R9pS54hm18i6ykHwn8KYOJJnJubGKesrX64ofRS3ealLzcoElNNKM35EY5DX+5gOVBzbDhH8eXGnGSexMGr0J79axAuSbh2FrevhGPkweTNdFS5bTuRD4zCjH9ilnBq5eeLDQUx0Flkr3Id9+yII2BmURatisZpNHskrUXlXc\/AeaoM0Mo5y6U\/C4Rvgo6USFANkatc1teqX\/S8KCcoqsfnThftAQ9zNHx3GX4vI++zISTdTH5bt6FbDx8eZJKqJZBCnUHYxeHz6ddp4ldcKZyBbeyaKQ\/JcsOdW3KTIP0AdRO2ii7PIn5bxl5Ed2OVDatQyk7n7X5IUo4K8xCwTc3q1bb8WvyCXI+FZr5B2MC695pYvd556+0A7xGTt0C0EKSZH8D5Dg6ANbewwv3S1e2mNDOlTPfKwdNEx1Itv01UlHgloanxF\/rcu1wMISkiWLO17D7qasuP6qY1Ni4XA4fhMwZvsLEdLsjQbuX9nmjJsL7LMOMwWEA6nzRNg6JA+uLI4LuCG+Crk2kRDZ01HJ2+5M\/2pHpViv9cLg7c+obXz2RVLYkyJpWMnoGWu4cfQYZj+Yfs9s07IJNn9rX93G3cEMQ8qqnjPaqMCCTlgZzV6vCiDRktthENJx5oE+hLUZf5YVLKNx1C3tD8t6tJ5aLmsLr8rkatJdmntVHi5gmjZKOis6ifgRoaVg2f1V77LezXrm6IQ5iKxXnpQZVqOdMhsSa9S97rXL5XMNvHm2\/mCpDgTOWn2YpuP+tBU7ETHjgiKftGQ5dzXyNIEAUBvODtefJ4bkefcQXS3vRGMbden0dtM0hmbMe6HomXoM1kD9qn1CwE4zV1G8cCnG9AfIuBG7+mK1YqHIIVYPNKbsFl6bMJSOunGR87VLTQ2Fg+s1fiQVE5xFs8tt027d0hqbwEXQGOgRcqKLmXcXcnxG6raDxzr3DhfSeUq56y\/zZMsK3rfC548uF3KcrFEmDKnUZcqtUrDbux9sw93WMfQERd1zrDCrVdfg7+DzT\/HKCRKUAX5wUwPPzkrN1kALD3gy\/xkkx4C3tIJlKBeRKNOEiavHFvIvmgBDW25H06yXXnbXMyOjV7gIDQ4PVmwvC5pnEDeZauwyEHcQXS3vRGMbden0dtM0hmbMe6HomXoM1kD9qn1CwE4zV1G8cCnG9AfIuBG7+mK1YqHIIVYPNKbsFl6bMJSOunGR87VLTQ2Fg+s1fiQVE5xFs8tt027d0hqbwEXQGOgRcr36hkKXEn99Kde6iMRvSQB+9+Kmo1oRSbkg2JCBR3Qq8tBJib0c9wPNaLC77dP39U2\/mPNIho\/AGjChbFRjCRLqF8g5eeRFYFwtQ4vZKL8q\/Q8FUDSQnVeEei9OLdMmbjoQFApC5ZsZHvA97SCmOVWsuQzQAaMhuJbfpzvbqoE\/HlKnnN8GTKEq68C3nMU1qSJDs2MxyD20eob+5VyCcCAHnZVCpHCl0C0x4iqBHhh\/9+q6diPRD3YHW6M50ZDnnzhU0GFgxnQvbJ80EU5ut9L\/XOXTOOJ8OX9CtSpXCi6niQyQb5C6Qc3v3Gpuf+Amqq1jDzboQVH5snokgJX9OE4KDbQ7V9amH1lca\/hbthQ9zA0c0iTJMWo9ey5j7gqdmuZAqbK9MO15BFmQ6FMoZEc6\/A5pO6drKisTY5byhB0uPv3630\/2oVrkpXUa2qZ4D0axWTJFueqG5KTn3LIvgUudUbRloEGhhS4OWbqNBZqbZx532dkGeQcLev4bDpNKgQWNvN+S+M2f5QLpmiXnS5R4ABI4xBMV9OS7tMoX3+IaAHDCNacTTj4PWieHGTiHE5PEiXMlH4WLt39lGjMdXhMWPLR+SBeAUF2CueAAIq04s2Cb5hFTxeSl\/Ov++Ii\/p5i2C1sZk7QK\/hq\/f20nGoUkdfXOoSsYK3miIn3Zg\/05ZpxG4LVdHgKD+T0anwbEI4eDguNOOnKWfs75kxhl156hx5jmxixGXOooLkPhBIMtNpB9V6EAbMdF46O43MbNqUDaPkk4QTRRh420G65RVK2v3iq5TI5c2phUDsCXgRhlyS6oemCX1LMJa0jSGEsOdFNjKq0xEKRjdv2o2FSNbGsU3gjIw2SSRDMvOOZTKfFHP4SWB5AU+iM5GmJHrxf4diVMCZktLLbg\/Z\/eoOpEBcekBs69INd2QUC6XGf0HfGjTgggTmndiAzTrgXGrd4bd1O477u2J9TbrI96l1twb8VXcpysUSYMqdRlyq1SsNu7JJu1qIceUJJQlNftZfI5msJQ\/Bgvp27IlOYZkDWKVB4hF1p83rOHqd+xYCgMExyJ0mJffnPLnUcBwRpVaeb0EuA4pGivCWGRbFuBiohrQ3GkLTti7QfhIFFA84O44PSLhbufhr7\/ZUaPcfiwEhYTrZv4kzL6rx0cCBlTrzi0\/Mxx+xeOMrErKaJ+znQem+y2c6FPQe2vcc9o+ewotZFoSwz5TBh0Ytn4LzXJxlIfgZBDHYd5R0SDmGLLLInztKn8KM3lyCKhJ5IqqYgvFfcKkC3Jk+AzRg84gDKTXgo0CZFwkMUvsRkh3ta5NtPsTEArNkBOy1m2h+af4Y0ZTd1iziyey\/QkttYk8Umuicplgl3aB1hvr3iVK1gdT\/aDlnaB8mQnVz30\/Vjz30WXFUCeY3TCGoqx693it8ffM063j+ipA0osErZG8xJPp4gOmHFpE5vDY1K+tsCF27LZrdJ8jS8VKe1FpHI+dsUYGKbMDBcTp8BomVfkRzrOQuzjegD1Hz1KI0bt9aSb\/engYQYUvWR5LAcsFFyE8EKje7s8y1Sv3qnScQY7F4xaDgMH9qAQV8qsMeotY35XUif+4k9UZeUAZhfU7wnoDZTc+PqKCnbG7q6dhytaw7HNJTlh1G1GzmQ+ZDHdo+F\/OWePwhRuZQwiJfRsBP55IXuKROzXKqMirughe21g\/mJhBTs503yVG+kV8tFlvm5gdk9fbS64oK88MooqK2E8xb2uGWO4229FAJu8U2CLkYNpfdimfnYpnwLm1O2LXZJgHmnc1d8\/2Z5QfKgxzisbWNh3eCPpZZsPCZB8OY34w89No5pjt7SfWe0dpBeMTr81BU0vFVuRS67JCtJUBzHiCb+Ou0WGJ+luh27xNvSuqIXuFdJiw9uHu5kXbPHI9Y4ChTqAo14AeJMvhkMCB+TpCMuGbfynItmZCDdWHUgRxxLL5nL3UbWSdwvJnveKlniBLOylgOf+ctJgqD9Kqiz8v\/Visav6CsW\/HMh4CLst4Hzmta67\/OWTgDk8S8W+zkcC53MP01frasUAm7xTYIuRg2l92KZ+dimfAubU7YtdkmAeadzV3z\/ZnlB8qDHOKxtY2Hd4I+llmw8JkHw5jfjDz02jmmO3tJ9Z7R2kF4xOvzUFTS8VW5FLrskK0lQHMeIJv467RYYn6W6HbvE29K6ohe4V0mLD24eywSciewykwx1rk7bgkUImzo9hwDn+pp5zyjGR\/IaMn5F2iZ1m+zT15ZD50zw6jo\/i66egdMDO8TiBLE3XXU9QQN\/fc7cJ5Y\/0vDlSw50v9ebH3icITtoEi6ZfF80K9ow8td4Gqs+VLJv2OXTteQDCHr\/396t1cRUpRldhlDdfa+\/eKrlMjlzamFQOwJeBGGXJLqh6YJfUswlrSNIYSw50U2MqrTEQpGN2\/ajYVI1saxTeCMjDZJJEMy845lMp8Uc\/hJYHkBT6IzkaYkevF\/h2JUwJmS0stuD9n96g6kQFx6QGzr0g13ZBQLpcZ\/Qd8aNo1gLuaoBtD3kdD4syHr4+f23jcOVlUaor0uc6eppDnNzY3qfzE9sXYo5EC9QJIZM7j+3\/Cp1x5cNr55BsOT1ljBmMhvIjmkn+hCQD5xEc3Zgtj0VKTDJtB9l7g\/xophbncDbeVoTERZUDIDkSR5roBAEGm7i7NQ\/ta8quNFjpdjGJoaEeZ8Tegz7ALFgeD7iWH3L91Skb\/xyonHDkLfjd1QhmU7h0OjaRsY9PbU\/PfxTiQkOoxr+LjAp+B1aI2TKHj2ghgx2X7OhpJXEUzoLwqQhyKuTygc8q7pvRnR87nsxtX+ItZ1JPv0\/ZFBgjzyUier4nZH7fy7CyGo5opyK959qTuWyiylpDFCES8CiwJrECdFNgGQd+s2pz+H5PWVrMpdS4p2VNRAifqE8ZmFnOEjbZUhec0Mk+O5D\/4kcAbnWdcmnn3fL55fU+tVvFZGYGx4byNiy+mJmgWovJgzF8BRol3I0xfOiaeE2gTBYiuA+z1nEkOdYgcWw4uD0bYtRKcvL243hQktlfCH5FhlvX5n9EaNviflu979mMSFeZJKYHnsM1Hv8uN\/RX7pykiivUpwpl6Pgy84trJ7xCvTo6tF\/nnZquc5GyFBYogo\/WslIXSaGSH9z4mmujIa5FGnifii1Cp7XrylZwpixWD20RqZH+Tgb3djAMglhSlzuNMuY5tHb5im1\/hGUdGnRfkQR2R2lgrwUd3\/hjJXaBN\/az8VaqqbPsY2bGaupy8SKKNSmLSGSpjhMusJVE\/ekvBhSwlTCFIc1U6WZsiXwqskbc4MFAKES\/7+179tqyY4S0wJHveiB5IQjyOzd+advkzc1bP7bRCdzDQJVSZSYX4DdCtaOpfKmS0AM+GL4z90DgSSsPVbUajFtUrUV+GYjLs1kZ4zhVHFPBWErjuPvMk00DZx532dkGeQcLev4bDpNKgQWNvN+S+M2f5QLpmiXnS5R4ABI4xBMV9OS7tMoX3+IaAHDCNacTTj4PWieHGTiHE5PEiXMlH4WLt39lGjMdXhMCEW1ztUYAJAnzYHTZpfpZf3ZNVpJnuj3L83BA8aTY+dbbFjlNtxcojX3H5tkrNvTY3CoxLAJkU2Wb3w9G9Fh\/jb+Y80iGj8AaMKFsVGMJEudkzBYQ+KAfHtoIRUmbZMy3kkqfWAmmpOtgmLmv6WnfwF19V3ACUUsFzhdAAG+P3Q1o9Ti37BlKKENp11QthPYkDgQZxv9t7YxMy0vc4tdtDuZqiusRF5z45gvXIbLteUi3gP0qJzYGOuRWIxq3DvN2lzUVQrXhnT5Kh5yCAlRUEnWcc4\/n+qS\/RdR2kMF2XdDvBE\/oEnUOsfUSB65RHjGjksCKUhcoMbyBxIP+GJwHNrE\/Srlhz+SilTdzFDHkkxh3\/\/b\/oCsmsIcN0J3KjXg8HdxnF16mjQFNlLWGJQ8cXf4tn80JNnu1xtP+hmHmj9dynKxRJgyp1GXKrVKw27s9ctRbhj7Y+QXf+jZ0VLfIq4JaUj8TcYwSeqWQQqEUeBR8LKcLDfPrDH2NCHY68x4PZuUQruXsBRfYmsPRpts7ECvvGjaSJ5ORsYsS0rvK\/cI0hGdpSDtNhDpKE7+Pda5Cf+XC2gMsE\/5IFhhcnTDF8Jyu3WByjB0phpjeUdMR74pwuo67aJZoRaTUfbec9lA5kxeWf4vXaSTBtLfBSBBQk0z1nHmO81m1Dy++IybOdbnbuotQgtLEdZpScYFlGVmCEQVj+VWJkt6iBSPHHQjn9wJ7wn6cKzDaSBFLJd9+uMijX1Uik2ra7UspoEfrQSeRdomdZvs09eWQ+dM8Oo6P1HYz4VHhG0gFWKOaeYeZPUU+CdDtUG3BRWFKMrEIxj8GJ+bwqmeYLxeQkmN6StfNWPkcZtPl\/S3CEe2ShU4UobNoENIZfLR5NIB19msGzkgFAJu8U2CLkYNpfdimfnYpnwLm1O2LXZJgHmnc1d8\/2Z5QfKgxzisbWNh3eCPpZZsPCZB8OY34w89No5pjt7SfWe0dpBeMTr81BU0vFVuRS67JCtJUBzHiCb+Ou0WGJ+luh27xNvSuqIXuFdJiw9uHs7deUMmH6Jy4Xp7zU0comGLriySD\/XTEwvaZXmaAPtZvNAHe3fWMM4K30\/a6iRsitv\/dloCzOcareT\/ixSCjNeO2pJEGfsjprhLMIJ54nEX2oGSzjUL71Z4HUIrNbqvvFg9EY88Q1o9JEqKWlt+x4J2VPHZ7qSJY7z+ZCfiBwL+qfvHxKN8zUzwgmKnMJR9SybZWWuXqSfT1deQvNqZ3pLHdsu9KGYkyV7RNwSXcmYIYr\/XC4O3PqG189kVS2JMiaVjJ6BlruHH0GGY\/mH7PbNOyCTZ\/a1\/dxt3BDEPKqp4z2qjAgk5YGc1erwog0ZLbYRDSceaBPoS1GX+WFSyjceApJ5D+l8oLnhIAgKoENs0GOuVWuUlVTWwWUIa4h9n+LfJtOEIYtNbWb1ioFewnnbJYvYyhRp4mZYt8RkgII5e4BOg+MiC0PGn8\/5zNJkLxibJWUAQgXIo+Lnhux\/iRx9w8U4CHFrftzuSUAEQ6O31RZ34hvlPDRsdct73HhhWMDBbzrT0\/9KKupD0C\/z6IAUPISy8nvahi7TTnVc7Ydze\/RvLe8v\/2ntVyRQt587OKG+LBJhGig86rPPMx0T28O426k2xha9COofme5W7cANyIYmmJ7qmFXDbo\/6L1QvcwPN\/zUt0eZXkGlu8FjRpuYBoJIjvkGnWQKppZEyH\/KD+Epo8NJN3w5IIre5MX0i8dEustCMno\/DgR7\/Gza4m5R2RfMWBmdJPkcv3NnytmS75CNPo6OKnz3wV0xxqVWiTJLVdPN8HV7IKKdysNvDXq\/IXI+a+PAJMGUE9Hmv1lu1CPCE2BOuHLfpSpIGx6UH5Kkd3\/jU+gZdHR5PoGPz2IavL2zupL1UxYscu5Nx9YkwoIFzy7DnARaVjQUP1BCbgWm+o7Em3fbcDa8HD5ID5hQtBN6bYYLaSSBtFLY6TtWZ8VCGZTuHQ6NpGxj09tT89\/FOJCQ6jGv4uMCn4HVojZMoePaCGDHZfs6GklcRTOgvCpCHIq5PKBzyrum9GdHzue0nWcc4\/n+qS\/RdR2kMF2Xe\/N4TTYW8PBhwhoMAK9Ok68tSdFqw+3vTGWdWNf2lrOotXhVt5bCJ0GF8JykooMDTNkT20v6\/nd2HbKUvVAx1nW0Nyia4n9y7LrNjzZKWVHJ\/+QzCoiNyUOTBNE38UpfoZjU99GJGhldtqXBrYecWOJVd6Y4ZyJZYGxvBBZSAzd\/k0GAPcrRZaH4ZzCuoDhVIW7n4a+\/2VGj3H4sBIWE62b+JMy+q8dHAgZU684tPzMcfsXjjKxKymifs50HpvstkM3tGYBWqUeQsAa+pWsK5CHj2ghgx2X7OhpJXEUzoLwt5bHyBXqvRZgH\/t9n\/FPdmYFLkt8+U5y381cho6lSxMbVuwijhmcu+XqFKVVT5Uc13KcrFEmDKnUZcqtUrDbuyhyKBIaYdPHSwRh\/+Lwo\/NvV1DVp+gP3I66nTd56+lLUQvqsN78WbIcrQVBOiw3vfhNfOu4DNUs1fwv0jw9ebb2e2YSZlwnmQayxyZ22yx0Yr3QgM240WR0UElpKQW+I2nGgzyEm7p+acxQfPKjNaWO3Up4\/nvfk2JZ+Jjwu87+SyTkKARccuz7eponZlo\/HHgIFHvEul8AgOzEO50q3SkllWcBEgfchoCJQg1pLxJPBvG9U3so0gDBvnvKm893GDJR6JIvPIF9NjcAULP68+PtEWWc3SH87S+GOWulAN3EI0VcDdSa71Ip\/ZUk3dB6NreqUTj9hRZ7Vx\/\/G\/kaKoQIoZjtsQZLCqR4ViCcMbFYhuQtoncR07agaS4uQScHDrDpyGutuYG+0HHND9Mk6XyL73eGSBreBnuNWTaTij0IqmkrQWyX7a1bQO8DzHltHWJq21B58TzeuilUAXuocCV8ikoXnm8+Dh5LjSkBlPqgHwLm1O2LXZJgHmnc1d8\/2Z5QfKgxzisbWNh3eCPpZZsPCZB8OY34w89No5pjt7SfWe0dpBeMTr81BU0vFVuRS6ACxTPsSd54RwOL3m2aK7EPJrFt99jiwkwwiPDEU4ttR80qKMeyXGYTeYsJk+1RCvial87ODPjs4S+uvJMrLzotC1XWV0bfCx1nFbGRI8fstv\/dloCzOcareT\/ixSCjNfCvHklqblvWFDB+T1sjPUjaBCASATp6bsKa\/\/1Ah+nQuCCajKllYGi6rkGZkBpgiQPesiV8a8S9uFEPY7iqk0APjCW34\/GNNSIAFmufe4AQtn\/rSu+sbXV6kJws22Lehe8VKe1FpHI+dsUYGKbMDBcTp8BomVfkRzrOQuzjegD1Hz1KI0bt9aSb\/engYQYUvWR5LAcsFFyE8EKje7s8y1SKcLqOu2iWaEWk1H23nPZQChciAa8LMrSkTZyuZOu4KARUMB3pwkEHz0sFqdMkvKA9DffNys11QN6qRmzCvqji6XXUfXjqBUAEnW5EazbvF+R19c6hKxgreaIifdmD\/Tl6\/gVdNcgGnrYMjVl6u2Uo8ZG8BQgiL0xrMT543313BfxKxQ9Oce3qxgt270Irl8CfZ6lsuqBwBSwgwA65EJwnFVW3aMBa9i1Vt7Rq\/XMpMIRzkXOXSs6TRWBtyGDuQL6ghUVCN6q2D59qTwRSOLTDmY2iftCvKxv\/eC+Y9dN1JkdZVCBffcQdi44EOU97eNXJ4f53ebqXj+WBtRuD3+388JDFL7EZId7WuTbT7ExAKxgXbuaoif9sCvRBcLXmzqJCjMJXSffU\/G\/MsBc+MIq46KoOZstgAN3oOiEg5nD\/FeM\/IwtlDgvB0e1Oin6jYf74\/DsQ6FLv0hTXlLrkGBAp7pi1DIPnuyVfynIZ+3l\/k46Uta+NwISvVfNqhqBmHWCfAubU7YtdkmAeadzV3z\/ZiqXZ5ore4sdhKtv48pLG6ijGuZBon0eE5NbP6IvgA62Z7R2kF4xOvzUFTS8VW5FLika\/Y87+Mi54NlN0BogEZPyZNksq+Qq6UtJufhiUaLunPJ9NDYK6uEg\/nYLiyZwu8XqN8KRs5X+2NTZjLdUN\/ftS5RB3x8AtkJQc8lKHuuMrmSKUDVlrZrgPkhaubDIqplBzlwd3YJfNEVYb1MGlIeFP63pJHvh3q4N0R6\/6hbzjmCQMIKWQPHAfYnYjVEZGTukKu6JuSsuseXQzxNEerSbrneqZzx2SXSNIWytwtPY\/3\/QS1oMfPlO6Bd9rZmcIYewJ2204ueMnIPdKnrApuHA\/ahCAM9zgaiclCzw2P1CvFSntRaRyPnbFGBimzAwXE6fAaJlX5Ec6zkLs43oA9R89SiNG7fWkm\/3p4GEGFL1keSwHLBRchPBCo3u7PMtUinC6jrtolmhFpNR9t5z2UAoXIgGvCzK0pE2crmTruCgjkqnILCW1EkBsR8zP4UjAFDKzZ05VhQ3P3FNQCLdMZKBzoyVMOcmPce7e5yvtZdga99kzetCfv9zjSy9lgqQ4HgLlBegv9y0MFye9aDWCGYu8Y3ThZpMDt8peIwzczhLJsnmKI3Rj32ANRwdwsChfqzM0mIMOuiys6\/T6HdFJGRNhTrsSdNprCBq2V2ZmFZFoAdEYft+ID0Tqu+UukKRKFCDyhPjekmyIR5aLSiD6LJ16pAfprkfCLEBB4O3nRpfC14YUa4JGJJ+lFilLvtEDDt1KeP5735NiWfiY8LvO\/mACxTPsSd54RwOL3m2aK7Eb+dEe5mpB\/D4TOv+gLriCpZVnARIH3IaAiUINaS8STxv4kzL6rx0cCBlTrzi0\/MxIdYDqBZ3PP4N8tTEEB\/dBag4AGgECZD41oG3+6DWmCn2vyQ768\/4VQdi\/jQw4oSfQTbsl469g57yX\/VmdSR7XiKxXnpQZVqOdMhsSa9S97r7R061SlPXlcZVDOcG8UY\/mMxEyNnLrsRjKNmDXDdFGjXxIT2D94s+n3guY4iofkME+35af5Iil+nztZ7sVsRxZ6iMvQEzWqq3eEKOEqZBtjFxEN3XtciAcGM1gWyKkmQ7dSnj+e9+TYln4mPC7zv5gAsUz7EneeEcDi95tmiuxG\/nRHuZqQfw+Ezr\/oC64gqWVZwESB9yGgIlCDWkvEk8b+JMy+q8dHAgZU684tPzMSHWA6gWdzz+DfLUxBAf3QXdea\/b9zgKbwJP8CC\/HY+mMRxu6T28EszDrTUezeGwLEjbZUhec0Mk+O5D\/4kcAbkxpgNLXTOZUUHfSHtBdXgWCg+UqO227NQ2EfGCsVY5H\/N\/zUt0eZXkGlu8FjRpuYBoJIjvkGnWQKppZEyH\/KD+Epo8NJN3w5IIre5MX0i8dEustCMno\/DgR7\/Gza4m5R0edlUKkcKXQLTHiKoEeGH\/GVPKsP32Ax+fqtpFTT3+RLCbZyY2uDWmL\/kTdjzSCsVXUjFNiiJw+FgRAcjRElT7yL\/0MU30xpfF46+5j2ynM0jbZUhec0Mk+O5D\/4kcAbmrtUpDUq\/IDUh1l9D4egWLLYBiuE9gco9AVTTE10lTubHHELTE1MfHNvFKFQQrLALkFw3CqQg0wVPcPeko8AGxKHKUkl0nkGS73NWjc0FZKSS6oemCX1LMJa0jSGEsOdFNjKq0xEKRjdv2o2FSNbGsU3gjIw2SSRDMvOOZTKfFHP4SWB5AU+iM5GmJHrxf4dhVVt2jAWvYtVbe0av1zKTCtqnKi28NRHVpuP6lM+3P\/6W6KmR45rNrkKKn+KuiKQBo5qwO1eGL2vtmY3yM+al\/SNtlSF5zQyT47kP\/iRwBuSlrXaUC5mpI24FpYGMUw8pftM7RJup6keDfHRtMNtcBe9Yy2RqBFMrnZzbyKY6\/N7TlMy3Su4jkEeJnQzZ42LzgNpk5hri0dA6jf6TZ1es9\/0QMSLJorOfhqlzqQnm6432epbLqgcAUsIMAOuRCcJxVVt2jAWvYtVbe0av1zKTCEc5Fzl0rOk0Vgbchg7kC+oIVFQjeqtg+fak8EUji0w5mNon7Qrysb\/3gvmPXTdSZjm2TebrXiSUgHWv8fev7wCPcpLbqyNtNnzlvl6Urx5uT0BKDgY2fxpwUV6tpcT4SkdfXOoSsYK3miIn3Zg\/05T8EmKuX0v7FxxkPQptNc0mGjvSAEJfBRgswJDCVquatztOol5NUR9vG2hn1E4g2kaQinXKfLJZrNP1X82ksmXLXd0BOImPwDC6VCHTEcy+rpaipawmwgBBsyyRK\/pqM3N\/ZTqXNSdsJzW4+lRBuJnrzf81LdHmV5BpbvBY0abmAaCSI75Bp1kCqaWRMh\/yg\/hKaPDSTd8OSCK3uTF9IvHRLrLQjJ6Pw4Ee\/xs2uJuUdHnZVCpHCl0C0x4iqBHhh\/xlTyrD99gMfn6raRU09\/kTMTK+qNnODCtlWiIy7KtJfppgalp7iixTQ0evSUvN0P13KcrFEmDKnUZcqtUrDbuyEvh2toQ9UszCk3xGmCYiXbK\/q4v0pC54mhOq+DQuEe5ir5UcVTqBlK\/dUulVuuH9UIZlO4dDo2kbGPT21Pz38U4kJDqMa\/i4wKfgdWiNkyh49oIYMdl+zoaSVxFM6C8KkIcirk8oHPKu6b0Z0fO57uxJJZvi+uXro\/+a2XLNjfnLoBM9HTGtmqqulvhmxn+ovuwwDz4Aq8\/FVcGKbKUIbBhHRWQa468jEKLpV2JTVYxdgUBjWMAJuzj9sgfjP2sNXk0QNaAyIaH6DmvydrzXCGXO\/jMtwtMaYBT50yxkBgY2inoQtEY4yA5JuxR1Md8hjZND1JzOF6xiDkaSOnF37u6rLMynqIkjKpeLclIDUDvN\/zUt0eZXkGlu8FjRpuYBoJIjvkGnWQKppZEyH\/KD+Epo8NJN3w5IIre5MX0i8dEustCMno\/DgR7\/Gza4m5R0edlUKkcKXQLTHiKoEeGH\/GVPKsP32Ax+fqtpFTT3+RF0W3mcT8WUgYu3ZoXDkqn9PaCbzp1vQTi9QxWq96Lm5V\/QfAcFaJshzxXmM3CVcJxrSETWlyqa9nHSiISopjBM6lIq4q6jBb2U28vNV7FbirYl0na9ZvYIViRxALcu0r6HR9Ak0VOFgh\/+V\/xQr6Uyc\/Td03fDr37u0qQVT5tlrDrUndNTHkBVNatb\/n9LlLjl8pZP1JC51f9yenDdISSpeXC\/S37wunC87jJHiSuOA7FqDHTB0U86gLswfyNkraNACgYrQRtHdZyZTz6+ulNsW7n4a+\/2VGj3H4sBIWE62KmmDduMqiuNawvra+3MWyeqnPrfLPO7qMfXxCyg\/FSnxUqn+If\/pnMvcaWZCeoXUeWQa80J8lbYMYllyXXTB+cBO8Miz84EEVFeY4lneuGOxWEJr4nFlyZ9goMdskLjrRdomdZvs09eWQ+dM8Oo6PyoctQ36e\/gw9Oep8qXfPEaDmFcV7ZD3LOd9ODxVXTsYj6pDU5iwqETxa1rFYhSdv8MYq7f+8MekIDjjOMWAPJF+ULml1OKTX8KAcErpcIi7a44Pbzl\/z+L9Y6dwovPA57862GyRdAOO7N2w5nt3FWf\/RAxIsmis5+GqXOpCebrjfZ6lsuqBwBSwgwA65EJwnFVW3aMBa9i1Vt7Rq\/XMpMIRzkXOXSs6TRWBtyGDuQL6ghUVCN6q2D59qTwRSOLTDmY2iftCvKxv\/eC+Y9dN1JmnvEwEMlwNJfrDsHUQAflPumHkOCNFUjQrqE587tVYqfAyzJEUgBHp7zJAMsSPmTKR19c6hKxgreaIifdmD\/TllRb3odTsl7s1WsnwNSVmuRIEejm3YaNMBUda+RTPlTcuqieTtesr\/CdtNldBXf0T+qbI6XPMVFNcABURDivLLGR601CYXGUmprhtzRbQJwYi7UlnUeGICcK88UyFSHaNkbyhjlr0s3HEh7\/qed672SDbf10rvqeDS21urtd1DG8MScg8KGR7zJV4X4FgeIQqfAubU7YtdkmAeadzV3z\/ZiqXZ5ore4sdhKtv48pLG6ijGuZBon0eE5NbP6IvgA62Z7R2kF4xOvzUFTS8VW5FLika\/Y87+Mi54NlN0BogEZPyZNksq+Qq6UtJufhiUaLuywXmZRO3mhvra\/Bs3neUwc6+v1nEtG0BC1TQKxxtfLdI22VIXnNDJPjuQ\/+JHAG5kWJj\/kF8SqxaK\/Y9JhkS8WoUsAFptPVqW64ZleBw34pF5xoBvZQ45RgmedwpNidK8\/XQ6NgdyVBHYuQNrCe76pgeewzUe\/y439FfunKSKK9SnCmXo+DLzi2snvEK9Ojq0X+edmq5zkbIUFiiCj9ayUhdJoZIf3Piaa6MhrkUaeJNjKq0xEKRjdv2o2FSNbGsI4EDB3Lx51CC6FMKIFEMxyIX\/0CxH+T+7rDY72BIq9p4NxTp6l\/9QbhWWDoIYn\/0us79itS4MT\/3c+BWM6T34zCIl9GwE\/nkhe4pE7NcqozrkD7dptNfAZvoNe+qEaKFcvmImKdJDudKI4Ui655DEkgz9GuQz6dmCmV\/OkzScSDfz7ZNWjWIC7op3tUdxM7QoGozjAOdniim293Q0Qh5m0aCPpSygr4UXeYh2ad3wlfvi2ogca6+jzVHdEevHEjZuO1Y8S9JDg8yGbAnvwfCxuQr7WT\/BO7UUIRvAzqZFgaJDs2MxyD20eob+5VyCcCAHnZVCpHCl0C0x4iqBHhh\/9+q6diPRD3YHW6M50ZDnnz12OAH+sOFYv+RKc4deWsmXUbxwKcb0B8i4Ebv6YrVimyCGYg9B3xKMTrxU+9J0C8JcGUlmvRkOQmC8hf5N10N7xQI\/2iCS0Fd37z7txsPu82ZNOerf419kOfYlm2yJfPjLGKGcLWAfhOqszwdwno0i0MiPXGKgwGLgE4VpG+\/Hf6w3AAC6EeNaiQlB9MKhfu7gVaaqs2fLTR\/IE1RigTkw0k06VHyTJV5i2xjA8t6yPTnE9WbxyoWwp+GmOxzDGJWe3KKs9di+8mb93wgJftSqsJBGr+16qmyq1cStrg6aEJcSCjM1sCmJfqkRO9vdfp8C5tTti12SYB5p3NXfP9mKpdnmit7ix2Eq2\/jyksbqKMa5kGifR4Tk1s\/oi+ADrZntHaQXjE6\/NQVNLxVbkUuKRr9jzv4yLng2U3QGiARk\/Jk2Syr5CrpS0m5+GJRou4q+71V19LTk\/4KVk6A3hr6riTSj7ymGLKVh5BvpXsAgO1LlEHfHwC2QlBzyUoe64xv4bPx3dqRTyevQxrO\/wozD2NRd4TvfDnn2da43hlijzv7y6eQFlAIp4UAtDOI3\/7dqkkZJleQzN3qObe3MvvJG0Bk0IzeufIcerDkcnmNXJn6BAy1WGVzfQbsXMEt4nyAaxYVqRpguDo30FrBzqIo8X0\/SbaND7RLNAjSpgYD5UNZIZRA1whB+7JOyDLP9dWced9nZBnkHC3r+Gw6TSoEFjbzfkvjNn+UC6Zol50uUeAASOMQTFfTku7TKF9\/iGjJJ3xPofqxw6kLDNmI8wA6zR8dxl+LyPvsyEk3Ux+W7QPmmMA34H8bysOuIjWNra02JVYc2fHFr14ngLi7I5ilUOz3ClQiunUOKAoUUnrAZN6pROP2FFntXH\/8b+RoqhCAPevOV30aeOIfvRSsUC8rz8nBnLv\/jANWyN02qF4It7eF77JZs+TQ24sUQ0pfxQZl2b163yqgTI7w3eVkgus\/YlZx22MDk1tRzsAQW0WAr\/ERrtPEcJ4WWEP6DvitNdgkuqHpgl9SzCWtI0hhLDnRTYyqtMRCkY3b9qNhUjWxrFN4IyMNkkkQzLzjmUynxRz+ElgeQFPojORpiR68X+HYlTAmZLSy24P2f3qDqRAXHpAbOvSDXdkFAulxn9B3xo3lGYsi0\/AzVQDb9zNeQd6qI8+1d5p2S35ueyGjxtHvp0XaJnWb7NPXlkPnTPDqOj9lIOggBZW36xljopuhoy6KkI7qotEYhVdnRqiczS3ouX\/5bo62vcJ6Ly0ehhA2\/z7XQmYFKP26S6IHj\/LiqTFKGbGVsCNqeTSXFgbv4CmqJeEnKqqz8givg3YxK\/8FO+zR0MqHJxBfr+20opjmELlV8VG9RZtcyBqVO6sqE2X4v2cBB7Xg8xVDKr8Kk6MYIBdp+xHIOpNGJD3erOflcp6V4LtzwSWAmYTwIAQ2MfmS1dpc1FUK14Z0+SoecggJUVBJ1nHOP5\/qkv0XUdpDBdl3Q7wRP6BJ1DrH1EgeuUR4xo5LAilIXKDG8gcSD\/hicBzaxP0q5Yc\/kopU3cxQx5JMYd\/\/2\/6ArJrCHDdCdyo14GeVTrbR6OQt81Cz3yx9okjJsFCl9frtXMEHZjbJXVvSt8kvfTfUm2cjrr6CAaFJeqYtIZKmOEy6wlUT96S8GFK5bSI3GuoOz7OdUy9T3Z95zuIuYvoEy+CbF9rXYQNI2lZ\/1Ao26KiTbSZ8hECxQBVPBXykwk4Eg\/Vvr36Q0RtZpK8A6Wlkir4Mp\/cfjiEz8i9MNPuZnTyfzBkbfAXvYdxUIZlO4dDo2kbGPT21Pz38U4kJDqMa\/i4wKfgdWiNkyh49oIYMdl+zoaSVxFM6C8KkIcirk8oHPKu6b0Z0fO57MbV\/iLWdST79P2RQYI88lInq+J2R+38uwshqOaKciveK8kxHdLN2RmCfFBxvd8GOZ2AkF0X8B6ZVxKdXaiVhgGnxJ2ZzkvIVFVpk7fUQAFwIdv2P1vPkCKnVGJwyEWpgZugWvJm2LeivjSaF2QnotKf\/K\/VXFhihDjBIwyeUXJ3Pgs\/jfTIzV\/d5w6xE62gvAOHVPsVW7ysq+7F496n6jMHG1atCvDWfOt445TLy+KpGPhYrWpfvbC3MPbkkjM8RmB57DNR7\/Ljf0V+6cpIor1KcKZej4MvOLaye8Qr06OrRf552arnORshQWKIKP1rJSF0mhkh\/c+JproyGuRRp4n4otQqe168pWcKYsVg9tEamR\/k4G93YwDIJYUpc7jTL1jrdSDLXrhq4Hp25O6tkUcI5dtc+IKBpiIVCaYWBicPNmTTnq3+NfZDn2JZtsiXz5F91bSny9BcrnrtWCK0a31+IKkDdrDXLAtLTl3ib8djv2z1W0lPuFP10w3AVBn+dg5IqtROQaCIWE2m9DrCqyMzbRigsG6ahEoAlUzqrcLqDdpMqpz\/GHJecOblBgBn7O3Up4\/nvfk2JZ+Jjwu87+YALFM+xJ3nhHA4vebZorsRv50R7makH8PhM6\/6AuuIKllWcBEgfchoCJQg1pLxJPNS664RyBU90VVFI\/0XcfTdb6abmXzk7XOe6brrHTyml\/fBukKLImUUjD5SICF89FG0OVMbRhpV+m2RLcrwnC7KR19c6hKxgreaIifdmD\/TlG4AbNXRhP0Dx1tLqhUHgteVpY7UraLy9Akh8HUUR3c+20mBqWR\/n41eCG0Pk1\/KVVkcISFNFh99MtH7\/49ikZqPM\/qyHdBq7iiqsRmk4EFuRPcTzQLnHEYqtIGl6At1wDDTUKYLVU4694IuJYpGgc2nlAMVrsw6qOefn9O6Uu\/GYHnsM1Hv8uN\/RX7pykiivUpwpl6Pgy84trJ7xCvTo6tF\/nnZquc5GyFBYogo\/WslIXSaGSH9z4mmujIa5FGnifii1Cp7XrylZwpixWD20RqZH+Tgb3djAMglhSlzuNMt1iBgJe1YAsEzg5TByHPQTsn3QRaSPOzgnoaWG\/U1j3MJDFL7EZId7WuTbT7ExAKzju79hRud81nm5DzP5uJotm5GbGxU9RIlZrsEo7bCd9bAlz7JXPmkHUWgrr\/BVQNN+jDcVmG4e\/X+cGBGMGiDgU+WIcHB3OtbxHy3GsikqdAoBNruvKYu5UOS+JqVRLqkm2Vlrl6kn09XXkLzamd6SRcibfgF\/snT3qvnbP6lE35geewzUe\/y439FfunKSKK9SnCmXo+DLzi2snvEK9Ojq0X+edmq5zkbIUFiiCj9ayUhdJoZIf3Piaa6MhrkUaeJ+KLUKntevKVnCmLFYPbRGpkf5OBvd2MAyCWFKXO40yxY5zQ+RWwAr70bYpSZJFXmdRMt5aU5pXQB9VgMtyWmZSCzC3qrUp3Ah9W3rNdYCqZHX1zqErGCt5oiJ92YP9OXUl+D3m1bJ1rGAxUPxPtjyXa8G605v9ICtMIDbt4i214UT3eS019XYzJEr+ogHoV5NCr8tLdPP7WJzArzNeQUu1DnhAO6O+BUJo9wjCoLTgyRP+QDoUxz9S0aYUuDwxhE3SqF9yp7b9yh4Z8ZbDK5kyu25hnm5Wjw\/b7OGfMQc3jt1KeP5735NiWfiY8LvO\/mACxTPsSd54RwOL3m2aK7Eb+dEe5mpB\/D4TOv+gLriCpZVnARIH3IaAiUINaS8STzUuuuEcgVPdFVRSP9F3H03W+mm5l85O1znum66x08ppVplAecGoFSgQ9o9OO8D40C7MdSdHD6vkEvgDVvUfwIykeZEsn5ZUI2Y8EwjsuGxkgh2\/Y\/W8+QIqdUYnDIRamDHQOH0EczJKBD8BpMV8SuOQztSwOk\/pqQF5602pKWiAK5I2pSBRU00zEmzcbARShpHxGSax0oHfaplBmgFsfod\/rTrBgGuwmnXYBnABS+HD0lgJBjnzwYNlgaxnW+1ZiLY\/R+kAcLK3SGLlgA3efztiQ7NjMcg9tHqG\/uVcgnAgB52VQqRwpdAtMeIqgR4Yf\/fqunYj0Q92B1ujOdGQ5584VNBhYMZ0L2yfNBFObrfS\/1zl0zjifDl\/QrUqVwoup6\/njSQWmubqKBDtLr8lFLDvu4h5AQSZUdzvVCrILY5ybtCZNq4+gqK+Sz+T4r1wNoQeNDqBBqhUOQzkNi4zzhqFqP1LGD4ccidxyquXd+aKvtpKuIl0+GpoNbHGFlBZaN1wMtkHxGmRSkFrA53nQL6qlkhwg0r55yoPlFsRsFbtwGqFZuJtAWY+5Wf\/Au9eAqN3cIjE6ZCOT+HRifPpX9MOnB1GNgh67aa6B\/C6A7Cba4G4iqF454+zpEjiGaXVE02Z\/VxO7oy\/yy4JrFzyw\/1DxibsrbUBCNGaVq7btZ4ZEjXW3E8tdhkmySic43hIrKa5GoFa1iAYt3i+SZdnrYPYM1UELXIW0LaqUiTRB7axNY05DWSHLiM7VzlazvNWOwRlRcsY0y73gZQdZ\/17OS0sa3ebMtM+5sWjQWOWtSHPp0nAzrt7jdGBOqK5Ozo7y3DTCDHnq9zpWW0RKYbtR2N9cuBrRQwumPUR5QdZn5h9txBdLe9EYxt16fR20zSGZvGg8se89v0W7PW4kYDT2kCfOcU6Iie6yDvxx1MUvrcXMoI2CWz8eQh++2lzQcSvjlGKCLDn\/mmJ\/sJwSaZgO7HhAk2\/bPMjy5paBmYd3C9FwEfvafnyxP1NmgWJFxASyhPNW5I6gZ470rKZZ6shvXyIaW+vNELgy1+sh2DGJhtuLY5smAhqtvXzW7hL52giltp9B2J2E3yOMgeKiOce3A6oXS31TJJxpeSfrtyqMEiKLFlTIm6Q2FxUxS4G0\/FhQXBBURp7v5YgBAdNTEu5MF3DQcX54y\/nn3B9JZcEKaYySqS2Id7CEdYYov33DKVNk2ZP+FBYDAQSXxpzQ7MvMWcmMCFcIGf\/D9m7On4fsjG9MGwTsVTyD7wCKr2b4WaxCK7kkz\/\/tfclSA8QhQ8j9PTh2JqG9X41bGOOrqfN\/KPXp0daQeC+RE4wG575m5BGGMAuSyCzvut36FhkUq3FyCYw62YSfsNq9HOnmqynN26EjrbmDZNDhCrn\/3dvARjZDcmbr4vHDHu6hpbof+sCecBfoZtZhWQYWWNiFoEePPDrdzSPldJujNizoPURTBZFfWfXas5MCzV0bAdCvEsEUrk5OYUjPOiJMwSvWif1W5WcxTvJqM42NrM+h7khuZW3q47dSnj+e9+TYln4mPC7zv5VjiXBqPDqoy0G0lIJa\/5D9oyE9rx6ShSoNkSy1ku2NCWVZwESB9yGgIlCDWkvEk8G8b1TeyjSAMG+e8qbz3cYNqQ7adfuX7zuRuJyPR0bz4dwFpQk2i2GgFJSyo6\/TrtByTWjWde6me1V+6X\/3P\/BBIhwlHBSHy\/heBBiYBiFIBCrJcwsoxBKiRfQFFV7esTuPpRE4wpCJ\/gjdyAXlj2kRLhJIm\/p4NcfJtsRmNF\/Kuf4j6QZfUoMoP+pN9MhZHhS2+YeZJEpjQMB3Ty0t+hNKNREA8B7OzoLzP8qPB+6bGojDtnARIsoRmSDE\/751AYtN5WLn7Ke7O00g4PEYb2lxBOZ3OSn7yvH2D4b0TTHa8pKFcv8nZdb7oNLrcuyr6GeeBafLZgv6owHgFf7yPSifRplCuwl8QSmoQkwMJtcgy3kI\/PwhJ9MLGLlhG0fiTN3JAOY+sqYV3sxZc05mDbcokOzYzHIPbR6hv7lXIJwIBs8rcvq1Pp3ahlt2NuJpJ6WtueMJ5dvsCo+Zql6lhppBujM\/yBNTaZXEaForm307bAwy\/pgmI1AnyOHgyUbxjoiWXY80nvy5skYPGSYhoWPeCBdhNGb0Kdz31FAGn5MDmXXlh4kx7C8z9Rqz4\/GGcKYEYvOJVmRy216BkGaOsaTkY5F6MQuN1M89E2DfNNUy7mYssXlfR2yz4fio9Nu6r6ylX7HucKWX7Egv489y+hgdGgEQRVum6z48FlHgYjd8p\/cdfn1a4THprCpXG0N33OlpTLxc7MJziM\/vnuFEhI\/nwQ8Cw7111jzBX5wcKU7RAXtA8yotTA82Ss7f64jL+eZ\/IXhgZlyYiQqZSnaw4z0e\/vz+f+XPYuolvHglPqh3udXen2D8e65lmUUDrt6kLaP2vtO5NPn2ZkdftQeE9IZ9YeY\/bZlQRaajpJ8ZjI2rC8VKe1FpHI+dsUYGKbMDBcDKEMmO6HMp4lhq97dah3CuhS4Gzrg\/4qLsFmP2EiejmR5LAcsFFyE8EKje7s8y1SoYjxpMo4coI+ihQ0hSy6RsWSxzP3BeX20imWeeTcKoDL38Af3L4HpF9Y895kt2XhXoW01srLhLMQ03enoiCu0Qg7OA0dGteVhio7o07HuVmGXM7YkWyQruOSjoR9lJH6G+7OiTaDPY6mCI8sPiVcfthA9be73SNv6SiOdDQvayo0at6TV7aR6YzdYThIC6Id6BrZi3eJLKJnqMTR2faBEd7e8h6NDG6uQHMOK93VZZioqpL4agwtkTtdQmFRuLD9ChXhW6ICg09\/Sq13E6b3kJ4P5CB+noQ2JVEsiPYqpV1dD6T234Hpb5RXKHLnwQHkP+7oUe0M6q1XD\/c0jaWKzLK0cFvgGuoI9lqihG3ZL6l9nqWy6oHAFLCDADrkQnCckXELcVDNvM52FppITNqRZTmzbQR5SijbPAL8g8bOTyN8lwhRSMQiZJgq4Rk2ZpGzG2DTLmFD9AoUb8DUWJzW20mE7Xw3jtjXdCCEyXxi8XyrKaZTC71l6q\/WaCR+6AC5ZU\/6\/7tNKL0gqMV9qprikqYtIZKmOEy6wlUT96S8GFK4dj9kyXLryobksI7oEQOJ2Dz+RAaCNoelwZvRrOVAWNceZ9y7oN7T1sXsJSJ019iSWku2lCYcRWfyOaPmzWnWkGCsqDoHfKwbk7UkZ8aOGRrqn\/q1ZyncH7SnyqVIDrFsf+GtarFFdjvGtB51Z0dWCcQxgj73V14R0XjgmIGG2kMMbSi+52lhI0ZlJxOliFht0WAt3y9J+KdgvWoZFopUyW5wL89aFKwVQ9JH3tFOv\/EwCZOCxUrFblAsSpowSNhUIZlO4dDo2kbGPT21Pz38U4kJDqMa\/i4wKfgdWiNkyh49oIYMdl+zoaSVxFM6C8KkIcirk8oHPKu6b0Z0fO57SdZxzj+f6pL9F1HaQwXZd783hNNhbw8GHCGgwAr06TpeaB8w+azn27kSu+g8H6Kc1uqd36RDAUmQIWSWOU87W60rROAIjF\/hi2D5Ft5yUoH2KCW5GSSDpgwanZNVuGA19SyAQtnvHwoXmUp4hlQrE5z1csH9WCm3ZDxrGaEluBKGyICdiJef0PDKQwx6psEmoZqOwuUJrtG946Qw\/l2XLtJGzQUqgPHXOwZvYyzAMNu8VKe1FpHI+dsUYGKbMDBcTp8BomVfkRzrOQuzjegD1Hz1KI0bt9aSb\/engYQYUvWR5LAcsFFyE8EKje7s8y1SKcLqOu2iWaEWk1H23nPZQChciAa8LMrSkTZyuZOu4KCCOdCqn3iI9WMpdhbOOt0XUOGHncgZI6+3ElFAq9Ha2wbBXEbrewOvWWxhIA7hgeDNyA1ERyILp1Bea\/CzeSsHcQEdN+rlpgbY46yD58hDE19G4JrNH37+gi5IAXC6ZbQDKYY3+XSXiji5O5+0ndD614sYytyWxXl6SFolIMyPFe2B\/P3\/wsNc3hnLE7+okp6z3w\/laOZsEQSpXqDnL3W\/xgkgewGxL+EFMTwFOTI5Eh9eV3+uFm\/CGZO7yF9U5fY7dSnj+e9+TYln4mPC7zv5LJOQoBFxy7Pt6midmWj8ceAgUe8S6XwCA7MQ7nSrdKSWVZwESB9yGgIlCDWkvEk8G8b1TeyjSAMG+e8qbz3cYAKrQNr1SgTdnyXFxL41n3J6AyD17B5RglerVQXaPiGYwkMUvsRkh3ta5NtPsTEArB+t7fIXpg65yCKJxqyIYxbYF7ecCqNiH+ceoKhiIgGLvwH7c675TWYmhXNTzV6EKwu7B\/p2iGh8PTkGBc9n\/JkkIGctsd0phJto0NJCN5y\/6m+Q58IBoThc7mK6lZvD1czMnCTDeSL22VckGjsX72rZJs+ntdvnsxqZULzYpE8g3EF0t70RjG3Xp9HbTNIZm0S2q6Rx8cUld4Wn4GnRbJH7YENwlvC9R9tFOB0N\/PpXTeurSieWQZE1EZGtSRUYKEYoIsOf+aYn+wnBJpmA7seECTb9s8yPLmloGZh3cL0XCO1i3MGLyLNDLx1x+V6w4rI3p7Csyxd78FwIJD9PUcgv1zxvj3ZcAW\/CJUopa46CIrFeelBlWo50yGxJr1L3uh6GIJdBHDXSozjjGv+Prbv6ZzeqJtWGdKYGhjqQDuD7TqUkAWlQM\/zK1Zq6l7FkS4Ytc8VpUP0E6Ir37XDBVe9mEp7DIG4L+m0XfgYee9W4mi4W+MivZOF7Dtq4IEuOprEL4QD1k1eO9jDMBBuSe9912gDRi4KUMZdbyR8ZsoXqxvYfUqSmzOU9yEDJuOLaSYFAxjsHhaSD2yL+Y\/GY5xrcQXS3vRGMbden0dtM0hmbMe6HomXoM1kD9qn1CwE4zV1G8cCnG9AfIuBG7+mK1YqHIIVYPNKbsFl6bMJSOunG5b+Nw2\/9rx50ig7Q9iZnD\/+HTpAYRpyAGoMe\/IKdLruileCa3lZBB43j\/MH28J\/HU3zuyeGsDON86O\/1iFjlxd6CdP8lRgcxvhjqb6WzIKhI22VIXnNDJPjuQ\/+JHAG5rxJNFpO0fv0QzNVqws3GIuX5DNRCzeZNCsFXpxzj5GuZbYBO96cLXfg3w42wCEJA2VM+uN\/+oS9PALcZ3d4YOZ2DNNHb8oAtWjie2g2IJdu75sdP+49CcNYlQL20b0T383\/NS3R5leQaW7wWNGm5gGgkiO+QadZAqmlkTIf8oP4Smjw0k3fDkgit7kxfSLx0S6y0Iyej8OBHv8bNriblHZF8xYGZ0k+Ry\/c2fK2ZLvkI0+jo4qfPfBXTHGpVaJMkEe8WQtWu7EJuVXQGKlZXO2d03dN9UCOcwpBF9vJWXyFVa112GsbbFIJ4DDAvqY7gT2CgOyC4roWvFEV4YDghxIeNodt2H2RHxrf8nh+mAD6JtQ\/T4UP8FR3m74O5X6+sS7u0IsYX4N19RqY3tyIEn2DN\/6jWf3GHj6OyZi3NLLLj2j5uts+m8JHXt6ggBmm8eDHz1DtH\/MbryazbqyVv5pgeewzUe\/y439FfunKSKK9SnCmXo+DLzi2snvEK9Ojq0X+edmq5zkbIUFiiCj9ayUhdJoZIf3Piaa6MhrkUaeJ+KLUKntevKVnCmLFYPbRGzvdjlaJqiAwfQ9shSVAJrg==")