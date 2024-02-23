import base64
import hashlib
import json
import math
import os
import re
import time
from collections import OrderedDict
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
    def GetUpdateStrByTick(tick):
        now = int(time.time())
        day = (now - tick) // (24*3600)
        hour = (now - tick) // 3600
        minute = (now - tick) // 60
        second = (now - tick)

        from tools.str import Str
        if day > 0:
            return "{}".format(day) + Str.GetStr(Str.DayAgo)
        elif hour > 0:
            return "{}".format(hour) + Str.GetStr(Str.HourAgo)
        elif minute > 0:
            return "{}".format(minute) + Str.GetStr(Str.MinuteAgo)
        else:
            return "{}".format(second) + Str.GetStr(Str.SecondAgo)

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
    def GetLookScaleModel(category, w, h, mat="jpg"):
        data = ToolUtil.GetModelByIndex(Setting.LookNoise.value, Setting.LookScale.value, ToolUtil.GetLookModel(category), mat)
        # 放大倍数不能过大，如果图片超过4k了，QImage无法显示出来，bug
        if min(w, h) > 3000:
            data["scale"] = 1
        elif min(w, h) > 2000:
            data["scale"] = 1.5
        return data

    @staticmethod
    def GetDownloadScaleModel(w, h, mat):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        return ToolUtil.GetModelByIndex(Setting.DownloadNoise.value, Setting.DownloadScale.value, Setting.DownloadModel.value, mat)

    @staticmethod
    def GetAnimationFormat(data):
        try:
            from PIL import Image
            from io import BytesIO
            a = BytesIO(data)
            img = Image.open(a)

            format = ""
            if getattr(img, "is_animated", ""):
                format = img.format
            a.close()
            return format
        except Exception as es:
            Log.Error(es)
        return ""

    @staticmethod
    def GetPictureSize(data):
        if not data:
            return 0, 0, "jpg", False
        try:
            from PIL import Image
            from io import BytesIO
            a = BytesIO(data)
            img = Image.open(a)
            isAnima = getattr(img, "is_animated", False)
            if img.format == "PNG":
                mat = "png"
            elif img.format == "GIF":
                mat = "gif"
            elif img.format == "WEBP":
                mat = "webp"
            else:
                mat = "jpg"
            a.close()
            return img.width, img.height, mat, isAnima
        except Exception as es:
            Log.Error(es)
        return 0, 0, "jpg", False

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
            for mat in [".jpg", ".png", ".gif", ".webp", ".bmp", ".apng"]:
                path = filePath + mat
                if not os.path.isfile(path):
                    continue

                with open(path, "rb") as f:
                    data = f.read()
                    c.Refresh("LoadCache", path)
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

    @staticmethod
    def Escape(s):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
        s = s.replace('\n', '<br/>')
        s = s.replace('  ', '&nbsp;')
        s = s.replace(' ', '&emsp;')
        return s

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
            b.baseInfo.category.append(category)
        category = v.get("category_sub", {}).get("title")
        if category:
            b.baseInfo.category.append(category)
        return b

    @staticmethod
    def ParseBookList(rawList):
        data = []
        for v in rawList:
            data.append(ToolUtil.ParseBookInfo(v))
        return data

    # 解析首页结果
    @staticmethod
    def ParseIndex2(result):
        parseData = {}
        raw = json.loads(result)
        for v in raw:
            bookList = ToolUtil.ParseBookList(v.get("content", []))
            parseData[v.get("title")] = bookList

        return parseData

    # 解析最近更新
    @staticmethod
    def ParseLatest2(result):
        raw = json.loads(result)
        bookList = ToolUtil.ParseBookList(raw)
        return bookList

    @staticmethod
    def ParseFavoritesReq2(result):
        bookList = []
        from tools.book import FavoriteInfo
        f = FavoriteInfo()
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
    def ParseMsgReq2(result):
        raw = json.loads(result)
        status = raw.get("status")
        msg = raw.get("msg")
        if status == "ok":
            return Status.Ok, msg
        return Status.Error, msg

    @staticmethod
    def ParseLogin2(result):
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
    def ParseSearch2(result):
        raw = json.loads(result)
        total = int(raw.get("total"))
        bookList = ToolUtil.ParseBookList(raw.get("content", []))
        return total, bookList

    # 解析搜索结果
    @staticmethod
    def ParseCategory2(result):
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
        categoryTitle = OrderedDict()
        for v in raw.get("blocks", []):
            categoryTitle[v.get("title")] = v.get("content")
        return categoryList, categoryTitle

    # 解析搜索结果
    @staticmethod
    def ParseSearchCategory2(result):
        raw = json.loads(result)
        total = int(raw.get("total"))
        bookList = ToolUtil.ParseBookList(raw.get("content", []))
        return total, bookList

    @staticmethod
    def ParseBookInfo2(result):
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
                if v.get("name"):
                    epsInfo.title = "第{}话_{}".format(epsInfo.index+1, v.get("name"))
                else:
                    epsInfo.title = "第{}话".format(epsInfo.index+1)
                epsInfo.epsId = v.get('id')
                epsInfo.epsName = v.get("name")
                b.pageInfo.epsInfo[epsInfo.index] = epsInfo
        else:
            epsInfo = BookEps()
            epsInfo.title = "第1话"
            epsInfo.epsUrl = "/photo/{}".format(bookId)
            epsInfo.epsId = bookId
            b.pageInfo.epsInfo[0] = epsInfo
        return b, isFavorite

    @staticmethod
    def ParseBookEpsScramble(data):
        try:
            mo = re.search(r"(?<=var scramble_id = )\w+", data)
            return int(mo.group())
        except Exception as es:
            Log.Error(es)
            return 220980

    @staticmethod
    def ParseBookEpsInfo2(result):
        raw = json.loads(result)
        from tools.book import BookEps
        epsInfo = BookEps()
        epsInfo.epsId = raw.get("id")
        epsInfo.aid = raw.get("series_id")
        epsInfo.epsName = raw.get("name")
        for info in raw.get("series", []):
            if str(info.get("id")) == str(epsInfo.epsId):
                epsInfo.index = int(info.get("sort")) - 1
        allIds = []
        idMap = {}
        for name in raw.get("images", []):
            picId = re.search(r"\d+", name).group()
            allIds.append(int(picId) -1)
        for index, picId in enumerate(sorted(allIds)):
                idMap[picId] = index
        for name in raw.get("images", []):
            picId = re.search(r"\d+", name).group()
            index = idMap.get(int(picId)-1)
            epsInfo.pictureName[index] = name.split(".")[0]
            epsInfo.pictureUrl[index] = "/media/photos/{}/{}".format(epsInfo.epsId, name)
        return epsInfo

    @staticmethod
    def ParseBookComment(result):
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
    def ParseSendBookComment(result):
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
    def ParseHistoryReq2(result):
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
    #             info.baseInfo.coverUrl = GlobalConfig.Url.value + info.baseInfo.coverUrl
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
        elif epsId > 421926:
            string = str(epsId) + pictureName
            string = string.encode()
            string = hashlib.md5(string).hexdigest()
            num = ord(string[-1])
            num %= 8
            num = num * 2 + 2
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

    # 图片分割合成
    @staticmethod
    def SegmentationPictureToDisk(imgData, epsId, scramble_id, bookId, path, toFormat):
        num = ToolUtil.GetSegmentationNum(epsId, scramble_id, bookId)

        from PIL import Image
        from io import BytesIO
        src = BytesIO(imgData)
        srcImg = Image.open(src)
        if num <= 1:
            srcImg.save(path, toFormat)
            return

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

        # des = BytesIO()
        desImg.save(path, toFormat)
        # value = des.getvalue()
        # desImg.close()
        # des.close()

    @staticmethod
    def IsSameName(name1, name2):
        return Converter('zh-hans').convert(name1) == Converter('zh-hans').convert(name2)


    @staticmethod
    def GetPictureFormat(data):
        import imghdr
        mat = imghdr.what(None, data)
        if mat:
            return mat
        return "jpg"

    @staticmethod
    def GetStrMaxLen(str, maxLen=6):
        if len(str) > maxLen:
            return str[:maxLen] + "..."
        else:
            return str

    @staticmethod
    def GetRealUrl(url, path):
        if path:
            return url + "/static/" + path
        else:
            return url

    @staticmethod
    def GetRealPath(path, direction):
        if path:
            data = "{}/{}".format(direction, path)
            return data
        else:
            return path

    @staticmethod
    def GetMd5RealPath(path, direction):
        if path:
            a = hashlib.md5(path.encode("utf-8")).hexdigest()
            return "{}/{}.jpg".format(direction, a)
        else:
            return path

    @staticmethod
    def SaveFile(data, filePath):
        if not data:
            return
        if not filePath:
            return

        try:
            fileDir = os.path.dirname(filePath)

            if not os.path.isdir(fileDir):
                os.makedirs(fileDir)

            with open(filePath, "wb+") as f:
                f.write(data)

            Log.Debug("add chat cache, cachePath:{}".format(filePath))

        except Exception as es:
            Log.Error(es)


if __name__ == "__main__":
    from server import req
    reqs = req.GetLatestInfoReq2()

    Text = "wV60pmqKsG5SWYgofUhsBQVFHVvxowZJ+Hp3GooM8NoZsL8g9klKHgeiNlXqVw9IXviwHxceBOQCYmkLulZNYEk6G\/rdv5Zif644m6s1EAcbdTpia1PqD3kOuCV9ny6AjmWGitpopiHs6OD+PWVASX28VD33Vh0ngIC1L2HX+gGqeDGtB5jboRoNyodsZe21aWVFP9FwYRvCT\/iTivjUrZ40ByRad1nFfuxqn5OHkWq983jFtsIeUCnJTFBjWOGq5XMA7XmxHmz9OJKT2PR5E0gD+HHcihbGfzMeck\/RSJtwZmospTfJL\/\/WFGzR993VpSbXNLANgd1x1dlkVWp7swQhhewQM\/uVgBNIW\/HIWfB9vFQ991YdJ4CAtS9h1\/oBE3qSo+F5szfGb7iWpKINeSyHzlYWMZDCCcFfz0EHG5iE2SsxtVz7Mm+66Gz4zT30V9vW46V9L4NL+D+kuLq8++VzAO15sR5s\/TiSk9j0eRNIA\/hx3IoWxn8zHnJP0UibLLdWv0yHvy2VJm1bFinjaBrK1pG9BZc6VigqnRGY4nh6eOfPcq\/r61rtT82EdmNpfbxUPfdWHSeAgLUvYdf6ARN6kqPhebM3xm+4lqSiDXmq5h0gTnH\/3xhi\/dFtGzydwXzuoPWzF9knUNkagjG8UXYZRRDP2IcQOYvkGz7ef119vFQ991YdJ4CAtS9h1\/oB+OqsJhSzDRAaElXmoPbbJlWWD4v2Ak8bImrFw29qy3uc2DYJF3Tr7BOEx+9YzMUTFiMWl5PFnV1QfWXIpnj3wk3KfxMefHAjKD7nnsv8tNdSTlAgBpC8fN0XhSC15b7kuRVrutJMShlFEwOG5LMu57exmt5PLtON\/51Oc7GHuW72D8xT4FVV9\/Rm0zUAjTpHn9bG7C\/aFfT9GKCcoxJxsljEn8suqOayO0s1o8RmcDbqO9+sKf3y3qZCHjK4BCJMBG8nPlEsniGb1ixZVJ9yBzhYxJrSMVXtOKVcmDeHM4qObRVLIOqAq+3OHjQYjVstCl2n6Fj5O+VvRU35tJNUB3pa7THCoIHXj\/kvW+fvabkl9fNqJb\/\/dCklWVg\/KAXtBo1wq+G5R9wu7ZfE7fnW4Gm+m8oVTTC0UTAkeFga+bIgT95r2+3biocmK3MiiafE9k7e3c94Ne+fL8jeSTjewvbtLHglDAM2GGb1cDcALEvGyH+AtmsTbz+l6UqZifXEiABBK\/6zaBkSw\/AWZVWUGpS7Pcgo5FRsUUkCvMRclRg0hMLqtQAh6JK2fFzZJYhX+8JmlmmAno63LodrXvE\/l9R5CysTMpRg+4QJ5G5wj0eKVE0dw6Qw8TS7ghhFENruLNLpTS0tH7LUKSS4APnuTDzwmWnFgTzhDHOcOzQNPH7SxJgqRHCLOoevbf9rkfHoDYhrhvhNiZhsYQ3fR1vvJ18Q2vFOkDuWcIm0+ngV10T3UgduENf3ob3hZeJdW2wUxYdDcXxvsIn\/CBOF+9k5Xi7s8AuhbNuUngXYQQVpY0cLjyiabMkckPW\/UewlY4pgBCRm4ZWkMZGQDzdNXLtZ2ZoGvp6pAGbRrLCFQZolndQe\/6DhvKirsmSdYUF+2UOZ2GlRrqW3C3VCp4OjiMpHF9Ds26eSlB5AhqQp\/f+f\/96iQTOJtwHpcsIRsuoKHXNBpKBxfuALnOqv9xwpOXC2OpjHKSP9CJdVDoPaWOUpAT5o181L5RWCvhsEzY8OIsm1A+S3dIHfeZPVcV8hwXBeaQ=="
    reqs.now = 1640933310

    # Text = "gj2Slw7zsER7I+7ve1GoMmSc4sPx98spX5fE\/UMNA7KJWGBkHGkHmTdzu+d9RBbtjyGLRSoem4CBpI8V88UxLYbZiPSbA7voN9ft8h78tlXyKAlLxfR4q43FeEOZ9iqhoaZzEXKobDbRAY3oVL12xf2rY1JoGRqD1Un+iZgEEe1knOLD8ffLKV+XxP1DDQOyiVhgZBxpB5k3c7vnfUQW7UkmyWUxo3LXMCe8zmOcgncm1jJto49dAVI1pqc5YJteOQcmHglyNS\/jBhf6er7v57zoBITHb2flKWD5DFA32GBZo\/LN5d3FlymLgKLHqelbdqnIOmmclKCW0Qj1h60N1yGg3i4CRDm2CQrLfKVSUrFubNyxxx83K5aIbvZ9NubWJ7fK3G+cYCwAUE18z2Rx9gMgOaef5pvHncrWJ5ItQ3dGVB1CxpVfSk5nmBNsYSO7HoQkg\/YuoD\/n5rB8210kK5sRzcYeaJ3VdySxoJuMC3+\/TF8KtbI+INY8XQFKWWOdTEMOpHdx50C5tVCDkuwzg+XaqnZoAlqhs7I9\/umInvhanEoUO2riA\/M9guiD\/5poRmW39EWpzD8e3QaHo1nCClI40vvsrkT6g4FSRdF1bZW\/1hxh06OYndviKtyYWn85no+GTqLOx4EqgRbHHzA+XhXlkx89fFI7PcocfzMfk8CVuG2LJud\/Znr8yQOVyoXO7GXHOmLA\/4aHwA9H9V9+X1BChE\/doxZtQy9KBoPaA0Q70+NFMpez0a901kNXo01j1torXqu4qBrPVxompGJK4TjuM0DfLsIqfaOZWmw4RXomhP6AWF+4Em5B\/qTEyq99C71uTH6t10DnLIxf1EscXwM7VXyP1QKGev3LVydfllL8cTWuqyPo\/yuHj\/JtESQnLvzwIvVF8K\/RasAti1J6L\/mXD1jYpSI0R\/JKi+Fjd\/kjOeK8qZ1nhHxQFMkr6wDBKKzW7TmXqj1UUSmLJcpwSDtIKEMeeVkaYW4NciqZhfI8BPJZcgHeVLrHT8pcu+nrTnRLEvVNrsvfaCIWWIlIimDLoICFlKi82r9UxJS+7y6tIOISGKEPHrjxq2BU1ggMitnqDeMP5EGO3dk84rgF2xkiaGKB76ZxYVmxxbnozK\/YBsMhUWG93I3yE3ZqG29f7zEexTVuwAzFMVMizp8rpYx1ClCY9ITp+w0n+u7NBNg6au+npFPzKta7Dw2eYQMwWggF3bQbIjx2YpoHvx\/uQHbV4E33VR1L54RaT5y4rv77qdAlBjnTQXc1X\/LEmxJ7+1WM0Cnk+qLQ3BkcqBTcnrKumzZZgGDZBPSTPUAnUsztwmNDYmK6azJHeEe5QQiVFQC91ZWznVeZArLfH7d1cOcGK2R2Tj4CFId2OHa5QuHwLy9\/Ylxp3h0qdn6r5tXDqbK3E6s9mjL7GwIXdxJt6ocBWGNPRvJkjzERZP9\/ffBpUs10FdcUxA2BYNR3lMvuCdg4CUVX7\/576cjCg9h8P1Pfet9QOFxlrUnr2j+Dfuutg1LOYHrUy\/b64R1nUfkFR1OfdChuAP+g3HmlOQByrd4lSMEX2yKpR0YGCXiSACpWh9N35eRt6\/cnd5L5g1X9wgmCfKVItkECrndJ04vzrY4XCZZZK486ZJxbl2GBI+q65xlWNLpQ7Kvkag9gsg\/35SyPFc+pKQg0YKRlBP5dgMzs48VwW3t3hBdQlvIQJg1rvSGk4qZWRpplUOPU5lN6A\/pFmceXXRkXlsOL5Zy5UDC1okLzGJzPJPUI\/lqIiy4="
    # reqs.now = 1700559977

    # Text2 = "X+bnzYIcwF6C7Rd3T7njPI8Ls+7WOpYMYB4Jo0v3EBUxajNiDbkp63V965sLWnuQ9fBoadXgN0Wra0p5YnchwW3+be1xjXtFkch0PChn9aDCLbwt24BPd/i5ZFXyr3nKhhpI1jM7k/KVNayWyuUAhX6XmowZHUD5fOJKWvUD761pNRTi9eq+vNh1XDr3dIWInkFeK7g5aXSGaSKux2z5jUIJzw69HQ300Nf0UJV3iyHbavraaKpGzXbkPhQAsM++"
    reqs.ParseData(Text)