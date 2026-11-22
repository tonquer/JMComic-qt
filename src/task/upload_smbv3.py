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

    @staticmethod
    def _SplitParts(path):
        if not path:
            return []
        return [part for part in path.replace("\\", "/").split("/") if part]

    def _BuildUncPath(self, *parts):
        normalized = []
        for part in parts:
            normalized.extend(self._SplitParts(part))
        base = rf"\\{self.address}\{self.service_name}"
        if normalized:
            return base + "\\" + "\\".join(normalized)
        return base

    def Init(self, nasInfo):
        assert isinstance(nasInfo, NasInfoItem)
        self.address = nasInfo.address
        self.port = nasInfo.port
        self.password = nasInfo.passwd
        self.username = nasInfo.user
        self.path = nasInfo.path

        datas = self._SplitParts(nasInfo.path)

        self.service_name = datas[0] if datas else ""

        self.client = None
        self.isLink = False

    def Connect(self):
        try:
            uncRoot = self._BuildUncPath()
            if self.port:
                smbclient.listdir(uncRoot, port=self.port, username=self.username,
                              password=self.password, connection_timeout=5)
            else:
                smbclient.listdir(uncRoot, username=self.username,
                                  password=self.password, connection_timeout=5)
            self.isLink = True
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        return Str.Ok

    def TestConnect(self):
        try:
            uncRoot = self._BuildUncPath()
            if self.port:
                dirs = smbclient.listdir(uncRoot, port=self.port, username=self.username,
                              password=self.password, connection_timeout=5)
            else:
                dirs = smbclient.listdir(uncRoot, username=self.username,
                                  password=self.password, connection_timeout=5)
            self.isLink = True
            return Str.Ok, ""
        except Exception as es:
            Log.Error(es)
            return self.GetTestExceptionSt(es)
        finally:
            self.DisConnect()

    def DisConnect(self):
        try:
            self.isLink = False
            if hasattr(smbclient, "reset_connection_cache"):
                smbclient.reset_connection_cache()
        except Exception as es:
            Log.Error(es)
        return Str.Ok

    def IsHaveDir(self, remote_directory):
        parts = self._SplitParts(remote_directory)
        if not parts:
            return True
        parentPath = self._BuildUncPath(*parts[:-1])
        name = parts[-1]
        dirs = []
        try:
            if self.port:
                dirs = smbclient.listdir(parentPath, port=self.port, username=self.username,
                              password=self.password, connection_timeout=5)
            else:
                dirs = smbclient.listdir(parentPath,
                                         username=self.username,
                                         password=self.password, connection_timeout=5)
        except SmbEx.SMBOSError as es:
            return False
        return name in dirs

    def Create(self, path):
        dirs = self._SplitParts(path)
        currentParts = []
        for directory in dirs:
            currentParts.append(directory)
            current_dir = "\\".join(currentParts)
            if not self.IsHaveDir(current_dir):
                uncPath = self._BuildUncPath(*currentParts)
                if self.port:
                    smbclient.mkdir(uncPath, port=self.port,
                                         username=self.username,
                                         password=self.password, connection_timeout=5)
                else:
                    smbclient.mkdir(uncPath,
                                    username=self.username,
                                    password=self.password, connection_timeout=5)
        return Str.Ok

    def Upload(self, localPath, remotePath):
        try:
            if not self.isLink:
                st = self.Connect()
                if st != Str.Ok:
                    return st

            parts = self._SplitParts(remotePath)
            if parts and parts[0] == self.service_name:
                parts = parts[1:]
            normRemotePath = "\\".join(parts)
            if not os.path.isfile(localPath):
                return Str.FileError
            self.Create(normRemotePath)
            fileName = os.path.basename(localPath)
            remoteFile = self._BuildUncPath(*parts, fileName)
            with open(localPath, "rb") as local_file:
                data = local_file.read()
                if self.port:
                    with smbclient.open_file(remoteFile,
                                    mode="wb+",
                                    port=self.port,
                                    username=self.username,
                                    password=self.password, connection_timeout=5) as fd:
                        fd.write(data)
                else:
                    with smbclient.open_file(remoteFile,
                                             mode="wb+",
                                             username=self.username,
                                             password=self.password, connection_timeout=5) as fd:
                        fd.write(data)
            os.remove(localPath)
            return Str.Ok
        except Exception as es:
            Log.Error(es)
            return self.GetExceptionSt(es)
        finally:
            self.DisConnect()


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
