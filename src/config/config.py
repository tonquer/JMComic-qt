import time

Url = "https://18comic.org"       # 域名
# Url = "https://jmcomic1.cc"       # 域名
Url2 = "https://www.asjmapihost.cc"       # 域名
# Url2 = "https://www.jmapibranch3.cc"       # 域名
PicUrl2 = "https://cdn-msp.jmapiproxy2.cc"       # 域名
Now = int(time.time())

ThreadNum = 10                 # 线程
DownloadThreadNum = 5          # 下载线程
ConvertThreadNum = 3           # 转换线程
ChatSavePath = "chat"
SavePathDir = "commies"        # 下载目录
ResetCnt = 5                   # 下载重试次数

IsUseCache = True              # 是否使用cache
CachePathDir = "cache"         # cache目录
# CacheExpired = 24 * 60 * 60  # cache过期时间24小时
PreLoading = 10                # 预加载5页
PreLook = 4                    # 预显示

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/JMComic-qt/releases/latest"
UpdateUrlBack = "https://github.com/tonquer/JMComic-qt/"
UpdateUrl2 = "https://hub.fastgit.org/JMComic-qt/releases/latest"
UpdateUrl2Back = "https://hub.fastgit.org/tonquer/JMComic-qt/"


UpdateVersion = "v1.0.1"
RealVersion = "v1.0.1"
VersionTime = "2022-1-2"

Waifu2xVersion = "1.1.1"
LoginUserName = ""


# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0             # 当前正在使用的索引
UseCpuNum = 0
EncodeGpu = ""

Waifu2xPath = "waifu2x"

IsTips = 1

# ISSUES
Issues = "https://github.com/tonquer/JMComic-qt/issues"

