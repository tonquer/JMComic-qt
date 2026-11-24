import copy
from collections import OrderedDict
from contextlib import asynccontextmanager

from curl_cffi import CurlInfo, requests as requests2

import server.req as req
from tools.log import Log

CURL_INFOS = [
    CurlInfo.NAMELOOKUP_TIME,
    CurlInfo.CONNECT_TIME,
    CurlInfo.APPCONNECT_TIME,
    CurlInfo.PRETRANSFER_TIME,
    CurlInfo.STARTTRANSFER_TIME,
    CurlInfo.TOTAL_TIME,
]


def _NormalizeIpKey(ipList) -> tuple:
    if not ipList:
        return ()
    if isinstance(ipList, str):
        return (ipList,)
    return tuple(sorted(ipList))


def _NormalizeValue(value):
    if isinstance(value, (list, tuple, set)):
        items = [_NormalizeValue(item) for item in value]
        return tuple(sorted(set(items), key=str))
    if isinstance(value, dict):
        items = [(_NormalizeValue(k), _NormalizeValue(v)) for k, v in value.items()]
        return tuple(sorted(items, key=lambda pair: str(pair[0])))
    try:
        hash(value)
        return value
    except TypeError:
        return repr(value)


def _NormalizeCurlOptKey(curlOpt) -> tuple:
    if not curlOpt:
        return ()

    def _SortKey(item):
        key = item[0]
        try:
            return (0, int(key))
        except (TypeError, ValueError):
            return (1, str(key))

    result = []
    for k, v in sorted(curlOpt.items(), key=_SortKey):
        try:
            optKey = int(k)
        except (TypeError, ValueError):
            optKey = str(k)
        result.append((optKey, _NormalizeValue(v)))
    return tuple(result)


def BuildSessionKey(request: req.ServerReq, impersonate) -> tuple:
    """Build an immutable cache key so curl_options are never mutated across concurrent requests."""
    return (
        impersonate,
        request.userName,
        bool(request.isH3),
        _NormalizeIpKey(request.ipList),
        _NormalizeCurlOptKey(request.curl_opt),
    )


class _SessionEntry:
    def __init__(self, session: requests2.AsyncSession, key: tuple):
        self.session = session
        self.key = key
        self.activeCount = 0
        self.retired = False
        self.closed = False

    async def Close(self):
        if self.closed or self.session is None:
            return
        self.closed = True
        session = self.session
        self.session = None
        try:
            await session.close()
        except Exception as es:
            Log.Error(es)


class AsyncSessionPool:
    """LRU pool of curl_cffi AsyncSession instances with safe deferred retirement."""

    def __init__(
        self,
        name: str,
        impersonate=None,
        maxClients: int = 10,
        maxSessions: int = 6,
        reuseSession: bool = True,
    ):
        self.name = name
        self.impersonate = impersonate
        self.maxClients = max(1, maxClients)
        self.maxSessions = max(1, maxSessions)
        self.reuseSession = reuseSession
        self._sessions: OrderedDict[tuple, _SessionEntry] = OrderedDict()
        self._retiring: set[_SessionEntry] = set()
        self._lastUserName = None

    def _CreateSession(self, request: req.ServerReq, maxClients: int = None) -> requests2.AsyncSession:
        kwargs = {
            "curl_infos": CURL_INFOS,
            "curl_options": copy.deepcopy(request.curl_opt),
            "max_clients": self.maxClients if maxClients is None else max(1, maxClients),
        }
        if self.impersonate:
            kwargs["impersonate"] = self.impersonate
        return requests2.AsyncSession(**kwargs)

    def _CreateEphemeralEntry(self, request: req.ServerReq, reason: str) -> _SessionEntry:
        entry = _SessionEntry(self._CreateSession(request, maxClients=1), key=())
        entry.retired = True
        entry.activeCount = 1
        self._retiring.add(entry)
        Log.Info(
            f"create new async session ({reason}), pool:{self.name}, ip:{request.ipList}, isH3:{request.isH3}"
        )
        return entry

    async def _RetireEntry(self, entry: _SessionEntry):
        entry.retired = True
        if entry.activeCount <= 0:
            self._retiring.discard(entry)
            await entry.Close()
        else:
            self._retiring.add(entry)

    async def RetireEntry(self, entry: _SessionEntry, reason: str = ""):
        """Retire a specific session entry by identity so a newer healthy replacement is never evicted."""
        if entry is None:
            return
        wasRetired = entry.retired
        if self._sessions.get(entry.key) is entry:
            self._sessions.pop(entry.key, None)
        await self._RetireEntry(entry)
        if not wasRetired and reason:
            Log.Info(f"retire async session ({reason}), pool:{self.name}")

    async def _RetireAll(self):
        entries = list(self._sessions.values())
        self._sessions.clear()
        for entry in entries:
            await self._RetireEntry(entry)

    async def _EvictOneIfFull(self):
        if len(self._sessions) < self.maxSessions:
            return
        evictKey = next(
            (k for k, entry in self._sessions.items() if entry.activeCount == 0),
            next(iter(self._sessions)),
        )
        await self._RetireEntry(self._sessions.pop(evictKey))

    async def Acquire(self, request: req.ServerReq) -> _SessionEntry:
        # 测速请求不复用 session，避免 RESOLVE/DNS 缓存与长连接复用导致延迟失真
        if not self.reuseSession or isinstance(
            request, (req.SpeedTestPingReq, req.SpeedTestPing2Req, req.SpeedTestReq)
        ):
            return self._CreateEphemeralEntry(request, reason="ephemeral")

        # 切换账号时清理旧会话，避免 Cookie 串号
        if self._lastUserName is not None and request.userName != self._lastUserName:
            await self._RetireAll()
        self._lastUserName = request.userName

        # 登录请求始终使用独立的新会话，结束后立即释放
        if isinstance(request, req.LoginReq2):
            await self._RetireAll()
            return self._CreateEphemeralEntry(request, reason="login")

        key = BuildSessionKey(request, self.impersonate)
        entry = self._sessions.get(key)
        if entry is not None:
            self._sessions.move_to_end(key)
        else:
            await self._EvictOneIfFull()
            entry = _SessionEntry(self._CreateSession(request), key)
            self._sessions[key] = entry
            Log.Info(
                f"create new async session, pool:{self.name}, ip:{request.ipList}, isH3:{request.isH3}"
            )

        entry.activeCount += 1
        return entry

    async def Release(self, entry: _SessionEntry):
        entry.activeCount = max(0, entry.activeCount - 1)
        if entry.retired and entry.activeCount == 0:
            self._retiring.discard(entry)
            await entry.Close()

    @asynccontextmanager
    async def Use(self, request: req.ServerReq):
        entry = await self.Acquire(request)
        try:
            yield entry.session
        finally:
            await self.Release(entry)

    async def CloseAll(self):
        entries = list(self._sessions.values()) + list(self._retiring)
        self._sessions.clear()
        self._retiring.clear()
        for entry in entries:
            entry.retired = True
            await entry.Close()
