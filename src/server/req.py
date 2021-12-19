import json

from config import config
from config.setting import Setting
from tools.tool import ToolUtil


class ServerReq(object):
    def __init__(self, url, header=None, params=None, method="POST") -> None:
        self.url = url
        self.headers = header
        self.params = params
        self.method = method
        self.isParseRes = False
        self.timeout = 5
        self.isUseHttps = True
        self.cookies = {}
        if Setting.IsHttpProxy.value:
            self.proxy = {"http": Setting.HttpProxy.value, "https": Setting.HttpProxy.value}
        else:
            self.proxy = {}

    def __str__(self):
        if Setting.LogIndex.value == 0:
            return self.__class__.__name__
        elif Setting.LogIndex.value == 1:
            return "{}, url:{}".format(self.__class__.__name__, self.url)
        headers = dict()
        headers.update(self.headers)
        params = self.params
        return "{}, url:{}, proxy:{}, method:{}, headers:{}, params:{}".format(self.__class__.__name__, self.url, self.proxy, self.method, headers, params)


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, isSaveCache=False, saveFile=""):
        method = "Download"
        self.url = url
        self.isSaveCache = isSaveCache
        self.saveFile = saveFile
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 登陆前，需要获取cookie
class LoginPreReq(ServerReq):
    def __init__(self):
        method = "Get"
        url = config.Url + "/login"
        header = ToolUtil.GetHeader(url, method)
        super(self.__class__, self).__init__(url, header, {}, method)


# 登陆
class LoginReq(ServerReq):
    def __init__(self, userId, passwd, cookies=None):
        method = "POST"
        url = config.Url + "/login"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["username"] = userId
        data["password"] = passwd
        data["submit_login"] = ""
        header["Content-Type"] = "application/x-www-form-urlencoded"
        # header["origin"] = config.Url
        # header["referer"] = url
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)
        if cookies:
            self.cookies = cookies


# 获得UserInfo
class GetUserInfoReq(ServerReq):
    def __init__(self):
        method = "GET"
        url = config.Url + "/user"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        super(self.__class__, self).__init__(url, header, data, method)


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self, url):
        # url = config.UpdateUrl
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False


# 本子信息
class GetBookInfoReq(ServerReq):
    def __init__(self, bookId):
        self.bookId = bookId
        url = config.Url + "/album/{}".format(bookId)
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 获取一个章节的图片地址
class GetBookImgUrl(ServerReq):
    def __init__(self, bookId, epsId):
        from tools.book import BookMgr
        book = BookMgr().GetBook(bookId)
        epsInfo = book.pageInfo.epsInfo.get(epsId)
        url = config.Url + epsInfo.epsUrl
        method = "Get"
        self.bookId = bookId
        self.epsId = epsId
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 搜索请求
class GetSearchReq(ServerReq):
    def __init__(self, search, page=1, mainCategory="", subCategory="", sort="mr", sortDay="a"):
        # sort []&t=t&o=tf

        # 所有，今日，本周，本月
        # t= [a, t, w, m]

        # 最新，最多点击，最多图片, 最多爱心
        # o = [mr, mv, mp, tf]

        # 其他漫画，another
        # 同人志, doujin, [汉化：chinese, 日语：japanese， CG:CG, cosplay:cosplay]
        # 韩漫  hanman
        # 美漫  meiman
        # 短片 short, [汉化：chinese, 日语：japanese]
        # 单本 single, [汉化：chinese, 日语：japanese]

        data = {"search_query": search}

        if page > 1:
            data['page'] = str(page)
        if sortDay:
            data['t'] = sortDay
        if sort:
            data["o"] = sort
        url = config.Url + "/search/photos"
        if mainCategory:
            url += "/" + mainCategory
            if subCategory:
                url += "/sub/" + subCategory

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)

# 获得首页
class GetIndexInfoReq(ServerReq):
    def __init__(self):
        url = config.Url
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得收藏
class GetFavoritesReq(ServerReq):
    def __init__(self, page=1, sort="mr"):
        # 收藏时间, 更新时间
        # o = [mr, mp]
        data = dict()
        data["o"] = sort
        if page > 1:
            data['page'] = str(page)
        param = ToolUtil.DictToUrl(data)
        url = config.Url + "/user/" + config.LoginUserName +"/favorite/albums/?" + param
        method = "GET"

        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 添加收藏
class AddFavoritesReq(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "/ajax/favorite_album"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["album_id"] = bookId
        data["fid"] = 0

        header["Content-Type"] = "application/x-www-form-urlencoded"
        header["origin"] = config.Url
        header["referer"] = config.Url + "/album/{}/".format(bookId)
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


# 删除收藏
class DelFavoritesReq(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url + "/ajax/remove_album_playlist"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["video_id"] = bookId
        data["list"] = "favorites"
        header["Content-Type"] = "application/x-www-form-urlencoded"
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


# Doh域名解析
class DnsOverHttpsReq(ServerReq):
    def __init__(self, domain=""):
        url = Setting.DohAddress.value + "?name={}&type=A".format(domain)
        method = "GET"
        header = dict()
        header["accept"] = "application/dns-json"
        super(self.__class__, self).__init__(url, header, {}, method)
        self.timeout = 5
        self.isParseRes = True


# 测试Ping
class SpeedTestPingReq(ServerReq):
    def __init__(self, domain):
        url = "https://{}".format(domain)
        method = "GET"
        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        super(self.__class__, self).__init__(url, header,
                                             {}, method)

# 测速
class SpeedTestReq(ServerReq):
    Index = 0
    URLS = [
        "https://storage1.picacomic.com/static/fc75975a-af8e-40c5-8679-725d6f64d6f5.jpg",
        # "https://storage1.picacomic.com/static/5aa5c52b-8fb5-4c16-866c-d6d92fb4a761.jpg",
        # "https://storage1.picacomic.com/static/7e7d1320-9717-4702-883d-2899975283b2.jpg",
        # "https://storage1.picacomic.com/static/91c3f41a-e6de-4de1-a80f-10af17aee5a8.jpg",
        # "https://storage1.picacomic.com/static/60c852b9-e47d-400c-af9d-bee86ce20b6d.jpg",
        # "https://storage1.picacomic.com/static/66541fe6-caaa-4965-ac1a-1b1b793e5677.jpg",
    ]

    def __init__(self):
        url = SpeedTestReq.URLS[SpeedTestReq.Index]
        SpeedTestReq.Index += 1
        if SpeedTestReq.Index >= len(SpeedTestReq.URLS):
            SpeedTestReq.Index = 0
        method = "Download"
        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        super(self.__class__, self).__init__(url, header,
                                             {}, method)
