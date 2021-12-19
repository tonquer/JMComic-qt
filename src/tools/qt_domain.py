import random

from config import config
from config.setting import Setting
from server.server import Server
from server import req
from tools.log import Log
from tools.singleton import Singleton
from tools.status import Status


class QtDomainMgr(Singleton):
    def __init__(self):
        self.cache_dns = {}  # host: ip
        self.fail_dns = set()  # host
        self.wait_dns = set()  # host

        self.http_dns_task = {}  # host: [tasks]
        self.download_dns_task = {}  # host: [tasks]

    def AddHttpTask(self, *args, **kwargs):
        request = args[0]
        from tools.tool import ToolUtil
        host = ToolUtil.GetUrlHost(request.url)
        from task.task_http import TaskHttp
        if host in self.cache_dns:
            TaskHttp().AddHttpTask(*args, **kwargs)
        else:
            tasks = self.http_dns_task.setdefault(host, [])
            tasks.append((args, kwargs))
            if host not in self.wait_dns:
                self.wait_dns.add(host)
                TaskHttp().AddHttpTask(req=req.DnsOverHttpsReq(host), callBack=self.AddHttpTaskBack, backParam=host)
        return

    def AddHttpTaskBack(self, data, host):
        self.wait_dns.discard(host)
        if data["st"] == Status.Ok:
            addresss = []
            for info in data.get("Answer", []):
                addresss.append(info.get("data"))
            if len(addresss) <= 0:
                Log.Warn("Dns parse error, host:{}".format(host))
            else:
                address = random.choice(addresss)
                self.cache_dns[host] = address
                Server().UpdateDns(host, address)
                Log.Info("Dns parse suc, host:{}:{}, {}".format(host, address, addresss))
        else:
            self.fail_dns.add(host)

        for arg1, arg2 in self.http_dns_task.get(host, []):
            from task.task_http import TaskHttp
            TaskHttp().AddHttpTask(*arg1, **arg2)
        if host in self.http_dns_task:
            self.http_dns_task.pop(host)

    def AddDownloadTask(self, *args, **kwargs):
        url = kwargs.get("url")
        if not url:
            url = args[0]
        from tools.tool import ToolUtil
        host = ToolUtil.GetUrlHost(url)
        if host in self.cache_dns:
            from task.task_download import TaskDownload
            TaskDownload().DownloadTask(*args, **kwargs)
        else:
            tasks = self.download_dns_task.setdefault(host, [])
            tasks.append((args, kwargs))
            if host not in self.wait_dns:
                self.wait_dns.add(host)
                from task.task_http import TaskHttp
                TaskHttp().AddHttpTask(req=req.DnsOverHttpsReq(host), callBack=self.AddDownloadTaskBack, backParam=host)
        return

    def AddDownloadTaskBack(self, data, host):
        self.wait_dns.discard(host)
        if data["st"] == Status.Ok:
            addresss = []
            Answer = data.get("Answer")
            if Answer:
                for info in data.get("Answer"):
                    addresss.append(info.get("data"))
                if len(addresss) <= 0:
                    Log.Warn("Dns parse error, host:{}".format(host))
                else:
                    address = random.choice(addresss)
                    self.cache_dns[host] = address
                    Server().UpdateDns(host, address)
                    Log.Info("Dns parse suc, host:{}:{}, {}".format(host, address, addresss))
            else:
                self.fail_dns.add(host)
                Log.Warn("Dns parse not found, host:{}".format(host))
        else:
            self.fail_dns.add(host)

        for arg1, arg2 in self.download_dns_task.get(host, []):
            from task.task_download import TaskDownload
            TaskDownload().DownloadTask(*arg1, **arg2)
        if host in self.download_dns_task:
            self.download_dns_task.pop(host)

    def Init(self):
        for host in config.DomainDns:
            from task.task_http import TaskHttp
            TaskHttp().AddHttpTask(req=req.DnsOverHttpsReq(host), callBack=self.AddHttpTaskBack, backParam=host)
        return

    def Update(self):
        # self.cache_dns.clear()
        # self.fail_dns.clear()
        if Setting.IsOpenDoh.value:
            self.Init()
        else:
            Server().ClearDns()
        return
