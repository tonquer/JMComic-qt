

class User:
    def __init__(self) -> None:
        super().__init__()
        self.isLogin = False
        self.userName = ""
        self.imgUrl = ""
        self.userAttr = {}

    @property
    def name(self):
        return self.userName

    @property
    def title(self):
        return self.userAttr.get("稱號", "")

    @property
    def level(self):
        return self.userAttr.get("等級", "")

    @property
    def canFavorites(self):
        return int(self.userAttr.get("可收藏數", 0))

    @property
    def medalNum(self):
        return int(self.userAttr.get("勳章", 0))

    @property
    def coin(self):
        return int(self.userAttr.get("JCoins", 0))