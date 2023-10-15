import time

Url = "https://18comic.org/"       # 域名
UrlBack = "https://jmcomic.ggo.icu/"       # 域名


# Url = "https://jmcomic1.cc"       # 域名
Url2 = "https://www.asjmapihost.cc"       # 域名
# Url2 = "https://www.jmapibranch3.cc"       # 域名
PicUrl2 = "https://cdn-msp.jmapiproxy2.cc"       # 域名

Url2List = ["https://www.jmapinode1.cc", "https://www.jmapinode2.cc", "https://www.jmapinode3.cc", "https://www.jmapibranch2.cc"]
PicUrlList = ["https://cdn-msp.jmapiproxy1.cc", "https://cdn-msp.jmapiproxy2.cc", "https://cdn-msp.jmapiproxy3.cc", "https://cdn-msp.jmapiproxy4.cc"]
Now = int(time.time())
ProxyApiDomain = "api.bika.life"
ProxyImgDomain = "img.bika.life"

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
UpdateUrlApi = "https://api.github.com/repos/tonquer/JMComic-qt/releases"
UpdateUrlBack = "https://github.com/tonquer/JMComic-qt/"

UpdateUrl2 = "https://hub.ggo.icu/tonquer/JMComic-qt/releases/latest"
UpdateUrl2Api = "https://api.ggo.icu/repos/tonquer/JMComic-qt/releases"
UpdateUrl2Back = "https://hub.ggo.icu/tonquer/JMComic-qt/"

UpdateUrl3 = "https://hub.fastgit.xyz/tonquer/JMComic-qt/releases/latest"
UpdateUrl3Api = "https://api.fastgit.xyz/repos/tonquer/JMComic-qt/releases"
UpdateUrl3Back = "https://hub.fastgit.xyz/tonquer/JMComic-qt"

UpdateVersion = "v1.1.5"
RealVersion = "v1.1.5"
VersionTime = "2023-10-15"

Waifu2xVersion = "1.1.6"
LoginUserName = ""


# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0             # 当前正在使用的索引
UseCpuNum = 0
EncodeGpu = ""

Waifu2xPath = "waifu2x"

IsTips = 1

# 代理与分流相关
ProxyUrl1 = "https://github.com/tonquer/picacg-qt/discussions/48"
ProxyUrl2 = "https://hub.ggo.icu/tonquer/picacg-qt/discussions/48"
ProxyUrl3 = "https://hub.fastgit.xyz/tonquer/picacg-qt/discussions/48"

# ISSUES
Issues1 = "https://github.com/tonquer/JMComic-qt/issues"
Issues2 = "https://hub.ggo.icu/tonquer/JMComic-qt/issues"
Issues3 = "https://hub.fastgit.xyz/tonquer/JMComic-qt/issues"

# cookie
ipcountry = ""
ipm5 = ""
AVS = ""
shunt = ""

# ipcountry = "CN"
# ipm5 = "4f15409f804567cd4f4344fae94126e5"
# AVS = "fgb9t6q1o3bct86srh4v5kthg2"
# shunt = "1"