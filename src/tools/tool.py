import base64
import hashlib
import ipaddress
import json
import math
import os
import re
import time
from collections import OrderedDict
from urllib.parse import quote

import io
from lxml import etree

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
    AllUseFormat = [".jpg", ".png", ".gif", ".webp", ".bmp", ".apng", ".jpeg", ".jxl", ".avif"]
    AllFormatStr = [v.replace(".", "") for v in AllUseFormat]
    SrNeedConvertFormat = ["avif"]                       # sr_vulkan 导入不支持，超分前需转 PNG
    QtNeedConvertFormat = ["jxl", "avif"]                # Qt 不原生支持，显示前需转 PNG
    SrExportAnimaFormat = ["webp", "apng", "jxl"]        # sr_vulkan 原生支持动图导出
    SrExportFormat = ["bmp", "png", "jpg", "apng", "webp", "jxl"]  # sr_vulkan 原生支持导出
    AnimaFormat = ["gif", "webp", "apng"]                # Pillow save_all 支持的动图导出


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
        data = ToolUtil.GetModelByIndex(Setting.LookModelName.value, Setting.LookScale.value, mat)
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
        return ToolUtil.GetModelByIndex(Setting.DownloadModelName.value, Setting.DownloadScale.value, mat)

    @staticmethod
    def GetAnimationFormat(data):
        try:
            from PIL import Image
            from io import BytesIO
            with (
                BytesIO(data) as buffer,
                Image.open(buffer) as img,
            ):
                format = ""
                if getattr(img, "is_animated", ""):
                    format = img.format
                return format
        except Exception as es:
            Log.Error(es)
        return ""

    @staticmethod
    def GetPictureSize(data):
        if not data:
            return 0, 0, "jpg", False

        try:
            import pillow_jxl
            import pillow_avif
        except Exception as es:
            Log.Error(es)

        try:
            from PIL import Image
            from io import BytesIO
            with (
                BytesIO(data) as buffer,
                Image.open(buffer) as img,
            ):
                isAnima = getattr(img, "is_animated", False)
                if img.format.upper() == "PNG":
                    mat = "png"
                elif img.format.upper() == "GIF":
                    mat = "gif"
                elif img.format.upper() == "WEBP":
                    mat = "webp"
                elif img.format.upper() == "JXL":
                    mat = "jxl"
                elif img.format.upper() == "AVIF":
                    mat = "avif"
                elif img.format.upper() == "JPEG":
                    mat = "jpg"
                else:
                    mat = img.format.lower()
                exif = img.getexif()
                orientation = exif.get(274, 1)  # 默认值为 1（正常方向）
                width, height = img.width, img.height
                if orientation in (5, 6, 7, 8):
                    width, height = height, width  # 互换宽高
                return width, height, mat, isAnima
        except Exception as es:
            Log.Error(es)
        return 0, 0, "jpg", False

    @staticmethod
    def GetCanUseData(data):
        from qt_owner import QtOwner
        try:
            import pillow_jxl
            import pillow_avif
        except Exception as es:
            Log.Error(es)

        try:
            from PIL import Image
            from io import BytesIO
            with (
                BytesIO(data) as buffer,
                Image.open(buffer) as img,
            ):
                if img.format.lower() in ToolUtil.QtNeedConvertFormat and img.format.lower() not in QtOwner().allSupportFmt:
                    toMat = "PNG"
                    newBuffer = BytesIO()
                    img.save(newBuffer, format=toMat)
                    newData = newBuffer.getvalue()
                    newBuffer.close()
                    return newData
                else:
                    return data
        except Exception as es:
            Log.Error(es)
        return data

    @staticmethod
    def GetCanConvertUseData(data):
        try:
            import pillow_jxl
            import pillow_avif
        except Exception as es:
            Log.Error(es)

        try:
            from PIL import Image
            from io import BytesIO
            with (
                BytesIO(data) as buffer,
                Image.open(buffer) as img,
            ):
                if img.format.lower() in ToolUtil.SrNeedConvertFormat:
                    toMat = "PNG"
                    newBuffer = BytesIO()
                    img.save(newBuffer, format=toMat)
                    newData = newBuffer.getvalue()
                    newBuffer.close()
                    return newData
                else:
                    return data
        except Exception as es:
            Log.Error(es)
        return data

    # @staticmethod
    # def GetLookModel(category):
    #     if Setting.LookModel.value == 0:
    #         if "Cosplay" in category or "cosplay" in category or "CosPlay" in category or "COSPLAY" in category:
    #             return 2
    #         return 3
    #     else:
    #         return Setting.LookModel.value

    # @staticmethod
    # def GetModelAndScale(model):
    #     if not model:
    #         return "cunet", 1, 1
    #     scale = model.get('scale', 0)
    #     noise = model.get('noise', 0)
    #     if index == 0:
    #         model = "anime_style_art_rgb"
    #     elif index == 1:
    #         model = "cunet"
    #     elif index == 2:
    #         model = "photo"
    #     else:
    #         model = "anime_style_art_rgb"
    #     return model, noise, scale

    @staticmethod
    def GetModelByIndex(modelName, scale, mat="jpg"):
        if not config.CanWaifu2x:
            return {}
        data = {"scale": scale}
        from sr_vulkan import sr_vulkan as sr
        data["model"] = getattr(sr, modelName, 0)
        data["model_name"] = modelName
        return data

    @staticmethod
    def GetShowModelName(name):
        if "WAIFU2X_CUNET" in name:
            return "Waifu2x(cunet)"
        elif "WAIFU2X_ANIME" in name:
            return "Waifu2x(anime)"
        elif "WAIFU2X_PHOTO" in name:
            return "Waifu2x(photo)"
        elif "REALCUGAN_PRO" in name:
            return "Realcugan(pro)"
        elif "REALCUGAN_SE" in name:
            return "Realcugan(se)"
        elif "REALSR" in name:
            return "RealSR"
        elif "REALESRGAN_X4PLUSANIME" in name:
            return "X4plusAnime"
        elif "REALESRGAN_X4PLUS" in name:
            return "X4Plus"
        elif "REALESRGAN_ANIMAVIDEOV3" in name:
            return "AnimaVideoV3"
        return name

    @staticmethod
    def GetCanSaveName(name):
        # 限制文件夹名称为255/3的长度
        return str(re.sub('[\\\/:*?"<>|\0\t\r\n]', '', name).rstrip(".").strip(" "))[:254//3-1].rstrip(".").strip(" ")

    @staticmethod
    def LoadCachePicture(filePath):
        try:
            c = CTime()
            path = ""
            for mat in ToolUtil.AllUseFormat:
                if filePath[-4:] in ToolUtil.AllUseFormat:
                    path = filePath
                    mat = filePath[-4:]
                elif filePath[-5:] in ToolUtil.AllUseFormat:
                    path = filePath
                    mat = filePath[-5:]
                else:
                    path = filePath + mat
                if not os.path.isfile(path):
                    continue
                data = None
                with open(path, "rb") as f:
                    data = f.read()
                    if len(data) < 20:
                        Log.Debug(f"load_fail_picture, {path}")
                        continue

                return data
            c.Refresh("LoadCache", path)
        except Exception as es:
            Log.Error(es)
        return None

    @staticmethod
    def SavePicture(data, path, format):
        if path and not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        if path and data:
            path = ToolUtil.GetPictureName(path, format)
            with open(path, "wb+") as f:
                f.write(data)

    @staticmethod
    def SaveConvertPicture(data, path, format, isAni):
        if path and not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        from qt_owner import QtOwner
        if path and data:
            newFormat = QtOwner().GetConvertFmtRule(format)
            if isAni and newFormat not in ToolUtil.AnimaFormat:
                newFormat = format

            if newFormat != format and newFormat in ToolUtil.AllFormatStr:
                isSuc, newData = ToolUtil.ConvertPicture(data, newFormat, isAni)
                if path[-4:] in ToolUtil.AllUseFormat:
                    path = path[:-4]
                elif path[-5:] in ToolUtil.AllUseFormat:
                    path = path[:-5]
                if isSuc:
                    path = ToolUtil.GetPictureName(path, newFormat)
                else:
                    path = ToolUtil.GetPictureName(path, format)
            else:
                newData = data
                path = ToolUtil.GetPictureName(path, format)
            with open(path, "wb+") as f:
                f.write(newData)

    @staticmethod
    def SaveDownloadPicture(data, path, format, isAni):
        if path and not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        from qt_owner import QtOwner
        if path and data:
            newFormat = QtOwner().GetDownFmtRule(format)
            if isAni and newFormat not in ToolUtil.AnimaFormat:
                newFormat = format

            if newFormat != format and newFormat in ToolUtil.AllFormatStr:
                isSuc, newData = ToolUtil.ConvertPicture(data, newFormat, isAni)
                if path[-4:] in ToolUtil.AllUseFormat:
                    path = path[:-4]
                elif path[-5:] in ToolUtil.AllUseFormat:
                    path = path[:-5]
                if isSuc:
                    path = ToolUtil.GetPictureName(path, newFormat)
                else:
                    path = ToolUtil.GetPictureName(path, format)
            else:
                newData = data
                path = ToolUtil.GetPictureName(path, format)
            with open(path, "wb+") as f:
                f.write(newData)

    @staticmethod
    def ConvertPicture(data, fmt, isAni=False):
        try:
            import pillow_jxl
            import pillow_avif
        except Exception as es:
            Log.Error(es)
        try:
            from PIL import Image
            from io import BytesIO
            with (
                BytesIO(data) as buffer,
                BytesIO() as output_io,
                Image.open(buffer) as img,
            ):
                imgFmt = fmt
                if not isAni:
                    if fmt.lower() == "jpg" and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    if fmt.lower() == "jpg":
                        imgFmt = "JPEG"
                    if fmt.lower() == "apng":
                        imgFmt = "PNG"
                    img.save(output_io, format=imgFmt)
                    jpeg_bytes = output_io.getvalue()
                    return True, jpeg_bytes
                else:
                    frames = []
                    durations = []
                    if fmt.lower() == "apng":
                        imgFmt = "PNG"
                    for frame_idx in range(getattr(img, "n_frames", 1)):
                        img.seek(frame_idx)
                        rgba_frame = img.convert("RGBA")
                        frames.append(rgba_frame)
                        durations.append(img.info.get("duration", 100))
                    if not frames:
                        return False, data
                    loop = img.info.get("loop", 0)  # 0 表示无限循环
                    frames[0].save(
                        output_io,
                        format=imgFmt,
                        save_all=True,
                        append_images=frames[1:],
                        duration=durations,
                        loop=loop,
                        quality=80,
                    )
                    jpeg_bytes = output_io.getvalue()
                    return True, jpeg_bytes
        except Exception as es:
            Log.Error(es)
        return False, data

    @staticmethod
    def GetPictureName(path, format):
        if path:
            if path[-4:] in ToolUtil.AllUseFormat:
                pass
            elif path[-5:] in ToolUtil.AllUseFormat:
                pass
            else:
                path = path + "." + format
        return path


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
        if isinstance(v.get("update_at"), int):
            b.baseInfo.addTime = v.get("update_at")
        if isinstance(v.get('update_at'), str) and v.get('update_at').isdigit():
            b.baseInfo.addTime = int(v.get("update_at"))
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
        parseData = []
        raw = json.loads(result)
        for v in raw:
            from tools.book import IndexInfo
            info = IndexInfo()
            bookList = ToolUtil.ParseBookList(v.get("content", []))
            info.title = v.get("title", "")
            info.id = v.get("id", "")
            info.slug = v.get("slug", "")
            info.type = v.get("type", "")
            info.bookList = bookList
            info.filter_val = v.get("filter_val", "")
            parseData.append(info)
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
        u.exp = raw.get('exp', 0)
        u.nex_exp = raw.get('nextLevelExp', 0)
        u.jwttoken = raw.get('jwttoken')
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
    def ParseRecommend2(result):
        raw = json.loads(result)
        # total = int(raw.get("total"))
        bookList = ToolUtil.ParseBookList(raw.get("content", []))
        return len(bookList), bookList

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
            for v2 in v.get("sub_categories", []):
                b2 = Category()
                b2.id = v2.get("CID")
                b2.name = v2.get("name")
                b2.slug = v2.get("slug")
                b.sub_categories.append(b2)
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
        if raw.get('series_id') and raw.get('series_id') != "0":
            b.baseInfo.series_id = raw.get('series_id')
        b.baseInfo.title = raw.get('name')
        b.baseInfo.likes = raw.get('likes')
        b.baseInfo.views = raw.get('total_views')
        addTime = raw.get("addtime", "")
        if isinstance(addTime, str) and addTime.isdigit():
            b.baseInfo.addTime = int(addTime)

        if raw.get('price'):
            b.baseInfo.price = raw.get('price', 0)
        if raw.get('purchased'):
            b.baseInfo.purchased = raw.get('purchased', True)
        b.baseInfo.authorList = raw.get("author")
        b.baseInfo.tagList = raw.get("tags", [])
        b.baseInfo.workList = raw.get("works", [])
        b.baseInfo.actorList = raw.get("actors", [])
        b.pageInfo.des = raw.get("description")
        b.pageInfo.commentNum = int(raw.get("comment_total"))
        isFavorite = raw.get("is_favorite")

        from tools.book import BookEps
        ## 264793不按sort顺序
        series = raw.get("series", [])
        if series:
            for index, v in enumerate(series):
                epsInfo = BookEps()
                epsInfo.index = index
                epsInfo.sort = int(v.get("sort"))
                from tools.str import Str
                if v.get("name"):
                    epsInfo.title = Str.GetStr(Str.EpisodeTitleWithName).format(epsInfo.index+1, v.get("name"))
                else:
                    epsInfo.title = Str.GetStr(Str.EpisodeTitle).format(epsInfo.index+1)
                epsInfo.epsId = v.get('id')
                epsInfo.epsName = v.get("name")
                b.pageInfo.epsInfo[epsInfo.index] = epsInfo
        else:
            from tools.str import Str
            epsInfo = BookEps()
            epsInfo.title = Str.GetStr(Str.EpisodeTitle).format(1)
            epsInfo.epsUrl = "/photo/{}".format(bookId)
            epsInfo.epsId = bookId
            b.pageInfo.epsInfo[0] = epsInfo
        return b, isFavorite

    @staticmethod
    def ParseBookEpsScramble(data):
        try:
            mo = re.search(r"(?<=var scramble_id = )\w+", data.decode("utf-8"))
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
                epsInfo.sort = int(info.get("sort"))
        allIds = []
        idMap = {}
        for name in raw.get("images", []):
            mo = re.search(r"\d+", name)
            if not mo:
                continue
            picId = mo.group()
            allIds.append(int(picId) -1)
        for index, picId in enumerate(sorted(allIds)):
                idMap[picId] = index
        for name in raw.get("images", []):
            mo = re.search(r"\d+", name)
            if not mo:
                continue
            picId = mo.group()
            index = idMap.get(int(picId)-1)
            epsInfo.pictureName[index] = name.split(".")[0]
            epsInfo.pictureUrl[index] = "/media/photos/{}/{}".format(epsInfo.epsId, name)
        epsInfo.allIndex = sorted(epsInfo.pictureUrl.keys())
        return epsInfo

    # 解析搜索结果
    @staticmethod
    def ParseReadBook2(result):
        raw = json.loads(result)
        from tools.book import BookEps
        epsInfo = BookEps()
        epsInfo.epsId = raw.get("id")
        epsInfo.series_id = raw.get("series_id")
        epsInfo.epsName = raw.get("name")
        # for info in raw.get("series", []):
        #     if str(info.get("id")) == str(epsInfo.epsId):
        #         epsInfo.sort = int(info.get("sort"))
        allIds = []
        idMap = {}
        for v in raw.get("images", []):
            page = v.get("page")
            image = v.get("image")
            allIds.append((page, image))

        # for index, picId in enumerate(sorted(allIds)):
        #     idMap[picId] = index
        for index, v in enumerate(sorted(allIds, key=lambda a:a[0])):
            _, image = v
            mo = re.search(r"(?<=media/photos/{}/).*\?".format(epsInfo.epsId), image)
            name = mo.group().strip("?")
            epsInfo.pictureName[index] = name.split(".")[0]
            epsInfo.pictureUrl[index] = "/media/photos/{}/{}".format(epsInfo.epsId, name)
        epsInfo.allIndex = sorted(epsInfo.pictureUrl.keys())
        epsInfo.scrambleId = raw.get("scramble_id", "")
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
                b2.linkBookName = v2.get("name")
                b2.linkBookId = v2.get("AID")
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
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        isSuc = False
        msg = ""
        errList = re.findall(r"(?<=toastr\[\'error\'\]\(\").*\"", data)
        if errList:
            msg = "\n".join(errList)

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

    @staticmethod
    def ParseSerializationReq2(result):
        raw = json.loads(result)
        bookList = ToolUtil.ParseBookList(raw.get("list", []))
        total = int(raw.get("total", 0))
        return bookList, total

    @staticmethod
    def ParseRandomRecommendReq2(result):
        raw = json.loads(result)
        bookList = ToolUtil.ParseBookList(raw)
        return bookList, len(bookList)

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
            return True

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
        return True

    @staticmethod
    def IsSameName(name1, name2):
        return Converter('zh-hans').convert(name1) == Converter('zh-hans').convert(name2)


    # @staticmethod
    # def GetPictureFormat(data):
    #     import imghdr
    #     mat = imghdr.what(None, data)
    #     if mat:
    #         return mat
    #     return "jpg"

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
                os.makedirs(fileDir, exist_ok=True)

            with open(filePath, "wb+") as f:
                f.write(data)

            Log.Debug("add chat cache, cachePath:{}".format(filePath))

        except Exception as es:
            Log.Error(es)

    @staticmethod
    def GetComicInfoXml(epsId, picNum, bookInfo):
        from lxml import etree
        from tools.book import BookInfo
        assert isinstance(bookInfo, BookInfo)
        root = etree.Element("ComicInfo")

        title = etree.SubElement(root, "Title")  # 标题
        title.text = bookInfo.baseInfo.title

        publish = etree.SubElement(root, "Publisher")  # 标题
        publish.text = config.ProjectName

        writer = etree.SubElement(root, "Writer")  # 作者
        writer.text = bookInfo.baseInfo.author
        if bookInfo.baseInfo.authorList:
            writer.text = bookInfo.baseInfo.authorList[0]

        desc = etree.SubElement(root, "Summary")  # 摘要
        desc.text = bookInfo.pageInfo.des

        bookId = etree.SubElement(root, "BookId")  # 当前章节
        bookId.text = str(bookInfo.baseInfo.id)

        series = etree.SubElement(root, "Series")  # 当前章节
        series.text = str(bookInfo.baseInfo.title)

        number = etree.SubElement(root, "Number")  # 当前章节
        number.text = str(epsId+1)

        count = etree.SubElement(root, "Count")  # 总章节
        count.text = str(bookInfo.pageInfo.maxEps() + 1)

        genre = etree.SubElement(root, "Genre")  # 分类
        genre.text = ",".join(bookInfo.baseInfo.category)

        tags = etree.SubElement(root, "Tags")
        tags.text = ",".join(bookInfo.baseInfo.tagList)

        everyoneTags = ["无h", "無h"]
        isNotH = ToolUtil.IsHaveAssignTag(tags, everyoneTags)
        ageRating = etree.SubElement(root, "AgeRating")  # R18+  Everyone
        if isNotH:
            ageRating.text = "Everyone"
        else:
            ageRating.text = "R18+"

        pageCount = etree.SubElement(root, "PageCount")  # ue
        pageCount.text = str(picNum)

        blackAndWhite = etree.SubElement(root, "BlackAndWhite")  # Yes No
        everyoneTags = ["全彩", "cosplay"]
        isColor = ToolUtil.IsHaveAssignTag(tags.text, everyoneTags)
        if isColor:
            blackAndWhite.text = "No"
        else:
            blackAndWhite.text = "Yes"

        manga = etree.SubElement(root, "Manga")  # Yes No
        everyoneTags = ["cosplay"]
        isCos = ToolUtil.IsHaveAssignTag(tags.text, everyoneTags)
        if isCos:
            manga.text = "No"
        else:
            manga.text = "Yes"

        tree = etree.ElementTree(root)
        buffer = io.BytesIO()
        tree.write(buffer, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        data = buffer.getvalue()
        buffer.close()
        return data

    @staticmethod
    def IsHaveAssignTag(tagList, assignList):
        isHave = False
        for tag in tagList:
            for noHtag in assignList:
                if noHtag.lower() in tag.lower():
                    isHave = True
                    break
        return  isHave

    @staticmethod
    def IsipAddress(hostname) -> bool:
        if isinstance(hostname, bytes):
            # IDN A-label bytes are ASCII compatible.
            hostname = hostname.decode("ascii")
        _IPV4_PAT = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        _IPV4_RE = re.compile("^" + _IPV4_PAT + "$")
        _HEX_PAT = "[0-9A-Fa-f]{1,4}"
        _LS32_PAT = "(?:{hex}:{hex}|{ipv4})".format(hex=_HEX_PAT, ipv4=_IPV4_PAT)
        _subs = {"hex": _HEX_PAT, "ls32": _LS32_PAT}
        _variations = [
            #                            6( h16 ":" ) ls32
            "(?:%(hex)s:){6}%(ls32)s",
            #                       "::" 5( h16 ":" ) ls32
            "::(?:%(hex)s:){5}%(ls32)s",
            # [               h16 ] "::" 4( h16 ":" ) ls32
            "(?:%(hex)s)?::(?:%(hex)s:){4}%(ls32)s",
            # [ *1( h16 ":" ) h16 ] "::" 3( h16 ":" ) ls32
            "(?:(?:%(hex)s:)?%(hex)s)?::(?:%(hex)s:){3}%(ls32)s",
            # [ *2( h16 ":" ) h16 ] "::" 2( h16 ":" ) ls32
            "(?:(?:%(hex)s:){0,2}%(hex)s)?::(?:%(hex)s:){2}%(ls32)s",
            # [ *3( h16 ":" ) h16 ] "::"    h16 ":"   ls32
            "(?:(?:%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s",
            # [ *4( h16 ":" ) h16 ] "::"              ls32
            "(?:(?:%(hex)s:){0,4}%(hex)s)?::%(ls32)s",
            # [ *5( h16 ":" ) h16 ] "::"              h16
            "(?:(?:%(hex)s:){0,5}%(hex)s)?::%(hex)s",
            # [ *6( h16 ":" ) h16 ] "::"
            "(?:(?:%(hex)s:){0,6}%(hex)s)?::",
        ]
        _IPV6_PAT = "(?:" + "|".join([x % _subs for x in _variations]) + ")"
        _UNRESERVED_PAT = r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._\-~"
        _ZONE_ID_PAT = "(?:%25|%)(?:[" + _UNRESERVED_PAT + "]|%[a-fA-F0-9]{2})+"
        _IPV6_ADDRZ_PAT = r"\[" + _IPV6_PAT + r"(?:" + _ZONE_ID_PAT + r")?\]"
        _BRACELESS_IPV6_ADDRZ_RE = re.compile("^" + _IPV6_ADDRZ_PAT[2:-2] + "$")
        return bool(_IPV4_RE.match(hostname) or _BRACELESS_IPV6_ADDRZ_RE.match(hostname))

    @staticmethod
    def HasIpv6() -> bool:
        """Returns True if the system can bind an IPv6 address."""
        host = "::1"
        sock = None
        has_ipv6 = False
        import socket
        if socket.has_ipv6:
            # has_ipv6 returns true if cPython was compiled with IPv6 support.
            # It does not tell us if the system has IPv6 support enabled. To
            # determine that we must bind to an IPv6 address.
            # https://github.com/urllib3/urllib3/pull/611
            # https://bugs.python.org/issue658327
            try:
                sock = socket.socket(socket.AF_INET6)
                sock.bind((host, 0))
                has_ipv6 = True
            except Exception:
                pass

        if sock:
            sock.close()
        return has_ipv6

    @staticmethod
    def ExportIpsByStr(text):
        _IPV4 = re.compile(
            r'(?<![\w.])' r'(?:25[0-5]|2[0-4]\d|1?\d?\d)' r'(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}' r'(?![\w.])')
        _IPV6 = re.compile(r'(?<![0-9A-Fa-f:])([0-9A-Fa-f:]{2,39})(?![0-9A-Fa-f:])')
        found, seen = [], set()
        for raw in _IPV4.findall(text) + _IPV6.findall(text):
            if not raw or raw in seen:
                continue
            try:
                ip = ipaddress.ip_address(raw)
            except ValueError:
                continue
            if (ip.is_loopback or ip.is_link_local or ip.is_unspecified
                    or ip.is_multicast or ip.is_reserved):
                continue
            seen.add(raw)
            found.append(raw)
        return found
