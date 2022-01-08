import json
import time

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


# 检查更新
class CheckUpdateReq(ServerReq):
    def __init__(self, url):
        # url = config.UpdateUrl
        method = "GET"
        super(self.__class__, self).__init__(url, {}, {}, method)
        self.isParseRes = False


# 下载图片
class DownloadBookReq(ServerReq):
    def __init__(self, url, loadPath="", cachePath="", savePath="", saveParam=(0, 0, "")):
        url = config.PicUrl2 + url
        method = "Download"
        self.url = url
        self.loadPath = loadPath
        self.cachePath = cachePath
        self.savePath = savePath
        self.saveParam = saveParam
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 注册前，需要获取cookie
class LoginPreReq(ServerReq):
    def __init__(self):
        method = "Get"
        url = config.Url + "/login"
        header = ToolUtil.GetHeader(url, method)
        super(self.__class__, self).__init__(url, header, {}, method)


# 登陆
# class LoginReq(ServerReq):
#     def __init__(self, userId, passwd):
#         method = "POST"
#         url = config.Url + "/login"
#
#         header = ToolUtil.GetHeader(url, method)
#         data = dict()
#         data["username"] = userId
#         data["password"] = passwd
#         data["submit_login"] = ""
#         super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 登陆
class LoginReq2(ServerReq):
    def __init__(self, userId, passwd):
        method = "POST"
        url = config.Url2 + "/login"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["username"] = userId
        data["password"] = passwd
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 注册
class RegisterReq(ServerReq):
    def __init__(self, userId, email, passwd, passwd2, sex="Male"):
        # [Male, Female]

        method = "POST"
        url = config.Url + "/signup"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["username"] = userId
        data["password"] = passwd
        data["email"] = email
        data["password_confirm"] = passwd2
        data["gender"] = sex
        data["age"] = "on"
        data["terms"] = "on"
        data["submit_signup"] = ""
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 重新获取注册验证
class RegisterVerifyMailReq(ServerReq):
    def __init__(self, email):
        method = "POST"
        url = config.Url + "/confirm"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["email"] = email
        data["submit_confirm"] = "發送EMAIL"
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 重置密码
class ResetPasswordReq(ServerReq):
    def __init__(self, email):
        method = "POST"
        url = config.Url + "/lost"

        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["email"] = email
        data["submit_lost"] = "恢復密碼"
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 账号验证
class VerifyMailReq(ServerReq):
    def __init__(self, url):
        method = "GET"
        host = ToolUtil.GetUrlHost(url)
        url = url.replace(host, ToolUtil.GetUrlHost(config.Url))

        header = ToolUtil.GetHeader(url, method)
        super(self.__class__, self).__init__(url, header, {}, method)


# 获得UserInfo
# class GetUserInfoReq(ServerReq):
#     def __init__(self):
#         method = "GET"
#         url = config.Url + "/user"
#
#         header = ToolUtil.GetHeader(url, method)
#         data = dict()
#         super(self.__class__, self).__init__(url, header, data, method)


# 本子信息
# class GetBookInfoReq(ServerReq):
#     def __init__(self, bookId):
#         self.bookId = bookId
#         url = config.Url + "/album/{}".format(bookId)
#         method = "GET"
#         super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


# 本子信息
class GetBookInfoReq2(ServerReq):
    def __init__(self, bookId):
        self.bookId = bookId
        url = config.Url2 + "/album"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["comicName"] = ""
        data["id"] = bookId

        param = ToolUtil.DictToUrl(data)
        self.now = int(time.time())
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, header, {}, method)


# 获得scramble_id
class GetBookEpsScrambleReq2(ServerReq):
    def __init__(self, bookId, epsIndex, epsId):
        self.bookId = bookId
        self.epsIndex = epsIndex
        url = config.Url2 + "/chapter_view_template"
        method = "GET"
        data = dict()
        data["id"] = epsId
        data["mode"] = "vertical"
        data["page"] = "0"
        data["app_img_shunt"] = "NaN"

        param = ToolUtil.DictToUrl(data)
        header = ToolUtil.GetHeader2(url, method)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, header, {}, method)


# 章节信息
class GetBookEpsInfoReq2(ServerReq):
    def __init__(self, bookId, epsId):
        self.bookId = bookId
        url = config.Url2 + "/chapter"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["comicName"] = ""
        data["skip"] = ""
        data["id"] = epsId

        param = ToolUtil.DictToUrl(data)
        self.now = int(time.time())
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, header, {}, method)


# 获取一个章节的图片地址
# class GetBookImgUrl(ServerReq):
#     def __init__(self, bookId, epsId):
#         from tools.book import BookMgr
#         book = BookMgr().GetBook(bookId)
#         epsInfo = book.pageInfo.epsInfo.get(epsId)
#         url = config.Url + epsInfo.epsUrl
#         method = "Get"
#         self.bookId = bookId
#         self.epsId = epsId
#         super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method), {}, method)


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
#         url = config.Url + "/search/photos"
#         if mainCategory:
#             url += "/" + mainCategory
#             if subCategory:
#                 url += "/sub/" + subCategory
#
#         param = ToolUtil.DictToUrl(data)
#         if param:
#             url += "/?" + param
#         method = "GET"
#         super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
#                                              {}, method)


# 搜索请求
class GetSearchReq2(ServerReq):
    def __init__(self, search, sort="mr", page=1):

        # 最新，最多点击，最多图片, 最多爱心
        # o = [mr, mv, mp, tf]

        data = dict()
        data["search_query"] = search
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        if page > 1:
            data['page'] = str(page)
        if sort:
            data["o"] = sort
        url = config.Url2 + "/search"

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 分類请求
class GetCategoryReq2(ServerReq):
    def __init__(self):
        url = config.Url2 + "/categories"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        method = "GET"
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 分類搜索请求
class GetSearchCategoryReq2(ServerReq):
    def __init__(self, category="0", page=1, sort="mr"):
        # sort []&t=t&o=tf

        # 最新，总排行，月排行，周排行， 日排行，最多图片, 最多爱心
        # o = [mr, mv, mv_m, mv_w, mv_t, mp, tf]

        # 最新, 同人, 单本, 短篇， 其他，韩漫， 美漫， CosPlay， 3D
        # category = ["0", "doujin", "single", "short", "another", "hanman", "meiman", "doujin_cosplay", "3D"]

        url = config.Url2 + "/categories/filter"

        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"

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
        super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
                                             {}, method)


# 获得首页
# class GetIndexInfoReq(ServerReq):
#     def __init__(self):
#         url = config.Url
#         method = "GET"
#         super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
#                                              {}, method)


# 获得首页
class GetIndexInfoReq2(ServerReq):
    def __init__(self, page="0"):
        url = config.Url2 + "/promote"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, header,
                                             {}, method)


# 获得最近更新
class GetLatestInfoReq2(ServerReq):
    def __init__(self, page="0"):
        url = config.Url2 + "/latest"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, header,
                                             {}, method)


# 获得收藏
class GetFavoritesReq2(ServerReq):
    def __init__(self, page=1, sort="mr", fid=""):
        # 收藏时间, 更新时间
        # o = [mr, mp]
        url = config.Url2 + "/favorite"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["page"] = page
        if fid:
            data["folder_id"] = fid
        data["o"] = sort

        param = ToolUtil.DictToUrl(data)
        self.now = int(time.time())
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param

        super(self.__class__, self).__init__(url, header,
                                             {}, method)


# 添加收藏文件夹
class AddFavoritesFoldReq2(ServerReq):
    def __init__(self, name=""):
        url = config.Url2 + "/favorite_folder"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["folder_name"] = name
        data["view_mode"] = "null"
        data["type"] = "add"
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


# 删除收藏文件夹
class DelFavoritesFoldReq2(ServerReq):
    def __init__(self, fid=""):
        url = config.Url2 + "/favorite_folder"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["folder_id"] = fid
        data["view_mode"] = "null"
        data["type"] = "del"
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)

# 移动收藏文件夹
class MoveFavoritesFoldReq2(ServerReq):
    def __init__(self, bookId="", fid=""):
        url = config.Url2 + "/favorite_folder"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["folder_id"] = fid
        data["view_mode"] = "null"
        data["type"] = "move"
        data["aid"] = bookId
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


# 添加收藏
class AddAndDelFavoritesReq2(ServerReq):
    def __init__(self, bookId=""):
        url = config.Url2 + "/favorite"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["aid"] = bookId
        super(self.__class__, self).__init__(url, header,
                                             ToolUtil.DictToUrl(data), method)


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
#         url = config.Url + "/user/" + config.LoginUserName + "/favorite/albums/?" + param
#         method = "GET"
#
#         super(self.__class__, self).__init__(url, ToolUtil.GetHeader(url, method),
#                                              {}, method)


# 添加收藏
# class AddFavoritesReq(ServerReq):
#     def __init__(self, bookId=""):
#         url = config.Url + "/ajax/favorite_album"
#         method = "POST"
#         header = ToolUtil.GetHeader(url, method)
#         data = dict()
#         data["album_id"] = bookId
#         data["fid"] = 0
#
#         header["origin"] = config.Url
#         header["referer"] = config.Url + "/album/{}/".format(bookId)
#         super(self.__class__, self).__init__(url, header,
#                                              ToolUtil.DictToUrl(data), method)


# 删除收藏
# class DelFavoritesReq(ServerReq):
#     def __init__(self, bookId=""):
#         url = config.Url + "/ajax/remove_album_playlist"
#         method = "POST"
#         header = ToolUtil.GetHeader(url, method)
#         data = dict()
#         data["video_id"] = bookId
#         data["list"] = "favorites"
#         super(self.__class__, self).__init__(url, header,
#                                              ToolUtil.DictToUrl(data), method)


# 获得评论
class GetCommentReq2(ServerReq):
    def __init__(self, bookId="", page="1"):
        self.bookId = bookId
        url = config.Url2 + "/forum"
        method = "GET"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["mode"] = "manhua"
        if bookId:
            data["aid"] = bookId
        data["page"] = page

        param = ToolUtil.DictToUrl(data)
        header = ToolUtil.GetHeader(url, method)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, header, {}, method)


# 发送评论
class SendCommentReq2(ServerReq):
    def __init__(self, bookId="", comment="", cid=""):
        url = config.Url2 + "/comment"
        method = "POST"
        header = ToolUtil.GetHeader(url, method)
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["comment"] = comment
        data["aid"] = bookId
        if cid:
            data["comment_id"] = cid
        super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)

# 查看评论
# class LookCommentReq(ServerReq):
#     def __init__(self, bookId="", page=1):
#         data = dict()
#         if bookId:
#             # 漫画评论
#             url = config.Url + "/ajax/album_pagination"
#             data["video_id"] = bookId
#         else:
#             # 全部评论
#             url = config.Url + "/ajax/forum_more"
#         method = "POST"
#         header = ToolUtil.GetHeader(url, method)
#
#         data["page"] = page
#         super(self.__class__, self).__init__(url, header, ToolUtil.DictToUrl(data), method)


# 回复评论
# class ReplySubCommentReq(ServerReq):
#     def __init__(self, replyId="", comment=""):
#         url = config.Url + "/ajax/forum_more"
#         method = "POST"
#         header = ToolUtil.GetHeader(url, method)
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
    def __init__(self):
        url = config.Url2 + "/latest"
        data = dict()
        data["key"] = "0b931a6f4b5ccc3f8d870839d07ae7b2"
        data["view_mode_debug"] = "1"
        data["view_mode"] = "null"
        data["page"] = "0"

        method = "GET"
        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        header["authorization"] = ""

        param = ToolUtil.DictToUrl(data)
        if param:
            url += "/?" + param
        super(self.__class__, self).__init__(url, header,
                                             {}, method)


class SpeedTestReq(ServerReq):
    Index = 0
    URLS = [
        "/media/photos/295840/00001.jpg",
        "/media/photos/295840/00002.jpg",
        "/media/photos/295840/00003.jpg",
        "/media/photos/295840/00004.jpg",
    ]

    def __init__(self):
        url = SpeedTestReq.URLS[SpeedTestReq.Index]
        SpeedTestReq.Index += 1
        if SpeedTestReq.Index >= len(SpeedTestReq.URLS):
            SpeedTestReq.Index = 0

        url = config.PicUrl2 + url
        method = "Download"
        header = ToolUtil.GetHeader(url, method)
        header['cache-control'] = 'no-cache'
        header['expires'] = '0'
        header['pragma'] = 'no-cache'
        super(self.__class__, self).__init__(url, header,
                                             {}, method)