import asyncio
from contextlib import suppress
import copy
import json
import os
import pickle
import re
import time
from datetime import timedelta

from curl_cffi.requests import exceptions

from config import config
from config.global_config import GlobalConfig
from config.setting import Setting
from task.qt_task import TaskBase
from server import req
from task.task_cache import TaskCache
from task.task_multi import TaskMulti
from tools.status import Status
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil
from .error import ClassifyRequestError
from .server import handler, Task, Server
from curl_cffi import requests as requests2, CurlInfo


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return
            verData = task.res.GetText()
            info = verData.replace("v", "").split(".")
            if len(info) >= 4:
                version = int(info[0]) * 1000 + int(info[1]) * 100 + int(info[2]) * 10 + int(info[3]) * 1
            else:
                version = int(info[0]) * 1000 + int(info[1]) * 100 + int(info[2]) * 10

            info2 = re.findall(r"\d+\d*", os.path.basename(config.RealVersion))
            if len(info2) >= 4:
                curversion = int(info2[0]) * 1000 + int(info2[1]) * 100 + int(info2[2]) * 10 + int(info2[3]) * 1
            else:
                curversion = int(info2[0]) * 1000 + int(info2[1]) * 100 + int(info2[2]) * 10
            from config.setting import Setting
            if not Setting.IsPreUpdate.value:
                version //= 10
                curversion //= 10

            if version > curversion:
                data["data"] = verData.replace("\r\n", "").replace("\n", "")
            else:
                data["data"] = "no"
        except Exception as es:
            pass
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.CheckUpdateInfoReq)
class CheckUpdateInfoHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                data["st"] = Str.NotFound
                return

            raw = task.res.GetText()
            data["data"] = raw
            if not raw:
                data["st"] = Str.NotFound
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.CheckUpdateConfigReq)
class CheckUpdateConfigHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                data["st"] = Str.NotFound
                return
            raw = task.res.GetText()
            data["data"] = raw
            if not raw:
                data["st"] = Str.NotFound
        except Exception as es:
            pass
        finally:
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))

# @handler(req.GetUserInfoReq)
# class GetUserInfoReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             user = ToolUtil.ParseUserInfo(task.res.raw.content)
#             if user:
#                 data["st"] = Status.Ok
#                 data["user"] = user
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.LoginPreReq)
class LoginPreHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return

            cookie_dict = {}
            for cookie in task.res.raw.cookies.jar:
                cookie_dict[cookie.name] = cookie.value
            # print(cookies)
            Log.Info("get pre cookies, {}, code:{}".format(list(cookie_dict.keys()), task.res.code))

        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.LoginCheck301Req)
class LoginCheck301Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status, "msg": ""}
        try:
            if task.status != Status.Ok:
                return
            if task.res.raw.status_code != 200:
                data["msg"] = task.req.GetWebError(task.res.GetText())

            cookie_dict = {}
            for cookie in task.res.raw.cookies.jar:
                cookie_dict[cookie.name] = cookie.value
                # print(cookies)
            Log.Info("get pre cookies, {}, code:{}".format(list(cookie_dict.keys()), task.res.code))
            url = "https://" + ToolUtil.GetUrlHost(task.res.raw.url)

            ## 如果发生了301跳转，必须设置为新的域名，否则无法注册
            if url != GlobalConfig.Url.value:
                Log.Warn("Login url change, url:{}->{}".format(GlobalConfig.Url.value, url))
                # GlobalConfig.SetSetting("Url", url)

            # for raw in task.res.raw.history:
            #     cookies = requests.utils.dict_from_cookiejar(raw.cookies)
            #     print(cookies)

        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetCaptchaReq)
class GetCaptchaReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status, "content": task.res.GetContent(), "msg": ""}
        try:
            if task.status != Status.Ok:
                return
            if task.res.raw.status_code != 200:
                data["st"] = Status.Error
                data["msg"] = task.req.GetWebError(task.res.GetText())

            desUrl = ToolUtil.GetUrlHost(task.res.raw.url)
            srcUrl = ToolUtil.GetUrlHost(task.req.url)
            if desUrl != srcUrl:
                data['desUrl'] = desUrl

        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))

# @handler(req.LoginReq)
@handler(req.RegisterReq)
@handler(req.RegisterVerifyMailReq)
@handler(req.VerifyMailReq)
@handler(req.ResetPasswordReq)
class ParseMsgHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status, "msg": ""}
        try:
            if task.status != Status.Ok:
                return
            isSuc, msg = ToolUtil.ParseMsg(task.res.raw.content)
            if isinstance(task.req, req.RegisterReq):
                desUrl = ToolUtil.GetUrlHost(task.res.raw.url)
                srcUrl = ToolUtil.GetUrlHost(task.req.url)
                if msg == "" and not isSuc and desUrl != srcUrl:
                    msg = "出现301跳转{}, 无法注册, 请切换域名".format(desUrl)
                    data['desUrl'] = desUrl

            data["msg"] = msg
            if isSuc:
                st = Status.Ok
                data["st"] = st
            else:
                if task.res.raw.status_code != 200:
                    data["msg"] = task.req.GetWebError(task.res.GetText())

                data["st"] = Status.Error
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.LoginReq2)
class LoginReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                Log.Warn("登陆失败！！！, code:{}, text:{}".format(str(task.res.code), task.res.GetText()))
                return
            user = ToolUtil.ParseLogin2(task.req.ParseData(v.get("data")))

            cookie_dict = {}
            for cookie in task.res.raw.cookies.jar:
                cookie_dict[cookie.name] = cookie.value

            # cookies = task.res.raw.cookies

            # ipcountry = cookies.get("ipcountry", "")
            # ipm5 = cookies.get("ipm5", "")
            # AVS = cookies.get("AVS", "")
            # shunt = cookies.get("shunt", "")
            # config.ipcountry = ipcountry if ipcountry else config.ipcountry
            # config.ipm5 = ipm5 if ipm5 else config.ipm5
            # config.AVS = AVS if AVS else config.AVS
            # config.shunt = shunt if shunt else config.shunt
            Log.Info("Login suc, user_id:{}, cookie_keys:{}".format(user.uid, list(cookie_dict.keys())))
            st = Status.Ok
            user.cookie = cookie_dict
            data["st"] = st
            data["user"] = user
        except Exception as es:
            data["st"] = Status.ParseError
            data['errorMsg'] = task.res.GetText()
            Log.Warn("登陆失败！！！, code:{}, text:{}".format(str(task.res.code), task.res.GetText()))
            Log.Error(es)
        finally:

            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.GetIndexInfoReq)
# class GetIndexInfoReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             bookList = ToolUtil.ParseIndex(task.res.raw.content)
#             from tools.book import BookMgr
#             BookMgr().UpdateBookInfoList(bookList)
#             data["st"] = Status.Ok
#             data["bookList"] = bookList
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetIndexInfoReq2)
class GetIndexInfoReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            cookies = task.res.raw.cookies
            cookie_keys = list(cookies.keys()) if hasattr(cookies, "keys") else []
            Log.Info("latest suc, cookie_keys:{}".format(cookie_keys))
            infos = ToolUtil.ParseIndex2(task.req.ParseData(v.get("data")))

            data["st"] = Status.Ok
            data["infos"] = infos
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetLatestInfoReq2)
class GetLatestInfoReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return

            bookInfo = ToolUtil.ParseLatest2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["bookList"] = bookInfo
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetFavoritesReq2)
class GetFavoritesReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            f = ToolUtil.ParseFavoritesReq2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["favorite"] = f
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.AddFavoritesFoldReq2)
@handler(req.DelFavoritesFoldReq2)
@handler(req.MoveFavoritesFoldReq2)
@handler(req.AddAndDelFavoritesReq2)
class ParseMsgReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            st, msg = ToolUtil.ParseMsgReq2(task.req.ParseData(v.get("data")))
            data["st"] = st
            data["message"] = msg
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.LookCommentReq)
# class LookCommentReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             comments = ToolUtil.ParseComment(task.res.raw.content)
#             data["st"] = Status.Ok
#             data["comments"] = comments
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.LookCommentReq)
# class LookCommentReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             resData = json.loads(task.res.raw.content)
#             msg = resData.get("message", [])
#             comments = ToolUtil.ParseComment("\n".join(msg))
#             data["st"] = Status.Ok
#             data["comments"] = comments
#             data["page"] = resData.get("page", 1)
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.GetSearchReq)
# class GetSearchReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             maxPages, bookList = ToolUtil.ParseSearch(task.res.raw.content)
#             data["st"] = Status.Ok
#             data["maxPages"] = maxPages
#             data["bookList"] = bookList
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetSearchReq2)
class GetSearchReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return

            total, bookList = ToolUtil.ParseSearch2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["total"] = total
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetCategoryReq2)
class GetCategoryReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return

            categoryList, categoryTitle = ToolUtil.ParseCategory2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["categoryList"] = categoryList
            data["categoryTitle"] = categoryTitle
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetSearchCategoryReq2)
class GetSearchCategoryReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return

            total, bookList = ToolUtil.ParseSearchCategory2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["total"] = total
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.GetFavoritesReq)
# class GetFavoritesReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             curNum, maxNum, bookList = ToolUtil.ParseFavorite(task.res.raw.content)
#             data["st"] = Status.Ok
#             data["curNum"] = curNum
#             data["maxNum"] = maxNum
#             data["bookList"] = bookList
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.GetBookInfoReq)
# class GetBookInfoReqHandler(object):
#     def __call__(self, task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             isFavorite, info = ToolUtil.ParseBookInfo(task.res.raw.content, task.req.bookId)
#             from tools.book import BookMgr
#             BookMgr().UpdateBookInfo(task.req.bookId, info)
#             data["st"] = Status.Ok
#             data["isFavorite"] = isFavorite
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookInfoReq2)
class GetBookInfoReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            if task.res.raw.status_code != 200:
                data["st"] = Status.Error
                msg = task.res.GetText()
                data["message"] = msg
                Log.Warn("GetBookInfoReq2 error, book_id={}, code={}, msg={}".format(task.req.bookId, task.res.raw.status_code, msg))
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            info, isFavorite = ToolUtil.ParseBookInfo2(task.req.ParseData(v.get("data")))
            from tools.book import BookMgr
            BookMgr().UpdateBookInfo(task.req.bookId, info)
            data["st"] = Status.Ok
            data["isFavorite"] = isFavorite
            data["bookInfo"] = info
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.ReadBookInfoReq2)
class ReadBookInfoReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            epsInfo = ToolUtil.ParseReadBook2(task.req.ParseData(v.get("data")))
            epsInfo.index = task.req.epsIndex
            from tools.book import BookMgr
            BookMgr().UpdateBookEps(task.req.bookId, epsInfo)
            data["st"] = Status.Ok
            data["epsInfo"] = epsInfo
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookEpsScrambleReq2)
class GetBookEpsScrambleReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            scrambleId = ToolUtil.ParseBookEpsScramble(task.res.raw.content)
            from tools.book import BookMgr
            BookMgr().UpdateBookEpsScrambleId(task.req.bookId, task.req.epsIndex, scrambleId)
            data["st"] = Status.Ok
            data["scrambleId"] = scrambleId
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookEpsInfoReq2)
class GetBookEpsInfoReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            # jm2接口，已淘汰
            # epsInfo = ToolUtil.ParseBookEpsInfo2(task.req.ParseData(v.get("data")))
            # epsInfo.index = task.req.epsIndex
            # from tools.book import BookMgr
            # BookMgr().UpdateBookEps(task.req.bookId, epsInfo)
            data["st"] = Status.Ok
            # data["epsInfo"] = epsInfo
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetCommentReq2)
@handler(req.GetMyCommentReq2)
class GetCommentReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            commentList, total = ToolUtil.ParseBookComment(task.req.ParseData(v.get("data")))
            # from tools.book import BookMgr
            # BookMgr().UpdateBookInfo(task.req.bookId, info)
            data["st"] = Status.Ok
            data["commentList"] = commentList
            data["total"] = total
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.SendCommentReq2)
class SendCommentReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            msg = ToolUtil.ParseSendBookComment(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["message"] = msg
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetHistoryReq2)
class GetHistoryReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            bookList, total = ToolUtil.ParseHistoryReq2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["total"] = total
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetSerializationReq2)
class GetSerializationReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            bookList, total = ToolUtil.ParseSerializationReq2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["total"] = total
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.RandomRecommendReq2)
class RandomRecommendReq2Handler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            bookList, total = ToolUtil.ParseRandomRecommendReq2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["total"] = total
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetWeekCategoriesReq2)
@handler(req.GetWeekFilterReq2)
@handler(req.GetBlogsReq2)
@handler(req.GetBlogInfoReq2)
@handler(req.GetBlogForumReq2)
@handler(req.SignDailyReq2)
@handler(req.GetDailyReq2)
@handler(req.GetBuyComicsReq2)
class GetReqRawDataHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.content)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            if not v.get("data"):
                data["data"] = {}
                return

            data2 = json.loads(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["data"] = data2
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.GetBookImgUrl)
# class GetBookImgUrlReqHandler(object):
#     def __call__(self, task: Task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             aid, minAid, pictureUrl, pictureName = ToolUtil.ParsePictureUrl(task.res.raw.content)
#             from tools.book import BookMgr
#             BookMgr().UpdateBookPicture(task.req.bookId, task.req.epsId, aid, minAid, pictureUrl, pictureName)
#             data["st"] = Status.Ok
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.AddFavoritesReq)
# class AddFavoritesReqHandler(object):
#     def __call__(self, task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             resData = json.loads(task.res.raw.content)
#             if resData.get("status") == 1:
#                 data["st"] = Status.Ok
#             else:
#                 data["st"] = Status.Error
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


# @handler(req.DelFavoritesReq)
# class DelFavoritesReqHandler(object):
#     def __call__(self, task):
#         data = {"st": task.status}
#         try:
#             if task.status != Status.Ok:
#                 return
#             resData = json.loads(task.res.raw.content)
#             if resData.get("status") == 1:
#                 data["st"] = Status.Ok
#             else:
#                 data["st"] = Status.Error
#         except Exception as es:
#             data["st"] = Status.ParseError
#             Log.Error(es)
#         finally:
#             if task.backParam:
#                 TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


async def _CloseStreamResponse(r, finished: bool):
    if not finished:
        quitNow = getattr(r, "quit_now", None)
        if quitNow is not None:
            quitNow.set()
        streamTask = getattr(r, "astream_task", None)
        if streamTask is not None and not streamTask.done():
            streamTask.cancel()
            with suppress(asyncio.CancelledError, Exception):
                await streamTask
            return
    with suppress(asyncio.CancelledError, Exception):
        await r.aclose()


@handler(req.DownloadBookReq)
class DownloadBookHandler(object):
    async def __call__(self, backData):
        task = backData
        ttfb_time = 0
        status_code = 0
        totalSize = 0
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.backParam, -backData.status, 0, b"")
            return

        fileSize = 0
        request = backData.req
        index = backData.index
        cfHit = False
        isFail = False
        data = b""
        try:
            try:
                r = await task.session.get(
                    request.url,
                    headers=request.headers,
                    timeout=None,
                    proxies=request.proxy,
                    stream=True,
                )
                streamFinished = False
                try:
                    ttfb_time = r.infos.get(CurlInfo.STARTTRANSFER_TIME)
                    status_code = r.status_code
                    cfHit = r.headers.get("cf-cache-status", False)

                    if r.status_code == 404 or r.status_code == 403:
                        backData.status = Status.Error
                        ## 404 尝试切换图片地址
                        isReset = backData.req.ResetToSwitchNextUrl()
                        if isReset and backData.req.resetCnt >= 0:
                            backData.req.isReset = True
                            if backData.backParam:
                                TaskBase.taskObj.downloadBack.emit(backData.backParam, -Status.Resetting, fileSize, b"")
                            Server().ReDownload(backData)
                            return
                        else:
                            if backData.backParam:
                                TaskBase.taskObj.downloadBack.emit(backData.backParam, -Status.Error, fileSize, b"")
                            return
                    elif r.status_code != 200:
                        backData.status = Status.Error
                        if backData.backParam:
                            TaskBase.taskObj.downloadBack.emit(backData.backParam, -Status.Error, fileSize, b"")
                        return

                    contentLen = r.headers.get("Content-Length") or r.headers.get("content-length")
                    try:
                        expectedSize = int(contentLen) if contentLen is not None else 1024 * 512
                    except (TypeError, ValueError):
                        expectedSize = 1024 * 512

                    buf = bytearray()
                    send = 0
                    now = time.time()
                    async for chunk in r.aiter_content():
                        buf.extend(chunk)
                        chunkLen = len(chunk)
                        totalSize += chunkLen
                        send += chunkLen
                        cur = time.time()
                        if cur - now >= 0.1:
                            if backData.backParam:
                                TaskBase.taskObj.downloadBack.emit(backData.backParam, send, expectedSize, b"")
                            send = 0
                            now = cur
                    streamFinished = True

                    data = bytes(buf)
                    fileSize = len(data)
                    if send > 0 and backData.backParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, send, fileSize, b"")
                finally:
                    await _CloseStreamResponse(r, streamFinished)

            except asyncio.CancelledError:
                raise
            except Exception as es:
                isFail = True
                task.status = ClassifyRequestError(es, isDownload=True)
                Log.Error(es)

            # 异常图片
            if len(data) < 20 or isFail:
                Log.Warn(f"download_error_picture, url:{backData.req.url}, data:{len(data)}, is_fail:{isFail}")
                if not data and not isFail and status_code == 200:
                    if backData.bakParam:
                        from server.req import ServerReq
                        ServerReq.SPACE_PIC.add(backData.req.url)
                        TaskBase.taskObj.downloadBack.emit(backData.bakParam, -Str.SpacePic, fileSize, b"")
                    return
                ## 尝试切换图片地址
                backData.req.ResetToSwitchNextUrl()
                if backData.req.resetCnt >= 0:
                    backData.req.isReset = True
                    if backData.bakParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, -Status.Resetting, fileSize, b"")
                    Server().ReDownload(backData)
                    return
                else:
                    if backData.status == Status.Ok:
                        backData.status = Status.DownloadBusy
                    if backData.bakParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, -backData.status, fileSize, b"")
                    return

            # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
            _, _, mat, isAni = ToolUtil.GetPictureSize(data)

            if len(data) > 0 and backData.req.saveParam and not isAni:
                try:
                    saveParam = backData.req.saveParam
                    newData = await asyncio.to_thread(
                        TaskMulti().GetJmPicResultsResult,
                        data,
                        saveParam[0],
                        saveParam[1],
                        saveParam[2],
                    )
                    if newData:
                        data = newData
                except Exception as es:
                    Log.Error(es)

            if config.IsUseCache and len(data) > 0:
                try:
                    if backData.req.cachePath or backData.req.savePath:
                        if backData.req.cachePath:
                            TaskCache().AddCacheDiskPath(ToolUtil.GetPictureName(backData.req.cachePath, mat), data)

                        for path in [backData.req.savePath]:
                            filePath = path
                            if not path:
                                continue
                            await asyncio.to_thread(ToolUtil.SaveDownloadPicture, data, filePath, mat, isAni)
                            Log.Debug("add download cache, cachePath:{}".format(filePath))
                except Exception as es:
                    Log.Error(es)
                    # 保存失败了
                    if backData.bakParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, -2, fileSize, b"")
                    return

            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.backParam, 0, fileSize, data)

            Log.Info("response{}-> backId:{}, {}, st:{}, hit:{}".format(
                index, backData.backParam, backData.req.__class__.__name__,
                backData.status, cfHit))

        except asyncio.CancelledError:
            raise
        except Exception as es:
            backData.status = Status.DownloadFail
            Log.Error(es)
            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.backParam, -backData.status, fileSize, b"")
        finally:
            if task.req.isImg and isinstance(ttfb_time, (int, float)):
                TaskBase.taskObj.statuImgBack.emit(ttfb_time, backData.status, status_code, totalSize)


@handler(req.GetProxyIpInfoReq)
class GetProxyIpInfoReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return

            from natsort import natsorted
            ips = json.loads(task.res.raw.content)
            allIps = []
            if isinstance(ips, list):
                for ip in ips:
                    v = ip.split(":")
                    if not v or not v[0]:
                        continue
                    allIps.append(v[0])
                data['list'] = natsorted(allIps)
            else:
                data['list'] = []
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetCfDnsReq)
@handler(req.GetIpInfoReq)
class GetRawHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            data['data'] = task.res.raw.content
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DnsOverHttpsReq)
class DnsOverHttpsReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return
            info = json.loads(task.res.raw.content)
            data['Answer'] = info.get("Answer")
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))



@handler(req.GetEchConfigReq)
class GetEchConfigReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        isReset = False
        try:
            if task.status != Status.Ok:
                return

            if task.res.raw.status_code != 200:
                isReset = True

            info = task.res.raw.content
            data['data'] = task.req.parse_dns_response(info)
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if isReset and task.req.resetCnt >= 0:
                task.req.ResetToSwitchNextUrl()
                task.req.isReset = True
                Server().Send(task.req, backParam=task.backParam)
                return
            else:
                if task.backParam:
                    TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.SpeedTestPingReq)
@handler(req.SpeedTestPing2Req)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if hasattr(task.res.raw, "elapsed"):
            if task.res.raw.status_code == 401 or task.res.raw.status_code == 200:
                if isinstance(task.res.raw.elapsed, timedelta):
                    data["data"] = str(
                        (task.res.raw.elapsed.seconds * 1000 + task.res.raw.elapsed.microseconds / 1000) // 4)
                else:
                    data["data"] = str(task.res.raw.elapsed * 1000 // 4)
            else:
                data["st"] = Status.Error
                data["data"] = "0"
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
        else:
            data["data"] = "0"
            if task.bakParam:
                TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.GetJmServerReq)
class GetJmServerHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            from jmcomic import JmCryptoTool
            raw = JmCryptoTool.decode_resp_data(task.res.raw.content, '', 'diosfjckwpqpdfjkvnqQjsik')
            v = json.loads(raw)
            data["st"] = Status.Ok
            data["data"] = v
        except Exception as es:
            data["st"] = Status.ParseError
            data["errorMsg"] = task.res.GetText()
            Log.Warn("url:{}, data:{}".format(task.req.url, task.res.GetText()))
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))

@handler(req.SpeedTestReq)
class SpeedTestHandler(object):
    async def __call__(self, backData):
        data = {"st": backData.status, "data": ""}
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
        else:
            request = backData.req
            index = backData.index
            try:
                now = time.time()
                async with requests2.AsyncSession(
                    curl_options=copy.deepcopy(request.curl_opt), max_clients=1
                ) as session:
                    r = await session.get(
                        request.url,
                        headers=request.headers,
                        timeout=backData.timeout,
                        proxies=request.proxy,
                    )

                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = len(r.content)
                # 网速快，太卡了，优化成最多100ms一次
                # try:
                #     for chunk in r.iter_content():
                #         getSize += len(chunk)
                #         consume = time.time() - now
                #         if consume >= 3.0:
                #             break

                # except Exception as es:
                #     Log.Error(es)

                consume = time.time() - now
                if consume == 0:
                    consume = 0.1
                downloadSize = getSize / consume
                speed = ToolUtil.GetDownloadSize(downloadSize)
                if backData.bakParam:
                    data["data"] = speed
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))

            except asyncio.CancelledError:
                raise
            except Exception as es:
                Log.Error(es)
                data["st"] = Status.DownloadFail
                if backData.bakParam:
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))


@handler(req.GetBestCfIpReq)
class GetBestCfIpReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        try:
            if task.status != Status.Ok:
                return

            data['list'] = ToolUtil.ExportIpsByStr(task.res.raw.text)
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))

