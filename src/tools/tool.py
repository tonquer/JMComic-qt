import hashlib
import json
import math
import os
import re
import time
from urllib.parse import quote

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
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        if Setting.Language.autoValue == 1:
            header["Accept-Language"] = "zh-CN,zh;q=0.9"
        elif Setting.Language.autoValue == 3:
            header["Accept-Language"] = "en-US,en;q=0.9"
        else:
            header["Accept-Language"] = "zh-HK,zh;q=0.9"
        return header

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
    def GetLookScaleModel(category):
        return ToolUtil.GetModelByIndex(Setting.LookNoise.value, Setting.LookScale.value, ToolUtil.GetLookModel(category))

    @staticmethod
    def GetDownloadScaleModel(w, h):
        dot = w * h
        # 条漫不放大
        if not config.CanWaifu2x:
            return {}
        return ToolUtil.GetModelByIndex(Setting.DownloadNoise.value, Setting.DownloadScale.value, Setting.DownloadModel.value)

    @staticmethod
    def GetPictureSize(data):
        from PIL import Image
        from io import BytesIO
        a = BytesIO(data)
        img = Image.open(a)
        a.close()
        return img.width, img.height

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
    def GetModelByIndex(noise, scale, index):
        if not config.CanWaifu2x:
            return {}
        if noise < 0:
            noise = 3
        from waifu2x_vulkan import waifu2x_vulkan
        if index == 0:
            return {"model": getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE" + str(noise)), "noise": noise,
                    "scale": scale, "index": index}
        elif index == 1:
            return {"model": getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE" + str(noise)), "noise": noise, "scale": scale,
                    "index": index}
        elif index == 2:
            return {"model": getattr(waifu2x_vulkan, "MODEL_PHOTO_NOISE" + str(noise)), "noise": noise, "scale": scale,
                    "index": index}
        elif index == 3:
            return {"model": getattr(waifu2x_vulkan, "MODEL_ANIME_STYLE_ART_RGB_NOISE" + str(noise)), "noise": noise,
                    "scale": scale, "index": index}
        return {"model": getattr(waifu2x_vulkan, "MODEL_CUNET_NOISE" + str(noise)), "noise": noise, "scale": scale,
                "index": index}

    @staticmethod
    def GetCanSaveName(name):
        return re.sub('[\\\/:*?"<>|\0\r\n]', '', name).rstrip(".")

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
    def ParseBookInfo(data, bookId):
        soup = BeautifulSoup(data, features="lxml")
        from tools.book import BookInfo
        book = BookInfo()
        book.baseInfo.bookId = bookId
        infos = soup.find_all("div", class_="p-t-5 p-b-5")
        for tag in infos:
            data = tag.text.replace("\n", "").strip()
            data = re.split('[:：]', data, maxsplit=1)
            if len(data) < 2:
                continue
            data[0] = data[0].strip()
            data[1] = data[1].strip()
            if ToolUtil.IsSameName(data[0], "叙述"):
                book.pageInfo.des = data[1]
            elif ToolUtil.IsSameName(data[0], "頁數"):
                book.pageInfo.pages = int(data[1])
            elif ToolUtil.IsSameName(data[0], "上架日期"):
                mo = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data[1])
                book.pageInfo.createDate = mo.group()
            elif ToolUtil.IsSameName(data[0], "更新日期"):
                mo = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", data[1])
                book.pageInfo.updateDate = mo.group()
            # print(data[0], data[1])
        tag = soup.find("img", class_="lazy_img img-responsive")
        book.baseInfo.coverUrl = tag.attrs.get("src", "")
        tag = soup.find("div", itemprop="name")
        if tag:
            book.baseInfo.title = tag.h1.text

        isFavorite = False
        tag = soup.find("span", class_="col btn collect-btn btn-primary")
        if tag:
            isFavorite = True

        infos = soup.find_all("div", class_="tag-block")
        for tag in infos:
            data = re.split('[:：]', tag.text.strip("\n"))
            if len(data) < 2:
                continue
            if ToolUtil.IsSameName(data[0], "作者"):
                book.baseInfo.authorList = data[1].strip().strip("\n").split("\n")
            elif ToolUtil.IsSameName(data[0], "标签"):
                book.baseInfo.tagList = data[1].strip().strip("\n").split("\n")
        epsTag = soup.find("ul", class_="btn-toolbar")
        from tools.book import BookEps
        if not epsTag:
            # 不分章节
            epsInfo = BookEps()
            epsInfo.title = "第一章"
            epsInfo.epsUrl = "/photo/{}".format(bookId)
            book.pageInfo.epsInfo[0] = epsInfo
        else:
            infos = epsTag.find_all("a")
            index = 0
            for tag in infos:
                epsUrl = tag.attrs.get("href")
                text = tag.li.text.strip("\n")
                epsText = text.split("\n")
                epsInfo = BookEps()
                epsInfo.epsUrl = epsUrl
                if len(epsText) == 3:
                    epsIndex = epsText[0]
                    epsTitle = epsText[1]
                    epsTime = epsText[2]
                    epsInfo.title = epsIndex
                    epsInfo.epsName = epsTitle
                    epsInfo.time = epsTime

                    book.pageInfo.epsInfo[index] = epsInfo
                    index += 1
                elif len(epsText) == 4:
                    epsIndex = epsText[0]
                    epsTitle = epsText[1] + epsText[2]
                    epsTime = epsText[3]
                    epsInfo.title = epsIndex
                    epsInfo.epsName = epsTitle
                    epsInfo.time = epsTime
                    book.pageInfo.epsInfo[index] = epsInfo
                    index += 1
        return isFavorite, book

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

    @staticmethod
    def ParseLoginUserName(data):
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find("div", id="userlinks")
        if not table:
            return "", ""
        tag = table.find("a")
        if not tag:
            return "", ""
        name = tag.text
        userId = "", ""
        mo = re.search("(?<=showuser=)\w+", tag.attrs.get("href", ""))
        if mo:
            userId = mo.group()
        return userId, name

    @staticmethod
    def ParseLoginResult(data):
        soup = BeautifulSoup(data, features="lxml")
        table = soup.find("div", class_="tablepad")
        if not table:
            return Status.Error
        if "captcha" in table.text:
            return Status.NeedGoogle
        elif "password incorrect" in table.text:
            return Status.UserError
        return Status.Error

    # 解析登录结果
    @staticmethod
    def ParseLogin(data):
        isSuc = False
        msg = ""
        mo = re.search("(?<=<script>toastr\[\'error\'\]\(\\\").* ", data)
        if mo:
            msg = mo.group()

        mo = re.search("(?<=<script>toastr\[\'success\'\]\(\\\").*!", data)
        if mo:
            isSuc = True
            msg = mo.group()
        return isSuc, msg

    # 解析用户信息
    @staticmethod
    def ParseUserInfo(data):
        from tools.user import User
        user = User()
        user.isLogin = True
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("img", class_="header-personal-avatar")
        user.imgUrl = tag.attrs.get("src", "")
        tag = soup.find("div", class_="header-right-username")
        user.userName = tag.text

        infos = soup.find_all("div", class_="header-profile-row")
        userAttr = {}
        for tag in infos:
            pass
            nameTag = tag.find("div", class_="header-profile-row-name")
            nameValue = tag.find("div", class_="header-profile-row-value")
            if nameTag and nameValue:
                name = nameTag.text.replace(" ", "").replace("\n", "")
                value = nameValue.text.replace(" ", "").replace(
                    "\n", "")
                userAttr[name] = value
        user.userAttr = userAttr
        return user

    # 解析收藏
    @staticmethod
    def ParseFavorite(data):
        soup = BeautifulSoup(data, features="lxml")
        tag = soup.find("div", class_="pull-left m-l-20")
        text = tag.text.replace("\n", "").replace(" ", "")
        print(text)
        data = re.findall("\d+", text)
        curNum = int(data[0])
        maxNum = int(data[1])
        tags = soup.find_all("div", class_="thumb-overlay")
        books = []
        for tag in tags:
            from tools.book import BookInfo
            info = BookInfo()
            info.baseInfo.bookUrl = tag.parent.attrs.get("href")
            if not info.baseInfo.bookUrl:
                continue
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("src", "")
            if info.baseInfo.coverUrl and "http" not in info.baseInfo.coverUrl:
                info.baseInfo.coverUrl = config.Url + info.baseInfo.coverUrl
            info.baseInfo.title = tag.img.attrs.get("title")
            for tag2 in tag.find_next_siblings():
                className = " ".join(tag2.attrs.get('class', []))
                if className == "video-title title-truncate":
                    info.baseInfo.title = tag2.text.replace("\n", "").strip()
                    pass
            books.append(info)
        return curNum, maxNum, books

    # 解析首页结果
    @staticmethod
    def ParseIndex(data):
        soup = BeautifulSoup(data, features="lxml")
        tags = soup.find_all("div", class_="thumb-overlay-albums")
        from tools.book import BookInfo
        books = []
        for tag in tags:
            info = BookInfo()
            info.baseInfo.bookUrl = tag.parent.attrs.get("href")
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("data-src")
            info.baseInfo.title = tag.img.attrs.get("title")
            for tag2 in tag.parent.find_next_siblings():
                className = " ".join(tag2.attrs.get('class', []))
                if className == "title-truncate hidden-xs":
                    info.baseInfo.author = tag2.a.text.replace("\n", "").strip()
                elif className == "title-truncate tags":
                    info.baseInfo.tagStr = tag2.text.replace("標籤: ", "").replace("\n", "").strip()
                elif className == "video-views pull-left hidden-xs":
                    info.baseInfo.date = tag2.text.replace("\n", "").strip()
            books.append(info)
        return books

    # 解析搜索结果
    @staticmethod
    def ParseSearch(data):
        soup = BeautifulSoup(data, features="lxml")
        tags = soup.find_all("div", class_="thumb-overlay")
        from tools.book import BookInfo
        books = []
        for tag in tags:
            info = BookInfo()
            info.baseInfo.bookUrl = tag.parent.attrs.get("href")
            info.baseInfo.bookId = re.search("(?<=/album/)\w*", info.baseInfo.bookUrl).group()
            info.baseInfo.coverUrl = tag.img.attrs.get("data-original")
            info.baseInfo.title = tag.img.attrs.get("title")
            for tag2 in tag.parent.find_next_siblings():
                className = " ".join(tag2.attrs.get('class', []))
                if className == "title-truncate hidden-xs":
                    info.baseInfo.author = tag2.a.text.replace("\n", "").strip()
                elif className == "title-truncate tags":
                    info.baseInfo.tagStr = tag2.text.replace("標籤: ", "").replace("\n", "").strip()
                elif className == "video-views pull-left hidden-xs":
                    info.baseInfo.date = tag2.text.replace("\n", "").strip()
            books.append(info)
        maxPage = 1

        pageTag = soup.find("ul", class_="pagination pagination-lg")
        if pageTag:
            allPage = pageTag.find_all("option")
            for v in allPage:
                maxPage = max(maxPage, int(v.text))
        return maxPage, books

    # 解析图片Url地址
    @staticmethod
    def ParsePictureUrl(data):
        soup = BeautifulSoup(data, features="lxml")
        infos = soup.find_all("div", id=re.compile(r"page_\d+"))
        # infos = soup.find_all("div")
        mo = re.search("(?<=var scramble_id = )\w+", data)
        minAid = int(mo.group())
        mo = re.search("(?<=var aid = )\w+", data)
        aid = int(mo.group())
        pictureUrl = {}
        pictureName = {}
        for tag in infos:
            tag2 = tag.find_next_sibling()
            url = tag2.get("data-original")
            id = re.search("\d+", tag2.get("id")).group()
            pictureName[int(id)-1] = id
            pictureUrl[int(id)-1] = url
        return aid, minAid, pictureUrl, pictureName

    # 获得图片分割数
    @staticmethod
    def GetSegmentationNum(aid, scramble_id, pictureName):
        if aid < scramble_id:
            num = 0
        elif aid < 268850:
            num = 10
        else:
            string = str(aid) + pictureName
            string = string.encode()
            string = hashlib.md5(string).hexdigest()
            num = ord(string[-1])
            num %= 10
            num = num * 2 + 2
        return num

    # 图片分割合成
    @staticmethod
    def SegmentationPicture(imgData, aid, scramble_id, bookId):
        num = ToolUtil.GetSegmentationNum(aid, scramble_id, bookId)
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