from config import config
from config.setting import Setting
from tools.tool import ToolUtil


class BaseRes(object):
    def __init__(self, data, isParseRes) -> None:
        self.raw = data
        self.data = {}
        self.message = ""
        self.reqBak = None
        self.isParseRes = isParseRes
        if isParseRes:
            ToolUtil.ParseFromData(self, self.raw.text)

    @property
    def code(self):
        if hasattr(self.raw, "status_code"):
            return self.raw.status_code
        else:
            return 0

    def __str__(self):
        if Setting.LogIndex.value == 0:
            return ""
        elif Setting.LogIndex.value == 1:
            return "code:{}".format(self.code)

        if self.isParseRes:
            data = self.GetText()
        else:
            data = ""
        return "code:{}, raw:{}".format(self.code, data.replace("\n", ""))

    def GetText(self):
        if hasattr(self.raw, "text"):
            return self.raw.text
        return ""

    def GetContent(self):
        if hasattr(self.raw, "content"):
            return self.raw.content
        return b""