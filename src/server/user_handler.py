import json
import os
import pickle
import re

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
    def __call__(self, backData):
        if not backData.GetText() or backData.status == Status.NetError:
            if backData.backParam:
                data = b""
                TaskBase.taskObj.taskBack.emit(backData.backParam, pickle.dumps(data))
            return

        updateInfo = re.findall(r"<meta property=\"og:description\" content=\"([^\"]*)\"", backData.res.raw.text)
        if updateInfo:
            data = updateInfo[0]
        else:
            data = ""

        info = re.findall(r"\d+\d*", os.path.basename(backData.res.raw.url))
        version = int(info[0]) * 100 + int(info[1]) * 10 + int(info[2]) * 1
        info2 = re.findall(r"\d+\d*", os.path.basename(config.UpdateVersion))
        curversion = int(info2[0]) * 100 + int(info2[1]) * 10 + int(info2[2]) * 1

        data = "\n\nv" + ".".join(info) + "\n" + data
        if version > curversion:
            if backData.backParam:
                TaskBase.taskObj.taskBack.emit(backData.backParam, pickle.dumps(data))


@handler(req.GetUserInfoReq)
class GetUserInfoReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            user = ToolUtil.ParseUserInfo(task.res.raw.text)
            if user:
                data["st"] = Status.Ok
                data["user"] = user
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


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

            ## 如果发生了301跳转，必须设置为新的域名，否则无法登录
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


@handler(req.LoginReq)
class LoginReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            isSuc, msg = ToolUtil.ParseLogin(task.res.raw.text)

            cookies = requests.utils.dict_from_cookiejar(task.res.raw.cookies)
            print(cookies)

            for raw in task.res.raw.history:
                cookies = requests.utils.dict_from_cookiejar(raw.cookies)
                print(cookies)

            data["msg"] = msg
            if isSuc:
                Log.Info("login success, {}".format(msg))
                st = Status.Ok
                data["st"] = st
            else:
                data["st"] = Status.UserError
                Log.Info("login error, {}".format(msg))
            # cookies = task.res.raw.headers.get("Set-Cookie", "")
            # print(cookies)
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetIndexInfoReq)
class GetIndexInfoReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            bookList = ToolUtil.ParseIndex(task.res.raw.text)
            from tools.book import BookMgr
            BookMgr().UpdateBookInfoList(bookList)
            data["st"] = Status.Ok
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetSearchReq)
class GetSearchReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            maxPages, bookList = ToolUtil.ParseSearch(task.res.raw.text)
            data["st"] = Status.Ok
            data["maxPages"] = maxPages
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))

@handler(req.GetFavoritesReq)
class GetFavoritesReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            curNum, maxNum, bookList = ToolUtil.ParseFavorite(task.res.raw.text)
            data["st"] = Status.Ok
            data["curNum"] = curNum
            data["maxNum"] = maxNum
            data["bookList"] = bookList
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookInfoReq)
class GetBookInfoReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            isFavorite, info = ToolUtil.ParseBookInfo(task.res.raw.text, task.req.bookId)
            from tools.book import BookMgr
            BookMgr().UpdateBookInfo(task.req.bookId, info)
            data["st"] = Status.Ok
            data["isFavorite"] = isFavorite
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.GetBookImgUrl)
class GetBookImgUrlReqHandler(object):
    def __call__(self, task: Task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            aid, minAid, pictureUrl, pictureName = ToolUtil.ParsePictureUrl(task.res.raw.text)
            from tools.book import BookMgr
            BookMgr().UpdateBookPicture(task.req.bookId, task.req.epsId, aid, minAid, pictureUrl, pictureName)
            data["st"] = Status.Ok
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.AddFavoritesReq)
class AddFavoritesReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            resData = json.loads(task.res.raw.text)
            if resData.get("status") == 1:
                data["st"] = Status.Ok
            else:
                data["st"] = Status.Error
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DelFavoritesReq)
class DelFavoritesReqHandler(object):
    def __call__(self, task):
        data = {"st": task.status}
        try:
            if task.status != Status.Ok:
                return
            resData = json.loads(task.res.raw.text)
            if resData.get("status") == 1:
                data["st"] = Status.Ok
            else:
                data["st"] = Status.Error
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


@handler(req.DownloadBookReq)
class DownloadBookReq(object):
    def __call__(self, backData):
        if backData.status != Status.Ok:
            if backData.backParam:
                TaskBase.taskObj.downloadBack.emit(backData.backParam, -1, b"")
        else:
            r = backData.res
            try:
                if r.status_code != 200:
                    if backData.backParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, -r.status_code, b"")
                    return
                fileSize = int(r.headers.get('Content-Length', 0))
                getSize = 0
                data = b""
                for chunk in r.iter_content(chunk_size=1024):
                    if backData.backParam:
                        TaskBase.taskObj.downloadBack.emit(backData.backParam, fileSize-getSize, chunk)
                    getSize += len(chunk)
                    data += chunk
                if backData.backParam:
                    TaskBase.taskObj.downloadBack.emit(backData.backParam, 0, b"")
                # Log.Info("size:{}, url:{}".format(ToolUtil.GetDownloadSize(fileSize), backData.req.url))
                if backData.cacheAndLoadPath and config.IsUseCache and len(data) > 0:
                    filePath = backData.cacheAndLoadPath
                    fileDir = os.path.dirname(filePath)
                    if not os.path.isdir(fileDir):
                        os.makedirs(fileDir)

                    with open(filePath + ".jpg", "wb+") as f:
                        f.write(data)
                    Log.Debug("add download cache, cachePath:{}".format(filePath))

                if backData.req.saveFile:
                    filePath = backData.req.saveFile
                    fileDir = os.path.dirname(filePath)
                    if not os.path.isdir(fileDir):
                        os.makedirs(fileDir)

                    with open(filePath + ".jpg", "wb+") as f:
                        f.write(data)
                    Log.Debug("add download file, filePath:{}".format(filePath))

            except Exception as es:
                Log.Error(es)
                if backData.backParam:
                    TaskBase.taskObj.downloadBack.emit(backData.backParam, -1, b"")


@handler(req.SpeedTestPingReq)
class SpeedTestPingHandler(object):
    def __call__(self, task):
        data = {"st": task.status, "data": str(0)}
        try:
            if task.status != Status.Ok:
                return
            if hasattr(task.res.raw, "elapsed"):
                data["data"] = str(task.res.raw.elapsed.total_seconds())
        except Exception as es:
            data["st"] = Status.ParseError
            Log.Error(es)
        finally:
            if task.backParam:
                TaskBase.taskObj.taskBack.emit(task.backParam, pickle.dumps(data))


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