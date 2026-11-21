import logging
import os
import queue
import time

from config import config
from config.setting import Setting
from logging.handlers import QueueHandler, QueueListener
import atexit


class Log(object):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = None
    fh = None
    listener = None
    qh = None
    _atexit_registered = False

    @staticmethod
    def UpdateLoggingLevel():
        if not Log.ch or not Log.fh:
            return
        if Setting.LogIndex.value == 0:
            Log.ch.setLevel(logging.WARN)
            Log.fh.setLevel(logging.WARN)
            # Log.logger.setLevel(logging.WARN)
        elif Setting.LogIndex.value == 1:
            Log.ch.setLevel(logging.INFO)
            Log.fh.setLevel(logging.INFO)
            # Log.logger.setLevel(logging.INFO)
        elif Setting.LogIndex.value == 2:
            Log.ch.setLevel(logging.DEBUG)
            Log.fh.setLevel(logging.DEBUG)
            # Log.logger.setLevel(logging.DEBUG)
        return

    @staticmethod
    def Init():
        # 1. 先断开旧 QueueHandler，不再往旧队列塞日志
        if Log.qh and Log.logger:
            Log.logger.removeHandler(Log.qh)
            Log.qh = None
        # 2. 停掉旧后台监听线程（会自动把旧队列剩余日志刷完再退出）
        if Log.listener:
            Log.listener.stop()
            Log.listener = None
        # 3. 线程停稳后再安全关闭旧日志文件句柄
        if Log.fh:
            Log.fh.close()
            Log.fh = None
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        Log.ch = ch
        logPath = Setting.GetLogPath()
        os.makedirs(logPath, exist_ok=True)
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        logfile = os.path.join(logPath, day + ".log")
        fh = logging.FileHandler(logfile, mode='a', encoding="utf-8")
        Log.fh = fh
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        log_queue = queue.Queue()
        handlers = (ch, fh) if os.environ.get("PYCHARM_HOSTED") == "1" else (fh,)
        listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
        listener.start()
        Log.listener = listener
        # 4. 用 _atexit_registered 保证整个进程生命周期只注册一次退出钩子
        if not Log._atexit_registered:
            atexit.register(lambda: Log.listener and Log.listener.stop())
            Log._atexit_registered = True
        logger = logging.getLogger("fast_logger")
        logger.setLevel(logging.DEBUG)  # 放行 DEBUG，由 ch/fh 各自按 LogIndex 过滤
        logger.propagate = False
        qh = QueueHandler(log_queue)
        logger.addHandler(qh)
        Log.qh = qh
        Log.logger = logger
        Log.Debug = Log.logger.debug
        Log.Info = Log.logger.info
        Log.Warn = Log.logger.warning
        Log.Error = Log.logger.exception
        Log.UpdateLoggingLevel()
        return

    @staticmethod
    def Debug(es):
        Log.logger.debug(es)

    @staticmethod
    def Info(es):
        Log.logger.info(es, exc_info=True)

    @staticmethod
    def Warn(es):
        Log.logger.warning(es, exc_info=True)

    @staticmethod
    def Error(es):
        Log.logger.error(es, exc_info=True)

    @staticmethod
    def InstallFilter(stream2):
        class Stream2Handler(logging.StreamHandler):
            def __init__(self, stream=None):
                logging.StreamHandler.__init__(self, stream)

            def emit(self, record):
                """
                Emit a record.

                If a formatter is specified, it is used to format the record.
                The record is then written to the stream with a trailing newline.  If
                exception information is present, it is formatted using
                traceback.print_exception and appended to the stream.  If the stream
                has an 'encoding' attribute, it is used to determine how to do the
                output to the stream.
                """
                try:
                    msg = self.format(record)
                    stream = self.stream
                    # issue 35046: merged two stream.writes into one.
                    stream.write(record.levelno, msg + self.terminator)
                    self.flush()
                except RecursionError:  # See issue 36272
                    raise
                except Exception:
                    self.handleError(record)

        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", datefmt=logging.Formatter.default_time_format)
        ch = Stream2Handler(stream2)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        Log.logger.addHandler(ch)
