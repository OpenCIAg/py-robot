import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from pyquery import PyQuery as pq

xml_engine = pq


class NoopCollector(object):
    async def __call__(self, item, robot):
        return item.text()


class AttrCollector(object):
    def __init__(self, selector, post_process=None, type=str):
        self.selector = selector
        self.type = type
        if post_process:
            setattr(self, post_process)

    def post_process(self, e):
        return self.type(e.text())

    async def __call__(self, item, robot) -> any:
        result = item.find(self.selector)
        return self.post_process(xml_engine(result))


class ObjectCollector(object):
    def __init__(self, *args, **kwargs):
        self.collectors = kwargs

    async def __call__(self, item, robot) -> dict:
        obj = dict()
        for attr_name, collector in self.collectors.items():
            obj[attr_name] = await collector(item, robot)
        return obj


class ArrayCollector(object):
    def __init__(self, selector, collector=None):
        self.selector = selector
        self.collector = collector
        if self.collector is None:
            self.collector = NoopCollector()

    async def __call__(self, item, robot) -> list:
        result = item.find(self.selector)
        return await asyncio.gather(*[self.collector(xml_engine(e), robot) for e in result])


class RemoteCollector(object):
    def __init__(self, selector, collector):
        self.selector = selector
        self.collector = collector

    async def __call__(self, item, robot) -> any:
        url = item.find(self.selector).text()
        html = await robot.fetch(url)
        document = xml_engine(html.encode())
        return await self.collector(document, robot)


class CollectorFactory(object):
    array_class = ArrayCollector
    attr_class = AttrCollector
    obj_class = ObjectCollector
    remote_class = RemoteCollector

    def array(self, *args, **kwargs):
        return self.array_class(*args, **kwargs)

    def attr(self, *args, **kwargs):
        return self.attr_class(*args, **kwargs)

    def obj(self, *args, **kwargs):
        return self.obj_class(*args, **kwargs)

    def remote(self, *args, **kwargs):
        return self.remote_class(*args, **kwargs)


class Robot(object):
    def __init__(self, client, collector, timeout=10):
        self.timeout = timeout
        self.client = client
        self.collector = collector
        self.session = None
        self.loop = None

    async def fetch(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    async def __call__(self, url):
        self.session = self.client.ClientSession()
        html = await self.fetch(url)
        document = xml_engine(html.encode())
        try:
            result = await self.collector(document, self)
            return result
        except Exception as ex:
            print(ex)
        finally:
            self.session.close()

    def run(self, url):
        cpu_count = multiprocessing.cpu_count()
        thread_pool = ThreadPoolExecutor(cpu_count)

        with thread_pool:
            self.loop = asyncio.get_event_loop()
            self.loop.set_default_executor(thread_pool)
            result = self.loop.run_until_complete(self(url))
            return result
