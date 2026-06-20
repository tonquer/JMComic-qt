import os
import uuid

import smbclient
from task.task_upload import UpLoadBase
import smbprotocol.exceptions as SmbEx

from tools.log import Log
from tools.str import Str
from view.nas.nas_item import NasInfoItem

class SmbV3Client(UpLoadBase):
    AllLink = {}

    def __init__(self):
        UpLoadBase.__init__(self)
        pass

    def Init(self, nasInfo):
        assert isinstance(nasInfo, NasInfoItem)
        self.address = nasInfo.address
        self.port = nasInfo.port
        self.password = nasInfo.passwd
        self.username = nasInfo.user
        self.path = nasInfo.path

        datas = nasInfo.path.strip("/").split("/")

        self.service_name = datas[0]

        self.client = None
        self.isLink = False

    def Connect(self):
        try:
            if self.port:
                smbclient.listdir(rf"\\{self.address}\{self.service_name}", port=self.port, username=self.username,
                              password=self.password)
            else:
                smbclient.listdir(rf"\\{self.address}\{self.service_name}", username=self.username,
                                  password=self.password)
            self.isLink = True
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def TestConnect(self):
        try:
            if self.port:
                dirs = smbclient.listdir(rf"\\{self.address}\{self.service_name}", port=self.port, username=self.username,
                              password=self.password)
            else:
                dirs = smbclient.listdir(rf"\\{self.address}\{self.service_name}", username=self.username,
                                  password=self.password)
            self.isLink = True
        except Exception as es:
            Log.Error(es)
            return self.GetTestExceptionSt(es)
        return Str.Ok, ""

    def DisConnect(self):
        try:
            pass
        except Exception as es:
            Log.Error(es)
        return Str.Ok

    def IsHaveDir(self, remote_directory):
        lastPath = os.path.dirname(remote_directory)
        name = os.path.basename(remote_directory)
        dirs = []
        try:
            if self.port:
                dirs = smbclient.listdir(rf"\\{self.address}\{self.service_name}\{lastPath}", port=self.port, username=self.username,
                              password=self.password)
            else:
                dirs = smbclient.listdir(rf"\\{self.address}\{self.service_name}\{lastPath}",
                                         username=self.username,
                                         password=self.password)
        except SmbEx.SMBOSError as es:
            return False
        return name in dirs

    def Create(self, path):
        current_dir = ""
        dirs = path.split("/")
        for directory in dirs:
            if not directory:
                continue
            current_dir += directory
            if not self.IsHaveDir(current_dir):
                if self.port:
                    smbclient.mkdir(rf"\\{self.address}\{self.service_name}\{current_dir}", port=self.port,
                                         username=self.username,
                                         password=self.password)
                else:
                    smbclient.mkdir(rf"\\{self.address}\{self.service_name}\{current_dir}",
                                    username=self.username,
                                    password=self.password)
            current_dir  += "/"
        return Str.Ok

    def Upload(self, localPath, remotePath):
        try:
            if not self.isLink:
                self.Connect()

            remotePath  = remotePath.replace("/{}/".format(self.service_name), "")
            if not os.path.isfile(localPath):
                return Str.FileError
            self.Create(remotePath)
            fileName = os.path.basename(localPath)
            with open(localPath, "rb") as local_file:
                data = local_file.read()
                if self.port:
                    with smbclient.open_file(rf"\\{self.address}\{self.service_name}\{remotePath}"+ "/" + fileName,
                                    mode="wb+",
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as fd:
                        fd.write(data)
                else:
                    with smbclient.open_file(rf"\\{self.address}\{self.service_name}\{remotePath}" + "/" + fileName,
                                             mode="wb+",
                                             username=self.username,
                                             password=self.password) as fd:
                        fd.write(data)
            os.remove(localPath)
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def GetExceptionSt(self, es):
        if isinstance(es, SmbEx.SMBAuthenticationError):
            return Str.CvAuthError
        elif isinstance(es, SmbEx.LogonFailure):
            return Str.CvAuthError
        elif isinstance(es, SmbEx.BadNetworkName):
            return Str.ErrorPath
        return Str.Error

    def GetTestExceptionSt(self, es):
        if isinstance(es, SmbEx.SMBAuthenticationError):
            return Str.CvAuthError, ""
        elif isinstance(es, SmbEx.LogonFailure):
            return Str.CvAuthError, ""
        elif isinstance(es, SmbEx.BadNetworkName):
            return Str.ErrorPath, ""
        elif isinstance(es, SmbEx.SMBException):
            return Str.Error, str(es)
        return Str.Error, ""
