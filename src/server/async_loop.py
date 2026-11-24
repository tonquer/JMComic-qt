import asyncio
import sys
import threading

from tools.log import Log


def CreateDefaultEventLoop() -> asyncio.AbstractEventLoop:
    # curl_cffi 依赖 add_reader/add_writer，Windows 下优先使用 SelectorEventLoop
    if sys.platform == "win32":
        return asyncio.SelectorEventLoop()
    return asyncio.new_event_loop()


class AsyncLoopRunner:
    """Hosts a single background asyncio event loop thread with named queues and worker coroutines."""

    def __init__(self, threadName="AsyncIO-Server", loopFactory=None):
        self._threadName = threadName
        self._loopFactory = loopFactory or CreateDefaultEventLoop

        self._lock = threading.RLock()
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._queuesReady = False
        self._stopped = False

        self._queueSpecs = []
        self._onStartup = None
        self._onShutdown = None

        self._pendingItems = []
        self._queues = {}
        self._workerTasks = []
        self._stopEvent = None

    @property
    def loop(self):
        return self._loop

    @property
    def thread(self):
        return self._thread

    def Configure(self, queueSpecs, onStartup=None, onShutdown=None):
        """
        queueSpecs: list of (queueName, workerPrefix, workerCount, handlerCoro)
        handlerCoro: async def(item, workerIndex)
        """
        self._queueSpecs = list(queueSpecs)
        self._onStartup = onStartup
        self._onShutdown = onShutdown

    def Start(self):
        with self._lock:
            if self._thread is not None and self._thread.is_alive() and not self._stopped:
                return
            self._stopped = False
            self._queuesReady = False
            self._ready.clear()
            self._thread = threading.Thread(
                target=self._ThreadMain, name=self._threadName, daemon=True
            )
            self._thread.start()
        self._ready.wait(timeout=5)

    def Stop(self, timeout: float = 3.0):
        with self._lock:
            self._stopped = True
            self._pendingItems.clear()
            loop = self._loop
            thread = self._thread

        if loop is not None and not loop.is_closed() and loop.is_running():
            try:
                fut = asyncio.run_coroutine_threadsafe(self._Shutdown(), loop)
                fut.result(timeout=timeout)
            except Exception as es:
                Log.Warn(f"async server shutdown warning: {es}")

        if thread is not None and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=timeout)
        Log.Info("all thread end")

    def ResetStopped(self):
        with self._lock:
            self._stopped = False
            self._pendingItems.clear()

    def Enqueue(self, queueName: str, item):
        with self._lock:
            if self._stopped:
                return
            if self._loop is None or not self._queuesReady or self._loop.is_closed():
                self._pendingItems.append((queueName, item))
                return
            loop = self._loop
        try:
            loop.call_soon_threadsafe(self._PutNowait, queueName, item)
        except RuntimeError:
            pass

    def RunSync(self, coro):
        """Execute a coroutine synchronously on the running loop or a temporary loop."""
        with self._lock:
            loop = self._loop
            thread = self._thread

        if (
            loop is not None
            and not loop.is_closed()
            and loop.is_running()
            and threading.current_thread() is not thread
        ):
            return asyncio.run_coroutine_threadsafe(coro, loop).result()

        tempLoop = self._loopFactory()
        try:
            return tempLoop.run_until_complete(coro)
        finally:
            self._FinalizeLoop(tempLoop)

    def _PutNowait(self, queueName: str, item):
        if self._stopped:
            return
        queue = self._queues.get(queueName)
        if queue is not None:
            queue.put_nowait(item)

    def _ThreadMain(self):
        loop = self._loopFactory()
        asyncio.set_event_loop(loop)
        with self._lock:
            self._loop = loop
        try:
            loop.run_until_complete(self._MainLoop())
        except Exception as es:
            Log.Error(es)
        finally:
            self._FinalizeLoop(loop)
            with self._lock:
                self._loop = None
                self._queuesReady = False
                self._queues.clear()
                self._stopEvent = None
            self._ready.set()

    @staticmethod
    def _FinalizeLoop(loop: asyncio.AbstractEventLoop):
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
        except Exception as es:
            Log.Error(es)
        finally:
            loop.close()

    async def _MainLoop(self):
        self._stopEvent = asyncio.Event()
        self._queues = {name: asyncio.Queue() for name, _, _, _ in self._queueSpecs}

        if self._onStartup is not None:
            await self._onStartup()

        with self._lock:
            self._queuesReady = True
            pending = list(self._pendingItems)
            self._pendingItems.clear()

        for queueName, item in pending:
            self._PutNowait(queueName, item)

        self._workerTasks = []
        for queueName, prefix, count, handlerCoro in self._queueSpecs:
            queue = self._queues[queueName]
            for index in range(count):
                task = asyncio.create_task(
                    self._WorkerLoop(queue, index, handlerCoro),
                    name=f"{prefix}-{index}",
                )
                self._workerTasks.append(task)

        self._ready.set()
        await self._stopEvent.wait()

    async def _WorkerLoop(self, queue: asyncio.Queue, index: int, handlerCoro):
        while True:
            item = await queue.get()
            try:
                if item == "" or item is None:
                    break
                await handlerCoro(item, index)
            except asyncio.CancelledError:
                raise
            except Exception as es:
                Log.Error(es)
            finally:
                queue.task_done()

    async def _Shutdown(self):
        for queue in self._queues.values():
            while True:
                try:
                    queue.get_nowait()
                    queue.task_done()
                except asyncio.QueueEmpty:
                    break

        workers = list(self._workerTasks)
        self._workerTasks.clear()
        for worker in workers:
            worker.cancel()
        if workers:
            await asyncio.gather(*workers, return_exceptions=True)

        if self._onShutdown is not None:
            await self._onShutdown()

        if self._stopEvent is not None:
            self._stopEvent.set()
