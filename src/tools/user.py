

class User:
    def __init__(self) -> None:
        super().__init__()
        self.uid = ""
        self.isLogin = False
        self.userName = ""
        self.title = ""
        self.level = ""
        self.favorites = 0
        self.canFavorites = 0
        self.coin = 0
        self.gender = ""
        self.userAttr = {}

    def Logout(self):
        self.isLogin = False
        self.uid = ""
        self.userName = ""
        return

    @property
    def imgUrl(self):
        if self.uid:
            return "/media/users/{}.jpg".format(self.uid)
        return ""

    @property
    def name(self):
        return self.userName

    # @property
    # def title(self):
    #     return self.userAttr.get("稱號", "")
    #
    # @property
    # def level(self):
    #     return self.userAttr.get("等級", "")
    #
    # @property
    # def canFavorites(self):
    #     return int(self.userAttr.get("可收藏數", 0))
    #
    # @property
    # def medalNum(self):
    #     return int(self.userAttr.get("勳章", 0))
    #
    # @property
    # def coin(self):
    #     return int(self.userAttr.get("JCoins", 0))