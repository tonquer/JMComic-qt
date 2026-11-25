"""Unified theme-aware SVG icon renderer for crisp HiDPI UI icons."""

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_ICON_CACHE: dict[tuple[str, str, int], QIcon] = {}
_STATEFUL_ICON_CACHE: dict[tuple[str, str, str, int], QIcon] = {}
_PIXMAP_CACHE: dict[tuple[str, str, int], QPixmap] = {}

_SVG_PATHS: dict[str, str] = {
    # 收藏（星标）
    "star": (
        '<path d="M12 2.6l2.9 5.88 6.49.94-4.7 4.58 1.11 6.46L12 17.4l-5.8 3.06 '
        '1.11-6.46-4.7-4.58 6.49-.94L12 2.6z" fill="none" stroke="{color}" '
        'stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    "star_filled": (
        '<path d="M12 2.6l2.9 5.88 6.49.94-4.7 4.58 1.11 6.46L12 17.4l-5.8 3.06 '
        '1.11-6.46-4.7-4.58 6.49-.94L12 2.6z" fill="{color}" stroke="{color}" '
        'stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 本地收藏（书签，与在线收藏星标区分）
    "bookmark": (
        '<path d="M6.5 3.5h11a1.5 1.5 0 0 1 1.5 1.5v16l-7-4.2L5 21V5a1.5 1.5 0 0 1 1.5-1.5z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    "bookmark_filled": (
        '<path d="M6.5 3.5h11a1.5 1.5 0 0 1 1.5 1.5v16l-7-4.2L5 21V5a1.5 1.5 0 0 1 1.5-1.5z" '
        'fill="{color}" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 评论
    "comment": (
        '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7 '
        'a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 我的评论
    "message_square": (
        '<path d="M20 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M8.5 8.5h7M8.5 12h4.5" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round"/>'
    ),
    # 下载
    "download": (
        '<path d="M12 3.5v11.5m0 0l-4.5-4.5M12 15l4.5-4.5M4.5 18.5v1a1.5 1.5 0 0 0 1.5 1.5h12a1.5 1.5 0 0 0 1.5-1.5v-1" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 存储 / 上传云端
    "cloud_upload": (
        '<path d="M7.5 18.5h-1a4 4 0 0 1-.4-7.98A5.5 5.5 0 0 1 16.8 9.2a3.75 3.75 0 0 1 1.2 7.3h-1.5" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M12 20.5v-8.5m0 0l-3 3m3-3l3 3" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 清理缓存
    "trash": (
        '<path d="M4.5 6.5h15M9.5 6.5V4.8A1.3 1.3 0 0 1 10.8 3.5h2.4a1.3 1.3 0 0 1 1.3 1.3v1.7'
        'M6.5 6.5l.8 12.2A1.8 1.8 0 0 0 9.1 20.5h5.8a1.8 1.8 0 0 0 1.8-1.8l.8-12.2'
        'M10 10.5v6M14 10.5v6" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 首页
    "home": (
        '<path d="M3.5 10.5L12 3.5l8.5 7M5.5 9v10.5a1.5 1.5 0 0 0 1.5 1.5h10a1.5 1.5 0 0 0 1.5-1.5V9" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M9.5 21v-6.5a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1V21" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 搜索
    "search": (
        '<circle cx="11" cy="11" r="7" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M20 20l-3.8-3.8" fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round"/>'
    ),
    # 分类与排行
    "grid": (
        '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<rect x="13.5" y="3.5" width="7" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<rect x="3.5" y="13.5" width="7" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<rect x="13.5" y="13.5" width="7" height="7" rx="1.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
    ),
    # 每周必看
    "calendar": (
        '<rect x="3.5" y="4.5" width="17" height="16" rx="2" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M8 2.8v3.4M16 2.8v3.4M3.5 9.5h17" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round"/>'
    ),
    # 观看记录
    "clock": (
        '<circle cx="12" cy="12" r="8.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M12 7.5v4.8l3.2 2" fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 本地记录
    "history": (
        '<path d="M3.5 12a8.5 8.5 0 1 0 2.5-6l-2.5 2.5M3.5 4.5v4h4" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M12 8v4l2.8 1.8" fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 本地漫画
    "folder": (
        '<path d="M3.5 6.5A1.5 1.5 0 0 1 5 5h4.2l2 2.2H19A1.5 1.5 0 0 1 20.5 8.7v9.8A1.5 1.5 0 0 1 19 20H5a1.5 1.5 0 0 1-1.5-1.5V6.5z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 网络存储 NAS
    "cloud": (
        '<path d="M7 18.5h10.5a4 4 0 0 0 .8-7.92A5.5 5.5 0 0 0 7.6 8.7 4.2 4.2 0 0 0 7 18.5z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 图片超分
    "sparkles": (
        '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linejoin="round"/>'
        '<path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2z" '
        'fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    # 批量超分
    "layers": (
        '<path d="M12 3.5L3.5 8 12 12.5 20.5 8 12 3.5z" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linejoin="round"/>'
        '<path d="M3.5 12.5L12 17l8.5-4.5M3.5 16.5L12 21l8.5-4.5" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 帮助
    "help": (
        '<circle cx="12" cy="12" r="8.5" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M9.5 9.3a2.6 2.6 0 0 1 5 .9c0 1.7-2.5 2.2-2.5 3.6" '
        'fill="none" stroke="{color}" stroke-width="1.85" stroke-linecap="round"/>'
        '<circle cx="12" cy="17.2" r="0.9" fill="{color}"/>'
    ),
    # 设置
    "settings": (
        '<circle cx="12" cy="12" r="3" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 '
        '1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06 '
        'a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09 '
        'a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.08 '
        'a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06 '
        'a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.08a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09 '
        'a1.65 1.65 0 0 0-1.51 1z" fill="none" stroke="{color}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 侧边栏折叠
    "sidebar": (
        '<rect x="3.5" y="4.5" width="17" height="15" rx="2" fill="none" stroke="{color}" stroke-width="1.85"/>'
        '<path d="M9 4.5v15" fill="none" stroke="{color}" stroke-width="1.85"/>'
    ),
}


def _RenderSvgPixmap(name: str, color: str, size: int = 20) -> QPixmap:
    key = (name, color, size)
    cached = _PIXMAP_CACHE.get(key)
    if cached is not None:
        return cached

    body = _SVG_PATHS[name].format(color=color)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{body}</svg>'
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))

    dpr = 2.0
    pxSize = int(size * dpr)
    pixmap = QPixmap(pxSize, pxSize)
    pixmap.fill(Qt.GlobalColor.transparent)
    pixmap.setDevicePixelRatio(dpr)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()

    _PIXMAP_CACHE[key] = pixmap
    return pixmap


def RenderSvgIcon(name: str, color: str, size: int = 20) -> QIcon:
    """Render a crisp 2x HiDPI QIcon from an inline SVG template."""
    key = (name, color, size)
    cached = _ICON_CACHE.get(key)
    if cached is not None:
        return cached

    icon = QIcon(_RenderSvgPixmap(name, color, size))
    _ICON_CACHE[key] = icon
    return icon


def RenderStatefulSvgIcon(name: str, normalColor: str, activeColor: str, size: int = 18) -> QIcon:
    """Render a checkable QIcon with distinct Off (normal) and On (checked) colors."""
    key = (name, normalColor, activeColor, size)
    cached = _STATEFUL_ICON_CACHE.get(key)
    if cached is not None:
        return cached

    icon = QIcon()
    normalPm = _RenderSvgPixmap(name, normalColor, size)
    activePm = _RenderSvgPixmap(name, activeColor, size)
    icon.addPixmap(normalPm, QIcon.Mode.Normal, QIcon.State.Off)
    icon.addPixmap(activePm, QIcon.Mode.Normal, QIcon.State.On)
    icon.addPixmap(activePm, QIcon.Mode.Active, QIcon.State.On)
    _STATEFUL_ICON_CACHE[key] = icon
    return icon
