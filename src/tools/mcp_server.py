"""JMComic MCP server —— 把客户端的只读能力暴露给 AI agent（stdio）。

只读工具：搜索、详情、评论、本地下载库、阅读历史。
不做下载等有副作用的操作；也不接触账号密码本身
（自动登录读取的是 config.ini 里用户已保存的凭据，仅在本进程内存中使用）。

运行：.venv/bin/python src/tools/mcp_server.py
依赖：offscreen 模式复用客户端的整个网络栈（登录态、加密、重试、DoH 兜底），
     因此所有网络韧性修复对 AI 同样生效。
"""
import json
import os
import sqlite3
import sys

# --- 必须在导入 PySide6 之前准备好无界面环境 ---
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from mcp.server.fastmcp import FastMCP

from PySide6.QtWidgets import QApplication

_app = QApplication.instance() or QApplication([])

from config.global_config import GlobalConfig          # noqa: E402
from config.setting import Setting                      # noqa: E402
from qt_owner import QtOwner                            # noqa: E402
import server.req as _req                               # noqa: E402
from server.server import Server                  # noqa: E402
from tools.log import Log                               # noqa: E402
from tools.tool import ToolUtil                         # noqa: E402

Log.Init()                  # InitLoadSetting 里会调日志等级，需要先建好 handler
Setting.InitLoadSetting()   # 读取 config.ini（下载目录/凭据/线路等，app 启动时同款）
GlobalConfig.LoadSetting()
QtOwner()  # 初始化空 owner（GUI 不存在，但登录态/请求构造需要它）

STATE_DIR = Setting.GetStatePath()

mcp = FastMCP(
    "jmcomic",
    instructions=(
        "JMComic 客户端工具：搜索、详情/评论、本地下载库与阅读历史，以及受控的下载。\n"
        "剧情总结有两种模式：\n"
        "  1. 元数据模式（默认，快）：get_book_detail 的简介/标签 + get_comments 的热门评论；\n"
        "  2. 内容模式（慢，需要视觉能力）：fetch_pages 抓取前几页到本地，再用视觉读图总结。\n"
        "先和用户确认用哪档；内容模式会向服务器请求图片，且图片会进入模型上下文。\n"
        "【重要】本作内容通常属于成人向。把页面图片读入上下文会让审核严格的模型\n"
        "（如智谱 coding plan、多数商业 API）直接返回 1301 并中断会话，retryable=false。\n"
        "因此：默认只用元数据档；未经用户明确要求，不要主动 Read fetch_pages 返回的图片；\n"
        "即使用户要求，也要先提示可能需要自建/无审查的视觉模型，并把读图放在最后一步，\n"
        "以免整轮工作因审核中断而丢失。\n"
        "download_book 是唯一有副作用的工具（写文件到「AI 下载区」），调用前务必先征得用户同意；"
        "它不进客户端的下载管理器，整个「AI-Downloads」文件夹可以随时一键删除。"
    ),
)


def _Sync(request):
    """在调用线程里同步执行一个请求，返回 (status, task)。

    走 Server.SendSync：先做备用线路准备，失败后照样享受
    换线重试 + DoH 兜底 + 域名冷却（与 GUI 完全同一条路）。
    """
    task = Server().SendSync(request)
    return task.status, task


def _Json(task):
    """取响应 JSON（已校验 code==200 的 data 之前的部分）"""
    if not task.res or not hasattr(task.res, "raw") or task.res.raw is None:
        raise RuntimeError("empty response (status {})".format(task.status))
    v = json.loads(task.res.raw.content)
    if v.get("code") != 200:
        raise RuntimeError("api error: code={}, msg={}".format(
            v.get("code"), v.get("errorMsg") or v.get("message")))
    return v


def _Db(dbName, query, params=()):
    """读本地 SQLite。app 可能开着（WAL 模式），用普通连接 + 忙等，
    只跑 select 不会写坏任何东西"""
    con = sqlite3.connect(os.path.join(STATE_DIR, dbName), timeout=2)
    try:
        cur = con.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        con.close()


def _EnsureLogin():
    """用 config.ini 里保存的凭据自动登录（和 app 启动时的自动登录同一份）。

    不登录时搜索/详情/评论大多可用，登录后可见收藏等账号数据。
    """
    user = QtOwner().user
    if user.isLogin:
        return
    if not Setting.AutoLogin.value or not Setting.UserId.value:
        return
    try:
        status, task = _Sync(_req.LoginReq2(Setting.UserId.value, Setting.Password.value))
        if status != 1001:
            Log.Warn("mcp login failed, status:{}".format(status))
            return
        v = _Json(task)
        from tools.user import User
        u = ToolUtil.ParseLogin2(task.req.ParseData(v.get("data")))
        cookie = {}
        for c in task.res.raw.cookies.jar:
            cookie[c.name] = c.value
        u.cookie = cookie
        u.isLogin = True
        QtOwner().SetUser(u)
    except Exception as es:
        Log.Warn("mcp login error: {}".format(es))


def _Book(book):
    """BookInfo -> 干净的 dict（只挑对 agent 有用的字段）"""
    base = book.baseInfo
    page = getattr(book, "pageInfo", None)
    return {
        "id": str(getattr(base, "bookId", "") or getattr(base, "id", "") or ""),
        "title": base.title,
        "author": getattr(base, "authorList", []) or ([base.author] if base.author else []),
        "tags": getattr(base, "tagList", []) or getattr(base, "category", []),
        "likes": base.likes,
        "views": base.views,
        "description": getattr(page, "des", "") if page else "",
        "commentCount": getattr(page, "commentNum", None) if page else None,
    }


@mcp.tool()
def search_comics(keyword: str, sort: str = "mr", page: int = 1,
                  search_type: str = None) -> dict:
    """搜索漫画，返回元数据列表（标题/作者/标签，不含简介）。

    sort: mr=最新, mv=最多点击, mp=最多图片, tf=最多爱心
    search_type: site=全文, work=作品, author=作者, tag=标签, character=角色
    需要简介请对结果里的 id 调 get_book_detail。
    """
    _EnsureLogin()
    status, task = _Sync(_req.GetSearchReq2(keyword, sort=sort, page=page, search_type=search_type))
    if status != 1001:
        return {"error": "network failed (status {})".format(status)}
    v = _Json(task)
    total, bookList = ToolUtil.ParseSearch2(task.req.ParseData(v.get("data")))
    return {"total": total, "page": page, "books": [_Book(b) for b in bookList]}


@mcp.tool()
def get_book_detail(book_id: str) -> dict:
    """获取一部漫画的完整元数据：标题、作者、标签、简介（剧情总结的主要输入）、章节数。"""
    _EnsureLogin()
    status, task = _Sync(_req.GetBookInfoReq2(str(book_id)))
    if status != 1001:
        return {"error": "network failed (status {})".format(status)}
    v = _Json(task)
    b, _isFavorite = ToolUtil.ParseBookInfo2(task.req.ParseData(v.get("data")))
    base = b.baseInfo
    result = _Book(b)
    epsInfo = getattr(b.pageInfo, "epsInfo", {}) or {}
    eps = [{"index": idx, "epsId": str(e.epsId), "title": e.epsName or e.title}
           for idx, e in sorted(epsInfo.items())]
    result.update({
        "works": base.workList,
        "actors": base.actorList,
        "pages": getattr(b.pageInfo, "pages", None),
        "epsCount": len(eps),
        "eps": eps[:20],
    })
    return result


@mcp.tool()
def get_comments(book_id: str, page: int = 1) -> dict:
    """获取漫画的热门评论。评论区常有读者总结剧情和观感，是剧情总结的重要输入。"""
    _EnsureLogin()
    status, task = _Sync(_req.GetCommentReq2(str(book_id), page=str(page)))
    if status != 1001:
        return {"error": "network failed (status {})".format(status)}
    v = _Json(task)
    commentList, total = ToolUtil.ParseBookComment(task.req.ParseData(v.get("data")))
    return {"total": total, "comments": [
        {"user": c.name, "content": c.content, "likes": c.like}
        for c in commentList
    ]}


@mcp.tool()
def local_library() -> dict:
    """列出本地已下载的漫画（客户端下载管理器里的内容，含保存路径）。"""
    rows = _Db("download.db", "select bookId, title, savePath, tick from download order by tick desc")
    return {"count": len(rows), "books": rows}


@mcp.tool()
def reading_history(limit: int = 30) -> dict:
    """查询站内阅读历史（最近看过的漫画和看到第几话/第几页）。"""
    limit = max(1, min(int(limit), 100))
    rows = _Db("history.db", "select bookId, name, epsId, picIndex, tick from history order by tick desc limit ?",
               (limit,))
    return {"count": len(rows), "history": rows}


@mcp.tool()
def local_read_books() -> dict:
    """列出已导入客户端的本地漫画文件（含最近阅读进度）。"""
    rows = _Db("local_read.db", "select id, title, path, picCnt, lastIndex, lastReadTime "
               "from local_book order by lastReadTime desc")
    return {"count": len(rows), "books": rows}


# ---------------------------------------------------------------------------
# 下载区（唯一有副作用的工具）
#
# 约定（和用户讨论定下的「第三条路」）：
#   * 用主账号网络栈，不搞第二套账号
#   * 文件落到 <客户端下载目录>/AI-Downloads/，与主库物理隔离
#   * 不写 download.db —— 客户端下载管理器完全看不到
#   * 不想留就删 AI-Downloads 文件夹；想要就挪进主库（结构兼容）
# ---------------------------------------------------------------------------

def _Sanitize(name, fallback="unnamed"):
    name = str(name or "").strip()
    for ch in '/\\:*?"<>|':
        name = name.replace(ch, " ")
    name = name.strip().rstrip(".")
    return name or fallback


def _GetDetail(book_id):
    status, task = _Sync(_req.GetBookInfoReq2(str(book_id)))
    if status != 1001:
        return None
    v = _Json(task)
    b, _ = ToolUtil.ParseBookInfo2(task.req.ParseData(v.get("data")))
    epsInfo = getattr(b.pageInfo, "epsInfo", {}) or {}
    eps = [{"index": idx, "epsId": str(e.epsId), "title": e.epsName or e.title or "第{}话".format(idx + 1)}
           for idx, e in sorted(epsInfo.items())]
    return {"id": str(book_id), "title": b.baseInfo.title or book_id, "eps": eps}


def _DownloadImage(urlPath, epsId, picName):
    """下载一张图（备用CDN轮换 + 域名冷却），返回原始字节。"""
    from curl_cffi import requests as curlRequests
    primary = GlobalConfig.GetImgUrl().rstrip("/")
    candidates = [(GlobalConfig.GetImgUrl(), primary + urlPath)]
    for domain in GlobalConfig.ImgAutoUrl.value:
        alt = "https://" + domain.rstrip("/")
        if alt != primary:
            candidates.append((domain, alt + urlPath))
    lastError = None
    for host, url in candidates:
        hostOnly = ToolUtil.GetUrlHost(url)
        if Server.IsHostCooling(hostOnly):
            continue
        try:
            request = _req.DownloadBookReq(url)
            session = curlRequests.Session(impersonate="chrome110")
            try:
                session.curl_options = dict(request.curl_opt)
                r = session.get(url, proxies=request.proxy, headers=request.headers,
                                timeout=max(5, Setting.ImgTimeOut.GetIndexV()))
            finally:
                try:
                    session.close()
                except Exception:
                    pass
            if r.status_code != 200:
                raise RuntimeError("http {}".format(r.status_code))
            if len(r.content) < 100:
                raise RuntimeError("too small")
            return r.content
        except Exception as es:
            lastError = es
            # 连接层失败才冷却；HTTP 403/404 是服务端态度，换下一个就行
            if not str(es).startswith("http "):
                Server.MarkHostFail(hostOnly)
    raise RuntimeError("image download failed after all cdns: {}".format(lastError))


def _RestoreAndSave(imgData, epsId, scrambleId, picName, path):
    """还原 JM 的切块乱序并落盘（与客户端阅读时的还原算法一致）"""
    data = ToolUtil.SegmentationPicture(imgData, epsId, scrambleId, picName)
    fileDir = os.path.dirname(path)
    if fileDir and not os.path.isdir(fileDir):
        os.makedirs(fileDir)
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def _EpsPageList(bookId, epsId):
    """拉一章的图片清单，返回 (scrambleId, [{index, urlPath, picName}])"""
    status, task = _Sync(_req.GetBookEpsInfoReq2(str(bookId), str(epsId), 0))
    if status != 1001:
        return None
    v = _Json(task)
    epsInfo = ToolUtil.ParseBookEpsInfo2(task.req.ParseData(v.get("data")))
    pages = []
    for idx in epsInfo.allIndex:
        pages.append({
            "index": idx,
            "urlPath": epsInfo.pictureUrl[idx],
            "picName": epsInfo.pictureName[idx],
        })
    return epsInfo.scrambleId, pages


def _SavePathBase():
    savePath = Setting.SavePath.value
    if not savePath:
        return None
    base = os.path.join(savePath, "AI-Downloads")
    if not os.path.isdir(base):
        os.makedirs(base)
    return base


@mcp.tool()
def download_book(book_id: str, eps_ids: list = None, max_pages_per_eps: int = 0,
                  overwrite: bool = False) -> dict:
    """下载漫画到「AI 下载区」：<客户端下载目录>/AI-Downloads/<书名>/<章节>/。

    注意：这是唯一有副作用的工具，调用前必须先征得用户同意。
    不会写进客户端的下载管理器；删除 = 删 AI-Downloads 文件夹；
    想收入主库就把对应文件夹移动到客户端下载目录顶层。

    eps_ids: 要下载的章节 epsId 列表（见 get_book_detail 的 eps 字段），空 = 全部章节。
    max_pages_per_eps: >0 时每章只下前 N 页（试读）。
    overwrite: 已存在的文件是否重新下载（默认跳过，可断点续传）。
    """
    _EnsureLogin()
    base = _SavePathBase()
    if not base:
        return {"error": "客户端未设置下载目录（Setting.SavePath 为空）"}
    detail = _GetDetail(book_id)
    if not detail:
        return {"error": "network failed"}
    bookDir = os.path.join(base, _Sanitize(detail["title"], book_id))

    want = [e for e in detail["eps"] if not eps_ids or str(e["epsId"]) in [str(x) for x in eps_ids]]
    if not want:
        return {"error": "no matching eps", "eps": detail["eps"]}

    summary = {"book": detail["title"], "saved_to": bookDir, "eps": []}
    totalFail = 0
    for e in want:
        fetched = _EpsPageList(book_id, e["epsId"])
        if not fetched:
            summary["eps"].append({"epsId": e["epsId"], "title": e["title"], "error": "chapter fetch failed"})
            continue
        scrambleId, pages = fetched
        epsDir = os.path.join(bookDir, _Sanitize(e["title"], "eps-{}".format(e["index"] + 1)))
        done, fail, skipped = 0, 0, 0
        for i, p in enumerate(pages):
            if max_pages_per_eps and i >= max_pages_per_eps:
                break
            path = os.path.join(epsDir, "{:05d}.jpg".format(i + 1))
            if os.path.isfile(path) and not overwrite and os.path.getsize(path) > 0:
                skipped += 1
                continue
            try:
                img = _DownloadImage(p["urlPath"], e["epsId"], p["picName"])
                _RestoreAndSave(img, e["epsId"], scrambleId, p["picName"], path)
                done += 1
            except Exception as es:
                fail += 1
                Log.Warn("mcp download pic failed: {}".format(es))
        totalFail += fail
        summary["eps"].append({"epsId": e["epsId"], "title": e["title"],
                               "pages": len(pages), "downloaded": done,
                               "skipped_existing": skipped, "failed": fail})
    summary["failed_total"] = totalFail
    return summary


@mcp.tool()
def fetch_pages(book_id: str, eps_id: str = "", page_count: int = 4) -> dict:
    """抓取某章前 N 页到预览目录（AI-Downloads/_preview/<书名>/），返回图片文件路径。

    只负责把图落到本地并返回路径，本身不读图。
    警告：本作多为成人向。若把返回的图片读入对内容审核严格的模型上下文
    （多数商业 API / 编码套餐），很可能直接 1301 中断整轮会话；
    视觉总结请使用自建或无审查的视觉模型，并由用户明确同意后再执行。
    纯元数据总结不需要调用本工具。页数建议 2-4 页，越多越慢也越贵。
    """
    _EnsureLogin()
    page_count = max(1, min(int(page_count), 8))
    base = _SavePathBase()
    if not base:
        return {"error": "客户端未设置下载目录（Setting.SavePath 为空）"}
    detail = _GetDetail(book_id)
    if not detail:
        return {"error": "network failed"}
    eps = detail["eps"][0]
    if eps_id:
        match = [e for e in detail["eps"] if str(e["epsId"]) == str(eps_id)]
        if match:
            eps = match[0]
    fetched = _EpsPageList(book_id, eps["epsId"])
    if not fetched:
        return {"error": "chapter fetch failed"}
    scrambleId, pages = fetched
    outDir = os.path.join(base, "_preview", _Sanitize(detail["title"], book_id))
    paths, fail = [], 0
    for i, p in enumerate(pages):
        if i >= page_count:
            break
        try:
            img = _DownloadImage(p["urlPath"], eps["epsId"], p["picName"])
            path = os.path.join(outDir, "{:05d}.jpg".format(i + 1))
            _RestoreAndSave(img, eps["epsId"], scrambleId, p["picName"], path)
            paths.append(path)
        except Exception as es:
            fail += 1
            Log.Warn("mcp fetch page failed: {}".format(es))
    return {"book": detail["title"], "eps": eps["title"], "paths": paths, "failed": fail,
            "note": "这些图已经过乱序还原，可直接视觉阅读；不想留可删 _preview 目录"}


if __name__ == "__main__":
    mcp.run()
