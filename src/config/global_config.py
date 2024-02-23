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
    Ver = GlobalItem(0)

    # web url
    WebDnsList = GlobalItem([])
    Url = GlobalItem("https://18comic-palworld.club")
    UrlList = GlobalItem(["https://18comic-palworld.club", "https://18comic.vip", "https://jmcomic.me", "https://18comic-palworld.vip"])

    # mobile url
    Url2 = GlobalItem("https://www.jmapinode.biz")
    PicUrl2 = GlobalItem("https://cdn-msp.jmapinodeudzn.net")
    Url2List = GlobalItem(["https://www.jmapinode.biz", "https://www.jmapinode.vip", "https://www.jmapinode3.top",
                                "https://www.jmapibranch2.cc"])
    PicUrlList = GlobalItem(
        ["https://cdn-msp.jmapinodeudzn.net", "https://cdn-msp2.jmapinodeudzn.net", "https://cdn-msp.jmapiproxy3.cc",
         "https://cdn-msp.jmapiproxy4.cc"])

    def __init__(self):
        pass

    @staticmethod
    def LoadSetting():
        try:
            for k, v in dict(Setting.GlobalConfig.value).items():
                Log.Debug("load global setting, k={}, v={}".format(k, v))
                value = getattr(GlobalConfig, k)
                if isinstance(value, GlobalItem) :
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
