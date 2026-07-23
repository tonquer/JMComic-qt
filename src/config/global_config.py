from config.setting import Setting
from tools.log import Log
from tools.singleton import Singleton


class GlobalItem(object):
    def __init__(self, default):
        self.value = default
        self.def_value = default

    def is_same(self):
        return self.value == self.def_value

    def set_value(self, value):
        if isinstance(self.def_value, int):
            self.value = int(value)
        elif isinstance(self.def_value, list) and isinstance(value, str):
            self.value = value.split(",")
        else:
            self.value = value


class GlobalConfig:
    Ver = GlobalItem(70)
    VerTime = GlobalItem("2026-6-20")

    # web url
    WebDnsList = GlobalItem([])
    JmFbUrl = GlobalItem("https://jmcomicog.net")

    Url = GlobalItem("https://18-comicblade.art")
    UrlList = GlobalItem(["https://comic18j-yodo.net",
                          "https://18comic.vip",
                          "https://jmcomic.me",
                          "https://18comic.tw",
                          "https://jmcomic-zzz.org",
                          "https://comic18j-robo.net",
                          "https://comic18j-lodo.net"])

    # mobile url

    # Url2 = GlobalItem("https://www.jmapinode.biz")
    # PicUrl2 = GlobalItem("https://cdn-msp.jmapinodeudzn.net")
    Url2List = GlobalItem(["https://www.cdnhjk.net",
                           "https://www.cdngwc.cc",
                           "https://www.cdngwc.net",
                           "https://www.cdngwc.club"])

    ProxyApiDomain2 = GlobalItem("jm2-api.jpacg.cc")
    ProxyImgDomain2 = GlobalItem("jm2-img.jpacg.cc")

    PicUrlList = GlobalItem(
        [
            "https://cdn-msp.jmapiproxy1.cc",
            "https://cdn-msp.jmapiproxy3.cc",
            "https://cdn-msp.jmapinodeudzn.net",
            "https://cdn-msp.jmdanjonproxy.xyz",
        ])

    ImgAutoUrl = GlobalItem([
        "cdn-msp2.jmapiproxy1.cc",
        "cdn-msp2.jmapiproxy3.cc",
        "cdn-msp2.jmapinodeudzn.net",
        "cdn-msp3.jmapinodeudzn.net",
        "cdn-msp3.jmapiproxy1.cc",
        "cdn-msp3.jmapiproxy3.cc",
    ])

    # ApiAutoUrl = GlobalItem([
    #     "www.cdn-mspjmapiproxy.xyz",
    # ])

    CdnApiUrl = GlobalItem("https://www.cdnhjk.net")
    CdnImgUrl = GlobalItem("https://cdn-msp.jmapiproxy3.cc")
    ProxyApiUrl = GlobalItem("https://www.cdnhjk.net")
    ProxyImgUrl = GlobalItem("https://cdn-msp.jmapiproxy3.cc")
    HeaderVer = GlobalItem("2.0.26")
    JMServerUrl = GlobalItem("https://rup4a04-c01.tos-ap-southeast-1.bytepluses.com/newsvr-2025.txt")

    # 非CF域名
    # NoHttp3Url = GlobalItem([
    #     "rup4a04-c01.tos-ap-southeast-1.bytepluses.com",
    #     "jpacg.cc",
    # ])

    DohUrlList = GlobalItem(["https://parse.jpacg.cc/parse",
                             "https://doh.pub/dns-query",
                             "https://dot.pub/dns-query"])
    EchDomain = GlobalItem("cloudflare-ech.com")
    
    ProxyIpList = GlobalItem([
"158.180.231.216",
"150.136.87.192",
"43.170.8.95",
"150.136.219.11",
"159.89.91.17",
"165.232.51.34",
"172.174.11.248",
"198.199.84.192",
"43.153.105.7",
"43.170.25.96",
"103.7.138.56",
"107.151.188.57",
"107.172.32.207",
"129.213.150.222",
"147.75.230.33",
"192.9.250.241",
"47.251.95.178",
"152.70.232.72",
"158.180.231.216",
"95.216.46.85",
"152.70.232.72",
"144.24.73.232",
"107.172.145.153",
"158.180.231.216",
"43.170.8.95",
"46.224.21.216",
"91.99.20.251",
"178.104.46.210",
"204.168.238.95",
"62.238.51.190",
])
    BestCfIpList = GlobalItem([
"104.18.40.104",
"172.64.229.155",
"198.41.208.26",
"162.159.39.157",  # CF 电信优选
"188.164.248.179",  # CF 电信优选
"162.159.32.130",  # CF 电信优选
"8.39.125.218", # CF 电信优选
"172.67.74.21",  # CF 联通优选
"172.67.74.74",  # CF 联通优选
"104.26.15.77",  # CF 联通优选
"104.26.9.248",  # CF 联通优选
"104.17.159.180",  # CF 移动优选
"104.18.33.232",  # CF 移动优选
"172.66.0.147",  # CF 移动优选
"91.193.58.245",  # CF 移动优选
"2606:4700:0:f920:12e9:bef7:bd1b:bf3",
"2606:4700:0:77:ba66:ef50:489c:299d",
"2606:4700:0:a0:6574:f93:6c28:17c5",
"2606:4700::2d:a321:64d3",
"2606:4700:0:a0:a55f:f7f9:5a17:8b8e",
"2606:4700:0:e0:9996:e26c:4b53:e69a",
"2606:4700:0:a0:65dc:517c:ad49:a2fd",
"2606:4700:0:f920:12c2:bb61:198a:ca56",
"2606:4700:0:e0:c653:a255:83dc:d0c"])

    def __init__(self):
        pass

    @staticmethod
    def GetApiUrl():
        return GlobalConfig.GetApiUrl2(Setting.ProxySelectIndex.value)

    @staticmethod
    def GetApiUrl2(index):
        if index == 5:
            return GlobalConfig.CdnApiUrl.value
        elif index == 6:
            return GlobalConfig.ProxyApiUrl.value
        elif index >= 7:
            return GlobalConfig.Url2List.value[0]
        return GlobalConfig.Url2List.value[index-1]

    @staticmethod
    def GetImgUrl():
        return GlobalConfig.GetImgUrl2(Setting.ProxyImgSelectIndex.value)

    @staticmethod
    def GetImgUrl2(index):
        if index == 5:
            return GlobalConfig.CdnImgUrl.value
        elif index == 6:
            return GlobalConfig.ProxyImgUrl.value
        elif index >= 7:
            return GlobalConfig.PicUrlList.value[0]
        return GlobalConfig.PicUrlList.value[index-1]


    @staticmethod
    def LoadSetting():
        try:
            newKv = {}
            for k, v in dict(Setting.GlobalConfig.value).items():
                Log.Debug("load global setting, k={}, v={}".format(k, v))
                newKv[k] = v
            oldV = newKv.get("Ver", 0)
            if GlobalConfig.Ver.value > oldV:
                Log.Debug("can not load old config, ver:{}->{}".format(oldV, GlobalConfig.Ver.value))
            else:
                for k, v in newKv.items():
                    value = getattr(GlobalConfig, k, "")
                    if isinstance(value, GlobalItem):
                        value.set_value(v)
        except Exception as es:
            Log.Error(es)
        pass

    @staticmethod
    def SaveSetting():
        saveData = {}
        try:
            for name in dir(GlobalConfig):
                value = getattr(GlobalConfig, name)
                if isinstance(value, GlobalItem) and not value.is_same():
                    saveData[name] = value.value
            Setting.GlobalConfig.SetValue(saveData)
        except Exception as es:
            Log.Error(es)
        pass

    @staticmethod
    def SetSetting(k, v):
        value = getattr(GlobalConfig, k)
        if isinstance(value, GlobalItem):
            Log.Info("set setting, k:{}, v:{}".format(k, v))
            value.set_value(v)
            GlobalConfig.SaveSetting()

    # 下载配置文件
    @staticmethod
    def UpdateSetting(data):
        allKvs = {}
        for v in data.replace("\r", "").split("\n"):
            if not v:
                continue
            [k, v2] = v.split("=")
            allKvs[k] = v2
        ver = int(allKvs.get("Ver", 0))
        if ver > GlobalConfig.Ver.value:
            Log.Info("update setting, {}".format(allKvs))
            for name, value in allKvs.items():
                item = getattr(GlobalConfig, name)
                if isinstance(item, GlobalItem):
                    item.set_value(value)
            GlobalConfig.SaveSetting()
        pass
