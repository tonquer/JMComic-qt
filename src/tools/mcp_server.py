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

from config.setting import Setting                      # noqa: E402
from qt_owner import QtOwner                            # noqa: E402
import server.req as _req                               # noqa: E402
from server.server import Server                  # noqa: E402
from tools.log import Log                               # noqa: E402
from tools.tool import ToolUtil                         # noqa: E402

QtOwner()  # 初始化空 owner（GUI 不存在，但登录态/请求构造需要它）

STATE_DIR = Setting.GetStatePath()

mcp = FastMCP(
    "jmcomic",
    instructions=(
        "JMComic 客户端的只读工具：搜索漫画、查看详情/评论、查询本地下载库与阅读历史。"
        "剧情总结请组合 get_book_detail（简介/标签）与 get_comments（热门评论）。"
        "所有工具都是只读的，不下载、不收藏、不发评论。"
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


if __name__ == "__main__":
    mcp.run()
