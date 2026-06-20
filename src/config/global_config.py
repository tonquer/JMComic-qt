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
        elif index == 7:
            from tools.tool import ToolUtil
            return "https://" + ToolUtil.GetUrlHost(Setting.HostApiDomain.value)
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
        elif index == 7:
            from tools.tool import ToolUtil
            return "https://" + ToolUtil.GetUrlHost(Setting.HostImgDomain.value)
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
