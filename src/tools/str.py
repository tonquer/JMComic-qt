from PySide6.QtCore import QObject, QCoreApplication


class QtStrObj(QObject):
    def __init__(self):
        QObject.__init__(self)


class Str:
    IconList = "๐๐๐๐๐๐๐๐๐ณ๐๐๐๐๐๐๐๐๐๐๐ด๐๐ฆ๐ง๐ฎ๐ฌ๐๐ฏ๐๐๐๐๐ฅ๐ฉ๐๐๐๐จ๐ฐ๐ฃ๐ข๐ญ๐๐ฒ๐ฑ๐ซ๐ ๐ก๐ค๐ช๐๐ท๐๐ต๐ฟ๐๐๐ถ๐๐ฝ๐๐๐๐๐๐๐๐๐ฆ๐ง๐ฉ๐จ๐ถ๐ต๐ด๐ฑ๐ฒ๐ณ๐ท๐ฎ๐ผ๐ธ๐บ๐ธ๐ป๐ฝ๐ผ๐๐ฟ๐น๐พ๐น๐บ๐๐๐๐๐๐พ๐๐๐ง๐๐๐๐๐๐ค๐ฅ๐ฌ๐ญ"

    obj = None
    strDict = dict()

    # Enum

    Ok = 1001              # "ๆๅ"
    Load = 1002            # "ๅ ่ฝฝ"
    Error = 1003           # "้่ฏฏ"
    WaitLoad = 1004        # "็ญๅพ"
    NetError = 1005        # "็ฝ็ป้่ฏฏ๏ผ่ฏทๆฃๆฅไปฃ็่ฎพ็ฝฎ"
    UserError = 1006       # "็จๆทๅๅฏ็ ้่ฏฏ"
    RegisterError = 1007   # "ๆณจๅๅคฑ่ดฅ"
    UnKnowError = 1008     # "ๆช็ฅ้่ฏฏ๏ผ"
    NotFoundBook = 1009    # "ๆชๆพๅฐไนฆ็ฑ"
    ParseError = 1010      # "่งฃๆๅบ้ไบ"
    NeedGoogle = 1011      # "้่ฆ่ฐทๆญ้ช่ฏ"
    SetHeadError = 1012    # "ๅคดๅ่ฎพ็ฝฎๅบ้ไบ, ่ฏทๅฐฝ้้ๆฉ500kbไปฅไธ็ๅพ็๏ผ"
    UnderReviewBook = 1013  # "ๆฌๅญๅฎกๆ ธไธญ"
    NotLogin = 1014         # "ๆช็ปๅฝ"
    SaveError = 1015         # "ไฟๅญๅบ้"
    Cache = 1016         # "็ผๅญ"
    AddError = 1017         # "Add้่ฏฏ"
    PathError = 1018         # "่ทฏๅพ้่ฏฏ"
    FileError = 1019         # "ๆชๅ็ฐๆบๆไปถ"
    FileFormatError = 1020   # "ๆไปถๆๅ"

    Success = 2001         # "ไธ่ฝฝๅฎๆ"
    Reading = 2002         # "่ทๅไฟกๆฏ"
    ReadingEps = 2003      # "่ทๅๅ้กต"
    ReadingPicture = 2004  # "่ทๅไธ่ฝฝๅฐๅ"
    DownloadCover = 2005   # "ๆญฃๅจไธ่ฝฝๅฐ้ข"
    Downloading = 2006     # "ๆญฃๅจไธ่ฝฝ"
    Waiting = 2007         # "็ญๅพไธญ"
    Pause = 2008           # "ๆๅ"
    DownError = 2009       # "ๅบ้ไบ"
    NotFound = 2010        # "ๅๅงๆไปถไธๅญๅจ"
    Converting = 2011      # "่ฝฌๆขไธญ"
    ConvertSuccess = 2012  # "่ฝฌๆขๆๅ"

    DownloadSuc = 3001     # "ไธ่ฝฝๅฎๆ"
    DownloadError = 3002   # "ไธ่ฝฝ้่ฏฏ"
    DownloadReset = 3003   # "้ๆฐไธ่ฝฝ"
    WaifuWait = 3004       # "็ญๅพไธญ"
    WaifuStateStart = 3005     # "่ฝฌๆขๅผๅง"
    WaifuStateCancle = 3006    # "ไธ่ฝฌๆข"
    WaifuStateEnd = 3007       # "่ฝฌๆขๅฎๆ"
    WaifuStateFail = 3008      # "่ฝฌๆขๅคฑ่ดฅ"
    OverResolution = 3009      # "่ถ่ฟ่ฎพ็ฝฎๅ่พจ็"

    LoadingPicture = 1     # "ๅพ็ๅ ่ฝฝไธญ..."
    LoadingFail = 2        # "ๅพ็ๅ ่ฝฝๅคฑ่ดฅ"
    LoginCookie = 3        # "ไฝฟ็จCookie็ปๅฝ"
    LoginUser = 4          # "ไฝฟ็จ่ดฆๅท็ปๅฝ"
    NotSpace = 5           # "ไธ่ฝไธบ็ฉบ"
    LoginFail = 6          # "็ปๅฝๅคฑ่ดฅ"

    Menu = 10              # ่ๅ
    FullSwitch = 11        # ๅจๅฑๅๆข
    ReadMode = 12          # ้่ฏปๆจกๅผ

    UpDownScroll = 13      # ไธไธๆปๅจ
    Default = 14           # ้ป่ฎค
    LeftRightDouble = 15   # ๅทฆๅณๅ้กต
    RightLeftDouble = 16   # ๅณๅทฆๅ้กต
    LeftRightScroll = 17   # ๅทฆๅณๆปๅจ
    RightLeftScroll = 18   # ๅณๅทฆๆปๅจ
    Scale = 19             # ็ผฉๆพ
    SwitchPage = 20        # ๅ้กต
    LastChapter = 21       # ไธไธ็ซ 
    NextChapter = 22       # ไธไธ็ซ 
    Exit = 23              # ้ๅบ
    AutoScroll = 24        # ่ชๅจๆปๅจ/็ฟป้กต
    ExitFullScreen = 25    # ้ๅบๅจๅฑ
    FullScreen = 26        # ๅจๅฑ
    ContinueRead = 27      # ็ปง็ปญ้่ฏป
    Page = 28              # ้กต
    AlreadyLastPage = 29   # ๅทฒ็ปๆฏ็ฌฌไธ้กต
    AlreadyNextPage = 30   # ๅทฒ็ปๆๅไธ้กต
    AutoSkipLast = 31      # ่ชๅจ่ทณ่ฝฌๅฐไธไธ็ซ 
    AutoSkipNext = 32      # ่ชๅจ่ทณ่ฝฌๅฐไธไธ็ซ 
    Position = 33          # ไฝ็ฝฎ
    Resolution = 34        # ๅ่พจ็
    Size = 35              # ๅคงๅฐ
    State = 36             # ็ถๆ
    DownloadNot = 37       # ไธ่ฝฝๆชๅฎๆ
    NotRecommendWaifu2x = 38  # Waifu2xๅฝๅไธบCPUๆจกๅผ๏ผ็ๅพๆจกๅผไธไธๆจ่ๅผๅฏ
    StopAutoScroll = 39    # ่ชๅจๆปๅจ/็ฟป้กตๅทฒๅๆญข
    LastPage = 40          # ไธไธ้กต
    NextPage = 41          # ไธไธ้กต
    LastScroll = 42        # ไธๆป
    NextScroll = 43        # ไธๆป
    NoProxy = 44           # ๆ ไปฃ็
    SaveSuc = 45           # ไฟๅญๆๅ
    Login = 46             # ็ปๅฝ
    Register = 47          # ๆณจๅ
    SpeedTest = 48         # ๆต้
    PasswordShort = 49     # ๅฏ็ ๅคช็ญ
    RegisterSuc = 50       # ๆณจๅๆๅ
    ComicFinished = 51     # ๅฎ็ป
    SelectFold = 52        # ้ๆฉๆไปถๅคน
    Save = 53              # ไฟๅญ
    CommentLoadFail = 54   # ่ฏ่ฎบๅ ่ฝฝๅคฑ่ดฅ
    Top = 55               # ็ฝฎ้กถ
    The = 56               # ็ฌฌ
    Floor = 57             # ๆฅผ
    DayAgo = 58            # ๅคฉๅ
    HourAgo = 59           # ๅฐๆถๅ
    MinuteAgo = 60         # ๅ้ๅ
    SecondAgo = 61         # ็งๅ
    FavoriteNum = 62       # ๆถ่ๆฐ
    FavoriteLoading = 63   # ๆญฃๅจๅ ่ฝฝๆถ่ๅ้กต
    Updated = 64           # ๆดๆฐๅฎๆ
    Picture = 65           # ๅพ็
    Sending = 66           # "ๆญฃๅจๅ้"
    OnlineNum = 67         # "ๅจ็บฟไบบๆฐ"
    AlreadyLastChapter = 68  # ๅทฒ็ปๆฏ็ฌฌไธ็ซ 
    AlreadyNextChapter = 69  # ๅทฒ็ปๆๅไธ็ซ 
    ChapterLoadFail = 70     # ็ซ ่ๅ ่ฝฝๅคฑ่ดฅ
    AddFavoriteSuc = 71      # ๆทปๅ ๆถ่ๆๅ
    Convert = 72             # ่ฝฌๆข
    CopySuc = 73             # ๅคๅถๆๅ
    HeadUpload = 74          # "ๅคดๅไธไผ ไธญ......"
    Update = 75              # ๆดๆฐ
    AlreadySign = 76         # ๅทฒๆๅก
    Sign = 77                # ๆๅก
    Hidden = 78              # ๅฑ่ฝ
    NotHidden = 79           # ๅๆถๅฑ่ฝ
    OpenDir = 80             # ๆๅผ็ฎๅฝ
    DeleteRecord = 81        # ๅ ้ค่ฎฐๅฝ
    DeleteRecordFile = 82    # ๅ ้ค่ฎฐๅฝๅๆไปถ
    SelectEps = 83           # ้ๆฉไธ่ฝฝ็ซ ่
    Start = 84               # ๅผๅง
    StartConvert = 85        # ๅผๅง่ฝฌๆข
    PauseConvert = 86        # ๆๅ่ฝฌๆข

    Open = 87                # ๆๅผ
    LookCover = 88           # ๆฅ็ๅฐ้ข
    ReDownloadCover = 89     # ้ไธๅฐ้ข
    Waifu2xConvert = 90      # Waifu2x่ฝฌๆข
    CopyTitle = 91           # ๅคๅถๆ ้ข
    Download = 92            # ไธ่ฝฝ
    Delete = 93              # ๅ ้ค
    CurVersion = 94          # ๅฝๅ็ๆฌ
    CheckUpdateAndUp = 95    # ๆฃๆฅๅฐๆดๆฐ๏ผๆฏๅฆๅๅพๆดๆฐ
    CopyAndroid = 96         # ๅคๅถAndroidไธ่ฝฝๅฐๅ
    CopyIos = 97             # ๅคๅถIOSไธ่ฝฝๅฐๅ
    SetDir = 98              # ่ฏท่ฎพ็ฝฎ็ฎๅฝ
    AddDownload = 99         # ๆทปๅ ไธ่ฝฝๆๅ
    LookFirst = 100          # ่ง็็ฌฌ1็ซ 
    LastLook = 101           # ไธๆฌก็ๅฐ็ฌฌ
    Chapter = 102            # ็ซ 
    Looked = 103             # ็่ฟ
    PressEnter = 104         # ๆEnterๅ้ๆถๆฏ
    PressCtrlEnter = 105     # ๆCtrl+Enterๅ้ๆถๆฏ
    DelWaifu2xConvert = 106     # ๅๆถWaifu2x่ฝฌๆข
    NeedResetSave = 107      # ้่ฆ้ๅฏไฟๅญ
    CheckUp = 108            # ๆฃๆฅๆดๆฐ
    DailyUpdated = 109            # ไปๆฅๅทฒๆดๆฐ
    HaveUpdate = 110            # ๆๆดๆฐ
    AlreadyUpdate = 111            # ๅทฒๆฏๆๆฐ
    AgoUpdate = 112                # ๆ่ฟๆดๆฐ
    LeaveMsg = 113                # ็่จๆฟ
    Rank = 114                # ๆ่กๆฆ
    RandomBook = 115                # ้ๆบๆฌๅญ
    DeleteSuc = 116                 # ๅ ้คๆๅ
    All = 117                       # ๆๆ
    Favorite = 118                  # ๆถ่
    Classify = 119                  # ๅ็ฑป
    Comment = 120                  # ่ฏ่ฎบ
    Change = 121                   # ๆดๆน
    SwitchSite = 122               # ่กจ้ๅๆข
    DelFavoriteSuc = 123           # ๅ ้คๆถ่ๆๅ
    AllComment = 124               # ๆๆ่ฏ่ฎบ
    Move = 125               # ็งปๅจ
    Add = 126                # ๆฐๅข
    SelectAll = 127                # ๅจ้
    NotSelectAll = 128             # ๅ้
    MyComment = 129          # ๆ็่ฏ่ฎบ
    LoginOut = 130                # ็ปๅบ
    Sock5Error = 131              # Sock5่ฎพ็ฝฎๅบ้

    @classmethod
    def Reload(cls):
        cls.obj = QtStrObj()
        cls.obj.setObjectName(u"ObjTr")
        cls.strDict[cls.Ok] = QCoreApplication.translate("cls.obj", "ๆๅ", None)
        cls.strDict[cls.Load] = QCoreApplication.translate("cls.obj",  "ๅ ่ฝฝ", None)
        cls.strDict[cls.Error] = QCoreApplication.translate("cls.obj",  "้่ฏฏ", None)
        cls.strDict[cls.WaitLoad] = QCoreApplication.translate("cls.obj",  "็ญๅพ", None)
        cls.strDict[cls.NetError] = QCoreApplication.translate("cls.obj",  "็ฝ็ป้่ฏฏ๏ผ่ฏทๆฃๆฅไปฃ็่ฎพ็ฝฎ", None)
        cls.strDict[cls.UserError] = QCoreApplication.translate("cls.obj",  "็จๆทๅๅฏ็ ้่ฏฏ", None)
        cls.strDict[cls.RegisterError] = QCoreApplication.translate("cls.obj",  "ๆณจๅๅคฑ่ดฅ", None)
        cls.strDict[cls.UnKnowError] = QCoreApplication.translate("cls.obj",  "ๆช็ฅ้่ฏฏ", None)
        cls.strDict[cls.NotFoundBook] = QCoreApplication.translate("cls.obj",  "ๆชๆพๅฐไนฆ็ฑ", None)
        cls.strDict[cls.ParseError] = QCoreApplication.translate("cls.obj",  "่งฃๆๅบ้ไบ", None)
        cls.strDict[cls.NeedGoogle] = QCoreApplication.translate("cls.obj",  "้่ฆ่ฐทๆญ้ช่ฏ", None)
        cls.strDict[cls.SetHeadError] = QCoreApplication.translate("cls.obj",  "ๅคดๅ่ฎพ็ฝฎๅบ้ไบ, ่ฏทๅฐฝ้้ๆฉ500kbไปฅไธ็ๅพ็", None)
        cls.strDict[cls.UnderReviewBook] = QCoreApplication.translate("cls.obj",  "ๆฌๅญๅฎกๆ ธไธญ", None)
        cls.strDict[cls.NotLogin] = QCoreApplication.translate("cls.obj",  "ๆช็ปๅฝ", None)
        cls.strDict[cls.SaveError] = QCoreApplication.translate("cls.obj",  "ไฟๅญๅบ้", None)
        cls.strDict[cls.Cache] = QCoreApplication.translate("cls.obj",  "็ผๅญ", None)
        cls.strDict[cls.AddError] = QCoreApplication.translate("cls.obj",  "Add้่ฏฏ", None)
        cls.strDict[cls.PathError] = QCoreApplication.translate("cls.obj",  "่ทฏๅพ้่ฏฏ", None)
        cls.strDict[cls.FileError] = QCoreApplication.translate("cls.obj",  "ๆชๅ็ฐๆบๆไปถ", None)
        cls.strDict[cls.FileFormatError] = QCoreApplication.translate("cls.obj",  "ๆไปถๆๅ", None)

        cls.strDict[cls.LoadingPicture] = QCoreApplication.translate("cls.obj",  "ๅพ็ๅ ่ฝฝไธญ...", None)
        cls.strDict[cls.LoadingFail] = QCoreApplication.translate("cls.obj",  "ๅพ็ๅ ่ฝฝๅคฑ่ดฅ", None)
        cls.strDict[cls.LoginCookie] = QCoreApplication.translate("cls.obj",  "ไฝฟ็จCookie็ปๅฝ", None)
        cls.strDict[cls.LoginUser] = QCoreApplication.translate("cls.obj",  "ไฝฟ็จ่ดฆๅท็ปๅฝ", None)
        cls.strDict[cls.NotSpace] = QCoreApplication.translate("cls.obj",  "ไธ่ฝไธบ็ฉบ", None)
        cls.strDict[cls.LoginFail] = QCoreApplication.translate("cls.obj",  "็ปๅฝๅคฑ่ดฅ", None)
        cls.strDict[cls.Success] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฝๅฎๆ", None)
        cls.strDict[cls.Reading] = QCoreApplication.translate("cls.obj",  "่ทๅไฟกๆฏ", None)
        cls.strDict[cls.ReadingEps] = QCoreApplication.translate("cls.obj",  "่ทๅๅ้กต", None)
        cls.strDict[cls.ReadingPicture] = QCoreApplication.translate("cls.obj",  "่ทๅไธ่ฝฝๅฐๅ", None)
        cls.strDict[cls.DownloadCover] = QCoreApplication.translate("cls.obj",  "ๆญฃๅจไธ่ฝฝๅฐ้ข", None)
        cls.strDict[cls.Downloading] = QCoreApplication.translate("cls.obj",  "ๆญฃๅจไธ่ฝฝ", None)
        cls.strDict[cls.Waiting] = QCoreApplication.translate("cls.obj",  "็ญๅพไธญ", None)
        cls.strDict[cls.Pause] = QCoreApplication.translate("cls.obj",  "ๆๅ", None)
        cls.strDict[cls.DownError] = QCoreApplication.translate("cls.obj",  "ๅบ้ไบ", None)
        cls.strDict[cls.NotFound] = QCoreApplication.translate("cls.obj",  "ๅๅงๆไปถไธๅญๅจ", None)
        cls.strDict[cls.Converting] = QCoreApplication.translate("cls.obj",  "่ฝฌๆขไธญ", None)
        cls.strDict[cls.ConvertSuccess] = QCoreApplication.translate("cls.obj",  "่ฝฌๆขๆๅ", None)
        cls.strDict[cls.DownloadSuc] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฝๅฎๆ", None)
        cls.strDict[cls.DownloadError] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฝ้่ฏฏ", None)
        cls.strDict[cls.DownloadReset] = QCoreApplication.translate("cls.obj",  "้ๆฐไธ่ฝฝ", None)
        cls.strDict[cls.WaifuWait] = QCoreApplication.translate("cls.obj",  "็ญๅพไธญ", None)
        cls.strDict[cls.WaifuStateStart] = QCoreApplication.translate("cls.obj",  "่ฝฌๆขๅผๅง", None)
        cls.strDict[cls.WaifuStateCancle] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฌๆข", None)
        cls.strDict[cls.WaifuStateEnd] = QCoreApplication.translate("cls.obj",  "่ฝฌๆขๅฎๆ", None)
        cls.strDict[cls.WaifuStateFail] = QCoreApplication.translate("cls.obj",  "่ฝฌๆขๅคฑ่ดฅ", None)
        cls.strDict[cls.OverResolution] = QCoreApplication.translate("cls.obj",  "่ถ่ฟ่ฎพ็ฝฎๅ่พจ็", None)

        cls.strDict[cls.Menu] = QCoreApplication.translate("cls.obj",  "่ๅ", None)
        cls.strDict[cls.FullSwitch] = QCoreApplication.translate("cls.obj",  "ๅจๅฑๅๆข", None)
        cls.strDict[cls.ReadMode] = QCoreApplication.translate("cls.obj",  "้่ฏปๆจกๅผ", None)
        cls.strDict[cls.UpDownScroll] = QCoreApplication.translate("cls.obj",  "ไธไธๆปๅจ", None)
        cls.strDict[cls.Default] = QCoreApplication.translate("cls.obj",  "้ป่ฎค", None)
        cls.strDict[cls.LeftRightDouble] = QCoreApplication.translate("cls.obj",  "ๅทฆๅณๅ้กต", None)
        cls.strDict[cls.RightLeftDouble] = QCoreApplication.translate("cls.obj",  "ๅณๅทฆๅ้กต", None)
        cls.strDict[cls.LeftRightScroll] = QCoreApplication.translate("cls.obj",  "ๅทฆๅณๆปๅจ", None)
        cls.strDict[cls.RightLeftScroll] = QCoreApplication.translate("cls.obj",  "ๅณๅทฆๆปๅจ", None)
        cls.strDict[cls.Scale] = QCoreApplication.translate("cls.obj",  "็ผฉๆพ", None)
        cls.strDict[cls.SwitchPage] = QCoreApplication.translate("cls.obj",  "ๅ้กต", None)
        cls.strDict[cls.LastChapter ]= QCoreApplication.translate("cls.obj",  "ไธไธ็ซ ", None)
        cls.strDict[cls.NextChapter] = QCoreApplication.translate("cls.obj",  "ไธไธ็ซ ", None)
        cls.strDict[cls.Exit] = QCoreApplication.translate("cls.obj",  "้ๅบ", None)
        cls.strDict[cls.AutoScroll] = QCoreApplication.translate("cls.obj",  "่ชๅจๆปๅจ/็ฟป้กต", None)
        cls.strDict[cls.ExitFullScreen] = QCoreApplication.translate("cls.obj",  "้ๅบๅจๅฑ", None)
        cls.strDict[cls.FullScreen] = QCoreApplication.translate("cls.obj",  "ๅจๅฑ", None)
        cls.strDict[cls.ContinueRead] = QCoreApplication.translate("cls.obj",  "็ปง็ปญ้่ฏป", None)
        cls.strDict[cls.Page] = QCoreApplication.translate("cls.obj",  "้กต", None)
        cls.strDict[cls.AlreadyLastPage] = QCoreApplication.translate("cls.obj",  "ๅทฒ็ปๆฏ็ฌฌไธ้กต", None)
        cls.strDict[cls.AlreadyNextPage] = QCoreApplication.translate("cls.obj",  "ๅทฒ็ปๆๅไธ้กต", None)
        cls.strDict[cls.AutoSkipLast] = QCoreApplication.translate("cls.obj",  "่ชๅจ่ทณ่ฝฌๅฐไธไธ็ซ ", None)
        cls.strDict[cls.AutoSkipNext] = QCoreApplication.translate("cls.obj",  "่ชๅจ่ทณ่ฝฌๅฐไธไธ็ซ ", None)
        cls.strDict[cls.Position] = QCoreApplication.translate("cls.obj",  "ไฝ็ฝฎ", None)
        cls.strDict[cls.Resolution] = QCoreApplication.translate("cls.obj",  "ๅ่พจ็", None)
        cls.strDict[cls.Size] = QCoreApplication.translate("cls.obj",  "ๅคงๅฐ", None)
        cls.strDict[cls.State] = QCoreApplication.translate("cls.obj",  "็ถๆ", None)
        cls.strDict[cls.DownloadNot] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฝๆชๅฎๆ", None)
        cls.strDict[cls.NotRecommendWaifu2x] = QCoreApplication.translate("cls.obj",  "Waifu2xๅฝๅไธบCPUๆจกๅผ๏ผ็ๅพๆจกๅผไธไธๆจ่ๅผๅฏ", None)
        cls.strDict[cls.StopAutoScroll] = QCoreApplication.translate("cls.obj",  "่ชๅจๆปๅจ/็ฟป้กตๅทฒๅๆญข", None)
        cls.strDict[cls.LastPage] = QCoreApplication.translate("cls.obj",  "ไธไธ้กต", None)
        cls.strDict[cls.NextPage] = QCoreApplication.translate("cls.obj",  "ไธไธ้กต", None)
        cls.strDict[cls.LastScroll] = QCoreApplication.translate("cls.obj",  "ไธๆป", None)
        cls.strDict[cls.NextScroll] = QCoreApplication.translate("cls.obj",  "ไธๆป", None)

        cls.strDict[cls.NoProxy] = QCoreApplication.translate("cls.obj",  "ๆ ไปฃ็", None)
        cls.strDict[cls.SaveSuc] = QCoreApplication.translate("cls.obj",  "ไฟๅญๆๅ", None)
        cls.strDict[cls.Login] = QCoreApplication.translate("cls.obj",  "็ปๅฝ", None)
        cls.strDict[cls.Register] = QCoreApplication.translate("cls.obj",  "ๆณจๅ", None)
        cls.strDict[cls.SpeedTest] = QCoreApplication.translate("cls.obj",  "ๆต้", None)
        cls.strDict[cls.PasswordShort] = QCoreApplication.translate("cls.obj",  "ๅฏ็ ๅคช็ญ", None)
        cls.strDict[cls.RegisterSuc] = QCoreApplication.translate("cls.obj",  "ๆณจๅๆๅ", None)
        cls.strDict[cls.ComicFinished] = QCoreApplication.translate("cls.obj",  "ๅฎ็ป", None)
        cls.strDict[cls.SelectFold] = QCoreApplication.translate("cls.obj",  "้ๆฉๆไปถๅคน", None)
        cls.strDict[cls.Save] = QCoreApplication.translate("cls.obj",  "ไฟๅญ", None)
        cls.strDict[cls.CommentLoadFail] = QCoreApplication.translate("cls.obj",  "่ฏ่ฎบๅ ่ฝฝๅคฑ่ดฅ", None)
        cls.strDict[cls.Top] = QCoreApplication.translate("cls.obj",  "็ฝฎ้กถ", None)
        cls.strDict[cls.The] = QCoreApplication.translate("cls.obj",  "็ฌฌ", None)
        cls.strDict[cls.Floor] = QCoreApplication.translate("cls.obj",  "ๆฅผ", None)
        cls.strDict[cls.DayAgo] = QCoreApplication.translate("cls.obj",  "ๅคฉๅ", None)
        cls.strDict[cls.HourAgo] = QCoreApplication.translate("cls.obj",  "ๅฐๆถๅ", None)
        cls.strDict[cls.MinuteAgo] = QCoreApplication.translate("cls.obj",  "ๅ้ๅ", None)
        cls.strDict[cls.SecondAgo] = QCoreApplication.translate("cls.obj",  "็งๅ", None)
        cls.strDict[cls.FavoriteNum] = QCoreApplication.translate("cls.obj",  "ๆถ่ๆฐ", None)
        cls.strDict[cls.FavoriteLoading] = QCoreApplication.translate("cls.obj",  "ๆญฃๅจๅ ่ฝฝๆถ่ๅ้กต", None)
        cls.strDict[cls.Updated] = QCoreApplication.translate("cls.obj",  "ๆดๆฐๅฎๆ", None)
        cls.strDict[cls.Picture] = QCoreApplication.translate("cls.obj",  "ๅพ็", None)
        cls.strDict[cls.Sending] = QCoreApplication.translate("cls.obj",  "ๆญฃๅจๅ้", None)
        cls.strDict[cls.OnlineNum] = QCoreApplication.translate("cls.obj",  "ๅจ็บฟไบบๆฐ", None)
        cls.strDict[cls.AlreadyLastChapter] = QCoreApplication.translate("cls.obj",  "ๅทฒ็ปๆฏ็ฌฌไธ็ซ ", None)
        cls.strDict[cls.AlreadyNextChapter] = QCoreApplication.translate("cls.obj",  "ๅทฒ็ปๆๅไธ็ซ ", None)
        cls.strDict[cls.ChapterLoadFail] = QCoreApplication.translate("cls.obj",  "็ซ ่ๅ ่ฝฝๅคฑ่ดฅ", None)
        cls.strDict[cls.AddFavoriteSuc] = QCoreApplication.translate("cls.obj",  "ๆทปๅ ๆถ่ๆๅ", None)
        cls.strDict[cls.Convert] = QCoreApplication.translate("cls.obj",  "่ฝฌๆข", None)
        cls.strDict[cls.CopySuc] = QCoreApplication.translate("cls.obj",  "ๅคๅถๆๅ", None)
        cls.strDict[cls.HeadUpload] = QCoreApplication.translate("cls.obj",  "ๅคดๅไธไผ ไธญ......", None)
        cls.strDict[cls.Update] = QCoreApplication.translate("cls.obj",  "ๆดๆฐ", None)
        cls.strDict[cls.AlreadySign] = QCoreApplication.translate("cls.obj",  "ๅทฒๆๅก", None)
        cls.strDict[cls.Sign] = QCoreApplication.translate("cls.obj",  "ๆๅก", None)
        cls.strDict[cls.Hidden] = QCoreApplication.translate("cls.obj",  "ๅฑ่ฝ", None)
        cls.strDict[cls.NotHidden] = QCoreApplication.translate("cls.obj",  "ๅๆถๅฑ่ฝ", None)
        cls.strDict[cls.OpenDir] = QCoreApplication.translate("cls.obj",  "ๆๅผ็ฎๅฝ", None)
        cls.strDict[cls.DeleteRecord] = QCoreApplication.translate("cls.obj",  "ๅ ้ค่ฎฐๅฝ", None)
        cls.strDict[cls.DeleteRecordFile] = QCoreApplication.translate("cls.obj",  "ๅ ้ค่ฎฐๅฝๅๆไปถ ", None)
        cls.strDict[cls.SelectEps] = QCoreApplication.translate("cls.obj",  "้ๆฉไธ่ฝฝ็ซ ่", None)
        cls.strDict[cls.Start] = QCoreApplication.translate("cls.obj",  "ๅผๅง", None)
        cls.strDict[cls.StartConvert] = QCoreApplication.translate("cls.obj",  "ๅผๅง่ฝฌๆข", None)
        cls.strDict[cls.PauseConvert] = QCoreApplication.translate("cls.obj",  "ๆๅ่ฝฌๆข", None)
        cls.strDict[cls.Open] = QCoreApplication.translate("cls.obj",  "ๆๅผ", None)
        cls.strDict[cls.LookCover] = QCoreApplication.translate("cls.obj",  "ๆฅ็ๅฐ้ข", None)
        cls.strDict[cls.ReDownloadCover] = QCoreApplication.translate("cls.obj",  "้ไธๅฐ้ข", None)
        cls.strDict[cls.Waifu2xConvert] = QCoreApplication.translate("cls.obj",  "Waifu2x่ฝฌๆข", None)
        cls.strDict[cls.CopyTitle] = QCoreApplication.translate("cls.obj",  "ๅคๅถๆ ้ข", None)
        cls.strDict[cls.Download] = QCoreApplication.translate("cls.obj",  "ไธ่ฝฝ", None)
        cls.strDict[cls.Delete] = QCoreApplication.translate("cls.obj",  "ๅ ้ค", None)
        cls.strDict[cls.CurVersion] = QCoreApplication.translate("cls.obj",  "ๅฝๅ็ๆฌ", None)
        cls.strDict[cls.CheckUpdateAndUp] = QCoreApplication.translate("cls.obj",  "ๆฃๆฅๅฐๆดๆฐ๏ผๆฏๅฆๅๅพๆดๆฐ", None)
        cls.strDict[cls.CopyAndroid] = QCoreApplication.translate("cls.obj",  "ๅคๅถAndroidไธ่ฝฝๅฐๅ", None)
        cls.strDict[cls.CopyIos] = QCoreApplication.translate("cls.obj",  "ๅคๅถIOSไธ่ฝฝๅฐๅ", None)
        cls.strDict[cls.SetDir] = QCoreApplication.translate("cls.obj",  "่ฏท่ฎพ็ฝฎ็ฎๅฝ", None)
        cls.strDict[cls.AddDownload] = QCoreApplication.translate("cls.obj",  "ๆทปๅ ไธ่ฝฝๆๅ", None)
        cls.strDict[cls.LookFirst] = QCoreApplication.translate("cls.obj",  "่ง็็ฌฌ1็ซ ", None)
        cls.strDict[cls.LastLook] = QCoreApplication.translate("cls.obj",  "ไธๆฌก็ๅฐ็ฌฌ", None)
        cls.strDict[cls.Chapter] = QCoreApplication.translate("cls.obj",  "็ซ ", None)
        cls.strDict[cls.Looked] = QCoreApplication.translate("cls.obj",  "็่ฟ", None)
        cls.strDict[cls.PressEnter] = QCoreApplication.translate("cls.obj",  "ๆEnterๅ้ๆถๆฏ", None)
        cls.strDict[cls.PressCtrlEnter] = QCoreApplication.translate("cls.obj",  "ๆCtrl+Enterๅ้ๆถๆฏ", None)
        cls.strDict[cls.DelWaifu2xConvert] = QCoreApplication.translate("cls.obj",  "ๅๆถWaifu2x่ฝฌๆข", None)
        cls.strDict[cls.NeedResetSave] = QCoreApplication.translate("cls.obj",  "้่ฆ้ๅฏไฟๅญ", None)
        cls.strDict[cls.CheckUp] = QCoreApplication.translate("cls.obj",  "ๆฃๆฅๆดๆฐ", None)
        cls.strDict[cls.DailyUpdated] = QCoreApplication.translate("cls.obj",  "ไปๆฅๅทฒๆดๆฐ", None)
        cls.strDict[cls.HaveUpdate] = QCoreApplication.translate("cls.obj",  "ๆๆดๆฐ", None)
        cls.strDict[cls.AlreadyUpdate] = QCoreApplication.translate("cls.obj",  "ๅทฒๆฏๆๆฐ", None)
        cls.strDict[cls.AgoUpdate] = QCoreApplication.translate("cls.obj",  "ๆ่ฟๆดๆฐ", None)
        cls.strDict[cls.LeaveMsg] = QCoreApplication.translate("cls.obj",  "็่จๆฟ", None)
        cls.strDict[cls.Rank] = QCoreApplication.translate("cls.obj",  "ๆ่ก็", None)
        cls.strDict[cls.RandomBook] = QCoreApplication.translate("cls.obj",  "้ๆบๆฌๅญ", None)
        cls.strDict[cls.DeleteSuc] = QCoreApplication.translate("cls.obj",  "ๅ ้คๆๅ", None)
        cls.strDict[cls.All] = QCoreApplication.translate("cls.obj",  "ๆๆ", None)
        cls.strDict[cls.Favorite] = QCoreApplication.translate("cls.obj",  "ๆถ่", None)
        cls.strDict[cls.Classify] = QCoreApplication.translate("cls.obj",  "ๅ็ฑป", None)
        cls.strDict[cls.Comment] = QCoreApplication.translate("cls.obj",  "่ฏ่ฎบ", None)
        cls.strDict[cls.Change] = QCoreApplication.translate("cls.obj",  "ๆดๆน", None)
        cls.strDict[cls.SwitchSite] = QCoreApplication.translate("cls.obj",  "่กจ้ๅๆข", None)
        cls.strDict[cls.DelFavoriteSuc] = QCoreApplication.translate("cls.obj",  "ๅ ้คๆถ่ๆๅ", None)
        cls.strDict[cls.AllComment] = QCoreApplication.translate("cls.obj",  "ๆๆ่ฏ่ฎบ", None)
        cls.strDict[cls.Move] = QCoreApplication.translate("cls.obj",  "็งปๅจ", None)
        cls.strDict[cls.Add] = QCoreApplication.translate("cls.obj",  "ๆฐๅข", None)
        cls.strDict[cls.SelectAll] = QCoreApplication.translate("cls.obj",  "ๅจ้", None)
        cls.strDict[cls.NotSelectAll] = QCoreApplication.translate("cls.obj",  "ๅ้", None)
        cls.strDict[cls.MyComment] = QCoreApplication.translate("cls.obj",  "ๆ็่ฏ่ฎบ", None)
        cls.strDict[cls.LoginOut] = QCoreApplication.translate("cls.obj",  "็ปๅบ", None)
        cls.strDict[cls.Sock5Error] = QCoreApplication.translate("cls.obj",  "Sock5่ฎพ็ฝฎๅบ้", None)

    @classmethod
    def GetStr(cls, enumType):
        return cls.strDict.get(enumType, "")

    @classmethod
    def CheckStr(cls):
        allEnum = set()
        for name in dir(cls):
            value = getattr(cls, name)
            if not isinstance(value, int):
                continue
            if value in allEnum:
                raise Exception("Already exists str: " + name)
            allEnum.add(value)
            if value not in cls.strDict:
                raise Exception("Not Found str: " + name)


if __name__ == "__main__":
    Str.Reload()
    Str.CheckStr()