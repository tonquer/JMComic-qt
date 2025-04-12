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
    Ver = GlobalItem(22)
    VerTime = GlobalItem("2024-10-15")

    # web url
    WebDnsList = GlobalItem([])
    Url = GlobalItem("https://18-comicblade.art")
    UrlList = GlobalItem(["https://18comic-hok.vip","https://18comic.vip","https://jmcomic.me","https://18comic-16promax.club","https://18comic.tw","https://18comic-doa.xyz"])

    # mobile url

    # Url2 = GlobalItem("https://www.jmapinode.biz")
    # PicUrl2 = GlobalItem("https://cdn-msp.jmapinodeudzn.net")
    Url2List = GlobalItem(["https://www.jmapiproxyxxx.vip",
                           "https://www.cdnblackmyth.vip",
                           "https://www.cdnblackmyth.xyz",
                           "https://www.jmapiproxyxxx.me"])

    ProxyApiDomain2 = GlobalItem("jm2-api.ggo.icu")
    ProxyImgDomain2 = GlobalItem("jm2-img.ggo.icu")

    PicUrlList = GlobalItem(
        ["https://cdn-msp.jmapinodeudzn.net", "https://cdn-msp2.jmapinodeudzn.net", "https://cdn-msp.jmapiproxy3.cc",
         "https://cdn-msp.jmapiproxy4.cc"])

    CdnApiUrl = GlobalItem("https://www.cdnxxx-proxy.vip")
    CdnImgUrl = GlobalItem("https://cdn-msp.jmapiproxy3.cc")
    ProxyApiUrl = GlobalItem("https://www.cdnxxx-proxy.vip")
    ProxyImgUrl = GlobalItem("https://cdn-msp.jmapiproxy3.cc")
    HeaderVer = GlobalItem("1.7.5")

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
