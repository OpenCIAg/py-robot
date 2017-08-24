from urllib.parse import urlparse
import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from pyquery import PyQuery as pq

xml_engine = pq


class NoopCollector(object):
    async def __call__(self, item, robot):
        return item.text()


class AttrCollector(object):
    def __init__(self, selector=None,
                 attr=None,
                 post_process=None,
                 regex=None, regex_filter=None,
                 type=None):
        self.selector = selector
        self.type = type
        self.attr = attr
        self.regex = regex
        self.regex_filter = regex_filter
        if post_process:
            setattr(self, 'post_process', post_process)

    def _regex_process(self, pre_result):
        if not self.regex or not pre_result:
            return pre_result
        match = self.regex.search(pre_result)
        if not match:
            return None
        d = match.groupdict()
        if d:
            return d
        l = match.groups()
        if len(l) > 1:
            return l
        elif l:
            return l[0]
        return match.group(0)

    def _type_process(self, pre_result):
        if not self.type or not pre_result:
            return pre_result
        return self.type(pre_result)

    def _attr_process(self, pre_result):
        if not pre_result:
            return pre_result
        if not self.attr:
            return pre_result.text()
        return pre_result.attr(self.attr)

    def _regex_filter_process(self, pre_result):
        if not self.regex_filter or not pre_result:
            return pre_result
        for e in pre_result:
            e = xml_engine(e)
            if self.regex_filter.search(e.text()):
                return e
        return None

    def post_process(self, e):
        result = self._regex_filter_process(e)
        result = self._attr_process(result)
        result = self._regex_process(result)
        result = self._type_process(result)
        return result

    async def __call__(self, item, robot) -> any:
        if self.selector:
            el = item.find(self.selector)
        else:
            el = item
        return self.post_process(el)


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
        url = item.find(self.selector).attr('href') or item.find(self.selector).text()
        try:
            html = await robot.fetch(url)
            document = xml_engine(html.encode())
            return await self.collector(document, robot)
        except:
            return None


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
        self.first_url = None

    async def fetch(self, url: str):
        if url.startswith('/'):
            url = self.first_url.scheme + '://' + self.first_url.netloc + url
        async with self.session.get(url) as response:
            return await response.text()

    async def __call__(self, url):
        self.first_url = urlparse(url)
        self.session = self.client.ClientSession()
        html = await self.fetch(url)
        document = xml_engine(html.encode())
        try:
            result = await self.collector(document, self)
            return result
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
