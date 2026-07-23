import base64
import hashlib
import json
import struct
import time

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
import platform
import urllib
from curl_cffi import CurlOpt, CurlHttpVersion


class ServerReq(object):
    SPACE_PIC = set()  # 优先使用CDN，如果出现空白图片则回源

    def __init__(self, url, params=None, method="POST") -> None:
        self.url = url
        self.resetCnt = 1
        self.resetUrl = []
        self.resetIndex = 0
        self.params = params
        self.method = method
        self.isParseRes = False
        self.timeout = 5
        self.isUseHttps = True
        # self.isUseHttps = bool(Setting.IsUseHttps.value)
        self.proxyUrl = ""
        self.extend = {}
        self.cookies = {}
        self.curl_opt = {}
        self.isApi = False
        self.isImg = False
        host = ToolUtil.GetUrlHost(self.url)
        if "https://" + host in GlobalConfig.Url2List.value :
            self.isApi = True
            self.timeout = Setting.ApiTimeOut.GetIndexV()

        if "https://" +host in GlobalConfig.PicUrlList.value:
            self.isImg = True
            self.timeout = Setting.ImgTimeOut.GetIndexV()
        # if Setting.ProxySelectIndex.value == 5:
        #     host = ToolUtil.GetUrlHost(url)
        #     if host in GlobalConfig.Url2List.value:
        #         self.proxyUrl = config.ProxyApiDomain
        #     elif host == GlobalConfig.Url.value:
        #         self.proxyUrl = config.ProxyApiDomain
        #     elif host in GlobalConfig.PicUrlList.value:
        #         self.proxyUrl = config.ProxyImgDomain
        self.SetIndex(Setting.ProxySelectIndex.value, Setting.ProxyImgSelectIndex.value)
        self.SetProxy(Setting.IsHttpProxy.value, Setting.HttpProxy.value, Setting.Sock5Proxy.value)
            
        self.now = int(time.time())
        self.headers = self.GetHeader(url, method)
            
        from qt_owner import QtOwner
        self.cookies = dict(QtOwner().cookie)
        if self.isApi and not self.proxyUrl and Setting.ProxySelectIndex.value == 5:
            self.ipList = [Setting.ProxyIpValue.value]
        elif self.isImg and not self.proxyUrl and Setting.ProxyImgSelectIndex.value == 5:
            self.ipList = [Setting.ProxyIpValue.value]
        else:
            self.ipList = []
        self.SetCurlOpt(Setting.IsOpenHTTP3.value, Setting.EnableEch.value, QtOwner().echConfig, self.ipList)

    def SetIndex(self, apiIndex, imgIndex, apiHost=None, imgHost=None):
        host = ToolUtil.GetUrlHost(self.url)
        self.proxyUrl = ""

        if self.isApi:
            if apiIndex == 6:
                self.proxyUrl = GlobalConfig.ProxyApiDomain2.value
            if apiHost:
                self.url = self.url.replace(host, ToolUtil.GetUrlHost(apiHost))

        if self.isImg:
            if imgIndex == 6:
                self.proxyUrl = GlobalConfig.ProxyImgDomain2.value
            if imgHost:
                self.url = self.url.replace(host, ToolUtil.GetUrlHost(imgHost))
        if self.proxyUrl:
            self.url += "/"

    def SetProxy(self, proxyIndex, httpProxy, sock5Proxy):
        if proxyIndex == 1:
            self.proxy = {"http": httpProxy, "https": httpProxy}
        elif proxyIndex == 2 and sock5Proxy:
            data = sock5Proxy.replace("http://", "").replace("https://", "").replace("sock5://", "").replace(
                "socks5://", "")
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                proxy = f"socks5://{host}:{port}"
                self.proxy = {"http": proxy, "https": proxy}
        elif proxyIndex == 3:
            proxy = urllib.request.getproxies()
            if isinstance(proxy, dict) and proxy.get("http"):
                self.proxy = {"http": proxy.get("http"), "https": proxy.get("http")}
        else:
            self.proxy = {"http": None, "https": None}

    def SetCurlOpt(self, isHttp3=False, isEch=False, echConfig="", dnsIpList=None):
        self.curl_opt = dict()
        self.curl_opt[CurlOpt.HTTP_VERSION] = CurlHttpVersion.V2_0
        host = ToolUtil.GetUrlHost(self.url)
        isEch = isEch and (self.isImg or self.isApi) and not self.proxyUrl
        # allUrls = GlobalConfig.DohUrlList.value[:]
        # allUrls.extend(GlobalConfig.NoHttp3Url.value[:])
        # allUrls.append(Setting.DohAddress.value)
        # for ignoreUrl in allUrls:
        #     if host in ignoreUrl:
        #         isEch = False
        #         break
        if isEch and echConfig:
            self.curl_opt[CurlOpt.ECH] = f"ecl:{echConfig}"
        if dnsIpList:
            if isinstance(dnsIpList, list):
                ipStr = ",".join(dnsIpList)
            else:
                ipStr = dnsIpList

            if ipStr:
                self.curl_opt[CurlOpt.RESOLVE] = [f"{host}:443:{ipStr}"]
        if isHttp3:
            self.curl_opt[CurlOpt.HTTP_VERSION] = CurlHttpVersion.V3

    def ResetToSwitchNextUrl(self):
        if not self.resetUrl:
            return False
        if self.resetIndex >= len(self.resetUrl):
            return False
        url = self.resetUrl[self.resetIndex]
        self.resetIndex += 1
        Log.Info("request switch url:{}->{}".format(self.url, url))
        self.url = url
        return True
        # host = ToolUtil.GetUrlHost(self.url)
        # if host in self.resetUrlHost:
        #     index = self.resetUrlHost.index(host)
        #     if index >= len(self.resetUrlHost)-1:
        #         return False
        #     newHost = self.resetUrlHost[index+1]
        #     host = ToolUtil.GetUrlHost(self.url)
        #     self.url = self.url.replace(host, newHost)
        #     Log.Info("request 404 switch:{}->{}".format(host, newHost))
        #     return True
        # else:
        #     newUrl = self.resetUrl[0]
        #     host = ToolUtil.GetUrlHost(self.url)
        #     self.url = self.url.replace(host, newHost)
        #     Log.Info("request 404 switch:{}->{}".format(host, newHost))
        #     return True

    def __str__(self):
        ech = False
        if CurlOpt.ECH in self.curl_opt:
            ech = True
        if Setting.LogIndex.value == 0:
            return self.__class__.__name__
        elif Setting.LogIndex.value == 1:
            return "{}, ech:{}, url:{}, ip:{}".format(self.__class__.__name__, ech, self.url, self.ipList)
        headers = dict()
        headers.update(self.headers)
        params = self.params
        return "{}, ech:{}, url:{}, proxy:{}, method:{}, headers:{}, params:{}".format(self.__class__.__name__, ech, self.url, self.proxy, self.method, headers, params)

    def GetHeader(self, _url: str, method: str) -> dict:
        param = "{}{}".format(self.now, "18comicAPP")
        token = hashlib.md5(param.encode("utf-8")).hexdigest()
        # if Setting.UerAgent.value:
        #     ua = Setting.UerAgent.value
        # else:
        #     ua = "Mozilla/5.0 (Linux; Android 7.1.2; DT1901A Build/N2G47O; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36"

        header = {
            "tokenparam": "{},{}".format(self.now, GlobalConfig.HeaderVer.value),
            "token": token,
            # "user-agent": ua,
            "accept-encoding": "gzip",
            "version": config.UpdateVersion,
        }
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
        return header

    def GetHeader2(self, _url: str, method: str) -> dict:
        param = "{}{}".format(self.now, "18comicAPPContent")
        token = hashlib.md5(param.encode("utf-8")).hexdigest()

        header = {
            "tokenparam": "{},{}".format(self.now, GlobalConfig.HeaderVer.value),
            "token": token,
            "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; DT1901A Build/N2G47O; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36",
            "accept-encoding": "gzip",
        }
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
        return header

    def GetWebHeader2(self) -> dict:
        return \
        {
            # "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }

    def GetWebHeader(self) -> dict:
        header = {
        # 'authority': '18comic.org',
          "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
          "accept-encoding":"gzip, deflate, br",
           # "cookie": 'ipcountry=CN; ipm5=6846bee8bfbb7323e83d0f32c635eae9',
          "accept-language":"zh-CN,zh;q=0.9",
           # "content-type": "application/x-www-form-urlencoded",
           "upgrade-insecure-requests":"1",
            # 'sec-ch-ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            # 'sec-fetch-dest': 'document',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'none',
            # 'sec-fetch-user': '?1',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }
        if self.method.lower() == "post" or self.method.lower() == "post2":
            header["content-type"] = "application/x-www-form-urlencoded"
        return header

    def GetWebError(self, text):
        if "Edge IP Restricted" in text:
            return "Edge IP Restricted"
        elif "Just a moment..." in text:
            return Str.GetStr(Str.NeedGoogle)
        elif "Sorry, you have been blocked" in text:
            return "Sorry, you have been blocked"
        else:
            return text

    def ParseData(self, data) -> str:
        # param = "{}{}".format(self.now, "18comicAPPContent")
        # key = hashlib.md5(param.encode("utf-8")).hexdigest()
        # aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        # byteData = base64.b64decode(data.encode("utf-8"))
        # result = aes.decrypt(byteData)
        # unpad = lambda s: s[0:-s[-1]]
        # result2 = unpad(result)
        # newData = result2.decode()
        # return newData
        from jmcomic import JmCryptoTool
        return JmCryptoTool.decode_resp_data(data, ts=self.now)


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self, url2List, isPre=False):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        if not isPre:
            newList = [v + "/version.txt?" for v in url2List[1:]]
            url = url2List[0] + "/version.txt?"
        else:
            newList = [v + "/version_pre.txt?" for v in url2List[1:]]
            url = url2List[0] + "/version_pre.txt?"
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)
        self.isParseRes = False
        self.headers["user-agent"] = config.RealVersion
        self.useImgProxy = False
        self.resetUrl = newList
        self.resetCnt = len(url2List)


# 检查更新
class CheckUpdateInfoReq(ServerReq):
    def __init__(self, url2List, newVersion):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        url = url2List[0] + "/{}.txt?".format(newVersion)
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)
        self.headers["user-agent"] = config.RealVersion
        self.isParseRes = False
        self.useImgProxy = False
        self.resetUrl = [v + "/{}.txt?".format(newVersion) for v in url2List[1:]]
        self.resetCnt = len(url2List)


# 检查更新配置
class CheckUpdateConfigReq(ServerReq):
    def __init__(self, url2List):
        method = "GET"
        data = dict()
        data["version"] = config.RealVersion
        data["platform"] = platform.platform()
        url = url2List[0] + "/config.txt?"
        url += ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)
        self.headers["user-agent"] = config.RealVersion
        self.isParseRes = False
        self.useImgProxy = False
        self.resetUrl = [v + "/config.txt?" for v in url2List[1:]]
        self.resetCnt = len(url2List)


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, loadPath="", cachePath="", savePath="", saveParam=(0, 0, ""), isReload=False, resetCnt=1):
        method = "Download"
        self.url = url
        if self.url in ServerReq.SPACE_PIC:
            self.url += "?v={}".format(int(time.time()))
        self.loadPath = loadPath
        self.cachePath = cachePath
        self.savePath = savePath
        self.saveParam = saveParam
        self.isReload = isReload
        self.isReset = False
        super(self.__class__, self).__init__(self.url, {}, method)
        self.resetCnt = resetCnt

        if "_3x4" in self.url:
            self.resetUrl.append(self.url.replace("_3x4", ""))

        self.headers = dict()
        self.headers["Accept-Encoding"] ="None"
        # if Setting.UerAgent.value:
        #     ua = Setting.UerAgent.value
        # else:
        #     ua = "Mozilla/5.0 (Linux; Android 7.1.2; DT1901A Build/N2G47O; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36"

        # self.headers["Accept-Encoding"] ="None"
        # self.headers["user-agent"] = ua


# 注册前，需要获取cookie
class LoginCheck301Req(ServerReq):
    def __init__(self):
        method = "Get2"
        url = GlobalConfig.Url.value
        super(self.__class__, self).__init__(url, {}, method)
        self.headers = self.GetWebHeader()


class LoginPreReq(ServerReq):
    def __init__(self):
        method = "Get2"
        url = GlobalConfig.Url.value + "/login"
        super(self.__class__, self).__init__(url, {}, method)
        self.headers = self.GetWebHeader()


# 登陆
# class LoginReq(ServerReq):
#     def __init__(self, userId, passwd):
#         method = "POST"
#         url = GlobalConfig.Url.value + "/login"
#
#         header = self.GetHeader(url, method)
#         data = dict()
#         data["username"] = userId
#         data["password"] = passwd
#         data["submit_login"] = ""
#         super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 登陆
class LoginReq2(ServerReq):
    def __init__(self, userId, passwd):
        method = "POST"
        url = GlobalConfig.GetApiUrl() + "/login"
        data = dict()
        data["username"] = userId
        data["password"] = passwd
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 注册
class RegisterReq(ServerReq):
    def __init__(self, userId, email, passwd, passwd2, sex="Male",  ver=""):
        # [Male, Female]

        method = "POST2"
        url = GlobalConfig.Url.value + "/signup"
        data = dict()
        data["username"] = userId
        data["password"] = passwd
        data["email"] = email
        # data["uicode"] = ""
        data["verification"] = ver
        data["password_confirm"] = passwd2
        data["gender"] = sex
        data["age"] = "on"
        data["terms"] = "on"
        data["submit_signup"] = ""
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)
        self.headers = self.GetWebHeader()
        self.headers["referer"] = url

# 重新获取注册验证
class RegisterVerifyMailReq(ServerReq):
    def __init__(self, user, password):
        method = "POST2"
        url = GlobalConfig.Url.value + "/confirm"

        data = dict()
        data["username"] = user
        data["password"] = password
        data["submit_confirm"] = "發送EMAIL"
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)
        self.headers = self.GetWebHeader()
        self.headers["referer"] = url


# 重置密码
class ResetPasswordReq(ServerReq):
    def __init__(self, email):
        method = "POST2"
        url = GlobalConfig.Url.value + "/lost"

        data = dict()
        data["email"] = email
        data["submit_lost"] = "恢復密碼"
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)
        self.headers = self.GetWebHeader()
        self.headers["referer"] = url


# 验证码图片
class GetCaptchaReq(ServerReq):
    def __init__(self):
        method = "Get2"
        url = GlobalConfig.Url.value + "/captcha"

        data = dict()
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)
        self.headers = self.GetWebHeader()
        self.headers['Referer'] = GlobalConfig.Url.value  + "signup"


# 账号验证
class VerifyMailReq(ServerReq):
    def __init__(self, url):
        method = "GET2"
        host = ToolUtil.GetUrlHost(url)
        url = url.replace("\r", "").replace("\n", "").replace(" ", "").replace(host, ToolUtil.GetUrlHost(GlobalConfig.Url.value))

        super(self.__class__, self).__init__(url, {}, method)
        self.headers = self.GetWebHeader()

# 获得UserInfo
# class GetUserInfoReq(ServerReq):
#     def __init__(self):
#         method = "GET"
#         url = GlobalConfig.Url.value + "/user"
#
#         header = self.GetHeader(url, method)
#         data = dict()
#         super(self.__class__, self).__init__(url, header, data, method)


# 本子信息
# class GetBookInfoReq(ServerReq):
#     def __init__(self, bookId):
#         self.bookId = bookId
#         url = GlobalConfig.Url.value + "/album/{}".format(bookId)
#         method = "GET"
#         super(self.__class__, self).__init__(url, self.GetHeader(url, method), {}, method)


# 本子信息
class GetBookInfoReq2(ServerReq):
    def __init__(self, bookId):
        self.bookId = bookId
        url = GlobalConfig.GetApiUrl() + "/album"
        method = "GET"
        data = dict()
        data["comicName"] = ""
        data["id"] = bookId

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)


# 获得scramble_id
class GetBookEpsScrambleReq2(ServerReq):
    def __init__(self, bookId, epsIndex, epsId):
        self.bookId = bookId
        self.epsIndex = epsIndex
        url = GlobalConfig.GetApiUrl() + "/chapter_view_template"
        method = "GET"
        data = dict()
        data["id"] = epsId
        data["mode"] = "vertical"
        data["page"] = "0"
        data["app_img_shunt"] = "NaN"

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)
        self.headers = self.GetHeader2(url, method)


# 章节信息
class GetBookEpsInfoReq2(ServerReq):
    def __init__(self, bookId, epsId):
        self.bookId = bookId
        url = GlobalConfig.GetApiUrl() + "/chapter"
        method = "GET"
        data = dict()
        data["comicName"] = ""
        data["skip"] = ""
        data["id"] = epsId

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)


# 获取一个章节的图片地址
# class GetBookImgUrl(ServerReq):
#     def __init__(self, bookId, epsId):
#         from tools.book import BookMgr
#         book = BookMgr().GetBook(bookId)
#         epsInfo = book.pageInfo.epsInfo.get(epsId)
#         url = GlobalConfig.Url.value + epsInfo.epsUrl
#         method = "Get"
#         self.bookId = bookId
#         self.epsId = epsId
#         super(self.__class__, self).__init__(url, self.GetHeader(url, method), {}, method)


# 搜索请求
# class GetSearchReq(ServerReq):
#     def __init__(self, search, page=1, mainCategory="", subCategory="", sort="mr", sortDay="a"):
#         # sort []&t=t&o=tf
#
#         # 所有，今日，本周，本月
#         # t= [a, t, w, m]
#
#         # 最新，最多点击，最多图片, 最多爱心
#         # o = [mr, mv, mp, tf]
#
#         # 其他漫画，another
#         # 同人志, doujin, [汉化：chinese, 日语：japanese， CG:CG, cosplay:cosplay]
#         # 韩漫  hanman
#         # 美漫  meiman
#         # 短片 short, [汉化：chinese, 日语：japanese]
#         # 单本 single, [汉化：chinese, 日语：japanese]
#
#         data = {"search_query": search}
#
#         if page > 1:
#             data['page'] = str(page)
#         if sortDay:
#             data['t'] = sortDay
#         if sort:
#             data["o"] = sort
#         url = GlobalConfig.Url.value + "/search/photos"
#         if mainCategory:
#             url += "/" + mainCategory
#             if subCategory:
#                 url += "/sub/" + subCategory
#
#         param = ToolUtil.DictToUrl(data)
#         if param:
#             url += "/?" + param
#         method = "GET"
#         super(self.__class__, self).__init__(url, self.GetHeader(url, method),
#                                              {}, method)


# 搜索请求
class GetSearchReq2(ServerReq):
    def __init__(self, search, sort="mr", page=1):

        # 最新，最多点击，最多图片, 最多爱心
        # o = [mr, mv, mp, tf]

        data = dict()
        data["search_query"] = search
        if page > 1:
            data['page'] = str(page)
        if sort:
            data["o"] = sort
        url = GlobalConfig.GetApiUrl() + "/search"

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)


# 分類请求
class GetCategoryReq2(ServerReq):
    def __init__(self):
        url = GlobalConfig.GetApiUrl() + "/categories"
        data = dict()
        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)


# 分類搜索请求
class GetSearchCategoryReq2(ServerReq):
    def __init__(self, category="0", page=1, sort="mr"):
        # sort []&t=t&o=tf

        # 最新，总排行，月排行，周排行， 日排行，最多图片, 最多爱心
        # o = [mr, mv, mv_m, mv_w, mv_t, mp, tf]

        # 最新, 同人, 单本, 短篇， 其他，韩漫， 美漫， CosPlay， 3D
        # category = ["0", "doujin", "single", "short", "another", "hanman", "meiman", "doujin_cosplay", "3D"]

        url = GlobalConfig.GetApiUrl() + "/categories/filter"

        data = dict()

        if page > 1:
            data['page'] = str(page)
        if sort:
            data["o"] = sort

        if category:
            data["c"] = category

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)


# 获得首页
# class GetIndexInfoReq(ServerReq):
#     def __init__(self):
#         url = GlobalConfig.Url.value
#         method = "GET"
#         super(self.__class__, self).__init__(url, self.GetHeader(url, method),
#                                              {}, method)


# 获得首页
class GetIndexInfoReq2(ServerReq):
    def __init__(self, page="0"):
        url = GlobalConfig.GetApiUrl() + "/promote"
        method = "GET"
        data = dict()
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, {}, method)


# 获得最近更新
class GetLatestInfoReq2(ServerReq):
    def __init__(self, page="0"):
        url = GlobalConfig.GetApiUrl() + "/latest"
        method = "GET"
        data = dict()
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, {}, method)


# 获得收藏
class GetFavoritesReq2(ServerReq):
    def __init__(self, page=1, sort="mr", fid=""):
        # 收藏时间, 更新时间
        # o = [mr, mp]
        url = GlobalConfig.GetApiUrl() + "/favorite"
        method = "GET"
        data = dict()
        data["page"] = page
        if fid:
            data["folder_id"] = fid
        else:
            data["folder_id"] = "0"
        data["o"] = sort

        param = ToolUtil.DictToUrl(data)
        self.now = int(time.time())
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, {}, method)


# 添加收藏文件夹
class AddFavoritesFoldReq2(ServerReq):
    def __init__(self, name=""):
        url = GlobalConfig.GetApiUrl() + "/favorite_folder"
        method = "POST"
        data = dict()
        data["folder_name"] = name
        data["type"] = "add"
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 删除收藏文件夹
class DelFavoritesFoldReq2(ServerReq):
    def __init__(self, fid=""):
        url = GlobalConfig.GetApiUrl() + "/favorite_folder"
        method = "POST"
        data = dict()
        data["folder_id"] = fid
        data["type"] = "del"
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)

# 移动收藏文件夹
class MoveFavoritesFoldReq2(ServerReq):
    def __init__(self, bookId="", fid=""):
        url = GlobalConfig.GetApiUrl() + "/favorite_folder"
        method = "POST"
        data = dict()
        data["folder_id"] = fid
        data["type"] = "move"
        data["aid"] = bookId
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 添加收藏
class AddAndDelFavoritesReq2(ServerReq):
    def __init__(self, bookId=""):
        url = GlobalConfig.GetApiUrl() + "/favorite"
        method = "POST"
        data = dict()
        data["aid"] = bookId
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 获得收藏
# class GetFavoritesReq(ServerReq):
#     def __init__(self, page=1, sort="mr"):
#         # 收藏时间, 更新时间
#         # o = [mr, mp]
#         data = dict()
#         data["o"] = sort
#         if page > 1:
#             data['page'] = str(page)
#         param = ToolUtil.DictToUrl(data)
#         url = GlobalConfig.Url.value + "/user/" + config.LoginUserName + "/favorite/albums/?" + param
#         method = "GET"
#
#         super(self.__class__, self).__init__(url, self.GetHeader(url, method),
#                                              {}, method)


# 添加收藏
# class AddFavoritesReq(ServerReq):
#     def __init__(self, bookId=""):
#         url = GlobalConfig.Url.value + "/ajax/favorite_album"
#         method = "POST"
#         header = self.GetHeader(url, method)
#         data = dict()
#         data["album_id"] = bookId
#         data["fid"] = 0
#
#         header["origin"] = GlobalConfig.Url.value
#         header["referer"] = GlobalConfig.Url.value + "/album/{}/".format(bookId)
#         super(self.__class__, self).__init__(url, header,
#                                              ToolUtil.DictToUrl(data), method)


# 删除收藏
# class DelFavoritesReq(ServerReq):
#     def __init__(self, bookId=""):
#         url = GlobalConfig.Url.value + "/ajax/remove_album_playlist"
#         method = "POST"
#         header = self.GetHeader(url, method)
#         data = dict()
#         data["video_id"] = bookId
#         data["list"] = "favorites"
#         super(self.__class__, self).__init__(url, header,
#                                              ToolUtil.DictToUrl(data), method)


# 获得评论
class GetCommentReq2(ServerReq):
    def __init__(self, bookId="", page="1", readMode="manhua"):
        self.bookId = bookId
        url = GlobalConfig.GetApiUrl() + "/forum"
        method = "GET"
        data = dict()
        data["mode"] = readMode
        if bookId:
            data["aid"] = bookId
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)


# 获得评论
class GetMyCommentReq2(ServerReq):
    def __init__(self, uid, page="1"):
        self.uid = uid
        url = GlobalConfig.GetApiUrl() + "/forum"
        method = "GET"
        data = dict()
        data["mode"] = "undefined"
        data["uid"] = uid
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)


# 发送评论
class SendCommentReq2(ServerReq):
    def __init__(self, bookId="", comment="", cid=""):
        url = GlobalConfig.GetApiUrl() + "/comment"
        method = "POST"
        data = dict()
        data["comment"] = comment
        data["aid"] = bookId
        if cid:
            data["comment_id"] = cid
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 获取观看记录
class GetHistoryReq2(ServerReq):
    def __init__(self, page=1):
        url = GlobalConfig.GetApiUrl() + "/watch_list"
        method = "GET"
        data = dict()
        data["page"] = page
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# Jcoin购买
class GetBuyComicsReq2(ServerReq):
    def __init__(self, bookId=""):
        url = GlobalConfig.GetApiUrl() + "/coin_buy_comics"
        method = "POST"
        data = dict()
        data["id"] = bookId
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)

# 获取周推荐分类
class GetWeekCategoriesReq2(ServerReq):
    def __init__(self, page=0):
        url = GlobalConfig.GetApiUrl() + "/week"
        method = "GET"
        data = dict()
        data["page"] = page
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)


# 获取周推荐
class GetWeekFilterReq2(ServerReq):
    def __init__(self, id, type, page=0):
        url = GlobalConfig.GetApiUrl() + "/week/filter?"
        method = "GET"
        data = dict()
        data["page"] = page
        data["id"] = id
        data["type"] = type
        url = url + ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)


# 获取深夜食堂
class GetBlogsReq2(ServerReq):
    def __init__(self, blog_type="dinner", search_query="", page=1):
        url = GlobalConfig.GetApiUrl() + "/blogs?"
        method = "GET"
        data = dict()
        data["blog_type"] = blog_type
        data["page"] = page
        data["search_query"] = search_query
        url = url + ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)


# 获取深夜食堂
class GetBlogInfoReq2(ServerReq):
    def __init__(self, id):
        url = GlobalConfig.GetApiUrl() + "/blog?"
        method = "GET"
        data = dict()
        data["id"] = id
        url = url + ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)


# 获取深夜食堂
class GetBlogForumReq2(ServerReq):
    def __init__(self, bid, page=1, mode="blog"):
        url = GlobalConfig.GetApiUrl() + "/forum?"
        method = "GET"
        data = dict()
        data["bid"] = bid
        data["page"] = page
        data["mode"] = mode
        url = url + ToolUtil.DictToUrl(data)
        super(self.__class__, self).__init__(url, {}, method)

# 获取签到信息
class GetDailyReq2(ServerReq):
    def __init__(self, user_id):
        url = GlobalConfig.GetApiUrl() + "/daily?user_id=" + user_id
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)


# 签到
class SignDailyReq2(ServerReq):
    def __init__(self, user_id, daily_id):
        url = GlobalConfig.GetApiUrl() + "/daily_chk"
        method = "POST"
        data = dict()
        data["user_id"] = user_id
        data["daily_id"] = daily_id
        super(self.__class__, self).__init__(url, ToolUtil.DictToUrl(data), method)



# 查看评论
# class LookCommentReq(ServerReq):
#     def __init__(self, bookId="", page=1):
#         data = dict()
#         if bookId:
#             # 漫画评论
#             url = GlobalConfig.Url.value + "/ajax/album_pagination"
#             data["video_id"] = bookId
#         else:
#             # 全部评论
#             url = GlobalConfig.Url.value + "/ajax/forum_more"
#         method = "POST"
#         header = self.GetHeader(url, method)
#
#         data["page"] = page
#         super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 回复评论
# class ReplySubCommentReq(ServerReq):
#     def __init__(self, replyId="", comment=""):
#         url = GlobalConfig.Url.value + "/ajax/forum_more"
#         method = "POST"
#         header = self.GetHeader(url, method)
#         data = dict()
#         data["comment_id"] = replyId
#         data["comment"] = comment
#         data["forum_subject"] = 1
#         data["originator"] = ""
#         data["is_reply"] = 1
#         data["video_id"] = 0
#         super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)

# Doh域名解析
class DnsOverHttpsReq(ServerReq):
    def __init__(self, domain="", dohAddress=""):
        url = dohAddress + "?name={}&type=A".format(ToolUtil.GetUrlHost(domain))
        method = "GET"
        header = dict()
        header["accept"] = "application/dns-json"
        header["Content-Type"] = "application/dns-json"
        super(self.__class__, self).__init__(url, {}, method)
        self.timeout = 5
        self.headers = header
        self.isParseRes = True


# Doh域名解析
class GetEchConfigReq(ServerReq):
    TYPE_HTTPS = 65

    @staticmethod
    def build_dns_query(domain: str, qtype: int) -> bytes:
        parts = [b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"]
        for label in domain.split("."):
            label_bytes = label.encode("idna")
            parts.append(bytes([len(label_bytes)]))
            parts.append(label_bytes)
        parts.append(b"\x00")
        parts.append(struct.pack("!HH", qtype, 1))
        return b"".join(parts)

    @staticmethod
    def _skip_dns_name(packet: bytes, offset: int) -> int:
        while offset < len(packet):
            length = packet[offset]
            if length & 0xC0 == 0xC0:
                return offset + 2
            if length == 0:
                return offset + 1
            offset += length + 1
        return offset

    @staticmethod
    def parse_https_record(data: bytes) -> str:
        if len(data) < 2:
            return ""
        offset = 2
        if offset < len(data) and data[offset] == 0:
            offset += 1
        else:
            offset = GetEchConfigReq._skip_dns_name(data, offset)
        while offset + 4 <= len(data):
            key, length = struct.unpack("!HH", data[offset: offset + 4])
            offset += 4
            if offset + length > len(data):
                break
            value = data[offset: offset + length]
            offset += length
            if key == 5:
                return base64.b64encode(value).decode("ascii")
        return ""

    @staticmethod
    def parse_dns_response(response: bytes) :
        if len(response) < 12:
            return ""
        ancount = struct.unpack("!H", response[6:8])[0]
        if ancount == 0:
            return ""

        offset = GetEchConfigReq._skip_dns_name(response, 12) + 4
        for _ in range(ancount):
            offset = GetEchConfigReq._skip_dns_name(response, offset)
            if offset + 10 > len(response):
                break
            rr_type = struct.unpack("!H", response[offset : offset + 2])[0]
            offset += 8
            data_len = struct.unpack("!H", response[offset : offset + 2])[0]
            offset += 2
            if offset + data_len > len(response):
                break
            data = response[offset : offset + data_len]
            offset += data_len
            if rr_type == GetEchConfigReq.TYPE_HTTPS:
                ech = GetEchConfigReq.parse_https_record(data)
                if ech:
                    return ech
        return ""

    def __init__(self, domain="", dohAddress=None):
        url = dohAddress[0]
        method = "POST"
        super(self.__class__, self).__init__(url, {}, method)
        headers = {
                    "Accept": "application/dns-message",
                   "Content-Type": "application/dns-message"
        }
        self.timeout = 5
        self.params = self.build_dns_query(domain, GetEchConfigReq.TYPE_HTTPS)
        self.headers = headers
        self.isParseRes = False
        self.resetUrl = dohAddress[1:]
        self.resetCnt = len(dohAddress)
        # self.resetUrl = ["https://parse.jpacg.cc/jmserve", "https://parse2.jpacg.cc/jmserve"]
        # self.resetCnt = 3

# 测试Ping
class SpeedTestPingReq(ServerReq):
    def __init__(self, url):
        url = url + "/latest"
        data = dict()
        data["page"] = "0"

        method = "GET"
        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, {}, method)
        self.headers['cache-control'] = 'no-cache'
        self.headers['expires'] = '0'
        self.headers['pragma'] = 'no-cache'
        self.headers["authorization"] = ""
        self.isReload = False
        self.timeout = 3


# 测试Ping
class SpeedTestPing2Req(ServerReq):
    def __init__(self, url):
        url = url + "/cdn-cgi/trace"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)
        self.headers['cache-control'] = 'no-cache'
        self.headers['expires'] = '0'
        self.headers['pragma'] = 'no-cache'
        self.headers["authorization"] = ""
        self.isReload = False
        self.timeout = 3


class SpeedTestReq(ServerReq):
    Index = 0
    URLS = [
        # "/media/photos/295840/00001.jpg"
        # "/media/photos/295840/00002.jpg",
        "/media/photos/292840/00002.webp",
        # "/media/photos/295840/00004.jpg",
    ]

    def __init__(self):
        url = SpeedTestReq.URLS[SpeedTestReq.Index]
        SpeedTestReq.Index += 1
        if SpeedTestReq.Index >= len(SpeedTestReq.URLS):
            SpeedTestReq.Index = 0

        url = GlobalConfig.GetImgUrl() + url
        method = "Download"
        super(self.__class__, self).__init__(url, {}, method)
        self.headers['cache-control'] = 'no-cache'
        self.headers['expires'] = '0'
        self.headers['pragma'] = 'no-cache'
        self.isReload = False
        self.resetCnt = 2
        self.isReset = False


class GetJmServerReq(ServerReq):
    def __init__(self):
        url = GlobalConfig.JMServerUrl.value
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)
        self.resetUrl = ["https://parse.jpacg.cc/jmserve", "https://parse2.jpacg.cc/jmserve"]
        self.resetCnt = 3
        self.timeout = 5


# 通过cf优选ip
class GetCfDnsReq(ServerReq):
    def __init__(self, domain):
        domain = ToolUtil.GetUrlHost(domain)
        url = "https://macapi1.com/app/picacomic/dns/resolve?domain={}".format(domain)
        method = "Get"
        self.domain = domain
        super(self.__class__, self).__init__(url, {}, method)


# Doh域名解析
class GetIpInfoReq(ServerReq):
    def __init__(self, ip):
        url = f"https://parse.jpacg.cc/ipinfo?ip={ip}"
        method = "GET"
        super(self.__class__, self).__init__(url, {}, method)
        self.timeout = 5
        self.headers = {
            "version": config.UpdateVersion
        }
        self.isParseRes = False
        self.resetUrl = [f"https://parse2.jpacg.cc/ipinfo?ip={ip}"]
        self.resetCnt = 2