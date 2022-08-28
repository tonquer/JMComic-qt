import json
import os
import pickle
import re
import time

import requests

from config import config
from task.qt_task import TaskBase
from server import req
from tools.status import Status
from tools.log import Log
from tools.tool import ToolUtil
from .server import handler, Task, Server


@handler(req.CheckUpdateReq)
class CheckUpdateHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": ""}
        try:
            if not task.res.GetText() or task.status == Status.NetError:
                return
            if task.res.raw.status_code != 200:
                return

            updateInfo = re.findall(r"<meta property=\"og:description\" content=\"([^\"]*)\"", task.res.raw.text)
            if updateInfo:
                rawData = updateInfo[0]
            else:
                rawData = ""

            versionInfo = re.findall("<meta property=\"og:url\" content=\".*tag/([^\"]*)\"", task.res.raw.text)
            if versionInfo:
                verData = versionInfo[0]
            else:
                verData = ""

            info = verData.replace("v", "").split(".")
            version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
            info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
            curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

            rawData = "\n\nv" + ".".join(info) + "\n" + rawData

            if version > curversion:
                data["data"] = rawData
            else:
                data["data"] = "no"
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
#             user = ToolUtil.ParseUserInfo(task.res.raw.text)
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

            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
            # print(cookies)
            url = "https://" + ToolUtil.GetUrlHost(task.res.raw.url)

            ## 如果发生了301跳转，必须设置为新的域名，否则无法注册
            if url != config.Url:
                Log.Warn("Login url change, url:{}->{}".format(config.Url, url))
                config.Url = url

            # for raw in task.res.raw.history:
            #     cookies = requests.utils.dict_from_cookiejar(raw.cookies)
            #     print(cookies)

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
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            isSuc, msg = ToolUtil.ParseMsg(task.res.raw.text)

            data["msg"] = msg
            if isSuc:
                st = Status.Ok
                data["st"] = st
            else:
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
            v = json.loads(task.res.raw.text)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                Log.Warn("登陆失败！！！, code:{}, text:{}".format(str(task.res.code), task.res.GetText()))
                return
            user = ToolUtil.ParseLogin2(task.req.ParseData(v.get("data")))

            from requests import Response
            assert isinstance(task.res.raw, Response)
            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)

            ipcountry = cookies.get("ipcountry", "")
            ipm5 = cookies.get("ipm5", "")
            AVS = cookies.get("AVS", "")
            shunt = cookies.get("shunt", "")
            # config.ipcountry = ipcountry if ipcountry else config.ipcountry
            # config.ipm5 = ipm5 if ipm5 else config.ipm5
            # config.AVS = AVS if AVS else config.AVS
            # config.shunt = shunt if shunt else config.shunt
            Log.Info("Login suc, cookies:{}".format(cookies))
            st = Status.Ok
            data["st"] = st
            data["user"] = user
        except Exception as es:
            data["st"] = Status.ParseError
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
#             bookList = ToolUtil.ParseIndex(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            from requests import Response
            assert isinstance(task.res.raw, Response)
            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
            Log.Info("latest suc, cookies:{}".format(cookies))
            bookInfo = ToolUtil.ParseIndex2(task.req.ParseData(v.get("data")))
            data["st"] = Status.Ok
            data["bookInfo"] = bookInfo
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetLatestInfoReq2)
class GetIndexInfoReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
#             comments = ToolUtil.ParseComment(task.res.raw.text)
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
#             resData = json.loads(task.res.raw.text)
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
#             maxPages, bookList = ToolUtil.ParseSearch(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetCategoryReq2)
class GetSearchReq2Handler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            v = json.loads(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
#             curNum, maxNum, bookList = ToolUtil.ParseFavorite(task.res.raw.text)
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
#             isFavorite, info = ToolUtil.ParseBookInfo(task.res.raw.text, task.req.bookId)
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
            v = json.loads(task.res.raw.text)
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
            scrambleId = ToolUtil.ParseBookEpsScramble(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
            code = v.get("code")
            data["errorMsg"] = v.get("errorMsg", "")
            data["message"] = v.get("message", "")
            if code != 200:
                data["st"] = Status.Error
                return
            epsInfo = ToolUtil.ParseBookEpsInfo2(task.req.ParseData(v.get("data")))
            from tools.book import BookMgr
            BookMgr().UpdateBookEps(task.req.bookId, epsInfo)
            data["st"] = Status.Ok
            data["epsInfo"] = epsInfo
        except Exception as es:
            data["st"] = Status.ParseError
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
            v = json.loads(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
            v = json.loads(task.res.raw.text)
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
#             aid, minAid, pictureUrl, pictureName = ToolUtil.ParsePictureUrl(task.res.raw.text)
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
#             resData = json.loads(task.res.raw.text)
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
#             resData = json.loads(task.res.raw.text)
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


@handler(req.DownloadBookReq)
class DownloadBookHandler(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.downloadBack.emit(backData.bakParam, -backData.status, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.bakParam:
                        TaskBase.taskObj.downloadBack.emit(backData.bakParam, -Status.Error, b"")
                    return
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""
                now = time.time()

                # 网速快，太卡了，优化成最多100ms一次
                for chunk in r.iter_content(chunk_size=4096):
                    cur = time.time()
                    tick = cur - now
                    if tick >= 0.1:
                        if backData.bakParam and fileSize-getSize > 0:
                            TaskBase.taskObj.downloadBack.emit(backData.bakParam, fileSize-getSize, b"")
                        now = cur

                    getSize += len(chunk)
                    data += chunk

                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                if config.IsUseCache and len(data) > 0:
                    try:
                        for path in [backData.req.cachePath]:
                            filePath = path
                            if not path:
                                continue
                            fileDir = os.path.dirname(filePath)
                            if not os.path.isdir(fileDir):
                                os.makedirs(fileDir)

                            with open(filePath, "wb+") as f:
                                f.write(data)
                            Log.Debug("add download cache, cachePath:{}".format(filePath))

                        for path in [backData.req.savePath]:
                            filePath = path
                            if not path:
                                continue
                            fileDir = os.path.dirname(filePath)
                            if not os.path.isdir(fileDir):
                                os.makedirs(fileDir)
                            saveParam = backData.req.saveParam
                            data2 = ToolUtil. SegmentationPicture(data, saveParam[0], saveParam[1], saveParam[2])
                            with open(filePath, "wb+") as f:
                                f.write(data2)
                            Log.Debug("add download cache, cachePath:{}".format(filePath))
                    except Exception as es:
                        Log.Error(es)
                        # 保存失败了
                        if backData.backParam:
                            TaskBase.taskObj.downloadBack.emit(backData.backParam, -2, b"")

                if backData.bakParam:
                    TaskBase.taskObj.downloadBack.emit(backData.bakParam, 0, data)
            except Exception as es:
                Log.Error(es)
                if backData.backParam:
                    TaskBase.taskObj.downloadBack.emit(backData.backParam, -1, b"")


@handler(req.DnsOverHttpsReq)
class DnsOverHttpsReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            info = json.loads(task.res.raw.text)
            data['Answer'] = info.get("Answer")
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": task.res.GetText()}
        if hasattr(task.res.raw, "elapsed"):
            if task.res.raw.status_code == 401 or task.res.raw.status_code == 200:
                data["data"] = str(task.res.raw.elapsed.total_seconds() / 2)
            else:
                data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))
        else:
            data["data"] = "0"
            TaskBase.taskObj.taskBack.emit(task.bakParam, pickle.dumps(data))


@handler(req.SpeedTestReq)
class SpeedTestHandler(object):
    def __call__(self, backData):
        data = {"st": backData.status, "data": ""}
        if backData.status != Status.Ok:
            if backData.bakParam:
                TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.bakParam:
                        TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))
                    return

                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                now = time.time()
                for chunk in r.iter_content(chunk_size=1024):
                    getSize += len(chunk)
                    consume = time.time() - now
                    if consume >= 3.0:
                        break
                consume = time.time() - now
                downloadSize = getSize / consume
                speed = ToolUtil.GetDownloadSize(downloadSize)
                if backData.bakParam:
                    data["data"] = speed
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))

            except Exception as es:
                Log.Error(es)
                if backData.bakParam:
                    TaskBase.taskObj.taskBack.emit(backData.bakParam, pickle.dumps(data))