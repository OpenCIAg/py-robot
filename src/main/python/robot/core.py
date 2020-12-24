import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import List

from robot.api import Robot, Collector, XmlNode, Y, Context
from robot.context.core import ContextImpl


@dataclass()
class RobotImpl(Robot):
    context: Context = field(default_factory=ContextImpl)

    _loop = None
    _thread_poll = None

    def __enter__(self):
        cpu_count = multiprocessing.cpu_count()
        thread_pool = ThreadPoolExecutor(cpu_count)
        self._loop = asyncio.get_event_loop()
        self._loop.set_default_executor(thread_pool)
        self._thread_poll = thread_pool.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._loop.run_until_complete(
            self.context.close()
        )
        self._thread_poll.__exit__(exc_type, exc_val, exc_tb)

    async def run(self, collector: Collector[None, Y]) -> Y:
        return await collector(self.context, None)

    def sync_run(self, collector: Collector[None, Y]) -> Y:
        return self._loop.run_until_complete(self.run(collector))
