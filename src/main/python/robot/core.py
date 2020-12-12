import asyncio
from dataclasses import dataclass, field
from robot.api import Robot, Collector, XmlNode, Y, Context
from robot.context.core import ContextImpl
from typing import List
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from pyquery import PyQuery as pq

xml_engine = pq


class NoopCollector(object):
    async def __call__(self, item, robot):
        return item.text()


class ConstCollector(object):
    def __init__(self, const):
        self.const = const

    async def __call__(self, item, robot):
        return self.const


def noop(e):
    return e


def to_text(e):
    return e.text()


def href_or_text(e):
    return e.attr('href') or e.text()


class CompositeCollector(object):
    def __init__(self, *actions):
        self.actions = actions

    async def __call__(self, e, robot):
        result = e
        for action in self.actions:
            if not result:
                return result
            result = action(result)
        return result


class CollectorBuilder(object):
    def __init__(self):
        self.actions = []

    def regex(self, regex):

        def _regex(pre_result):
            match = regex.search(pre_result)
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

        self.actions.append(_regex)
        return self

    def regex_filter(self, regex):
        def _regex_filter(pre_result):
            for e in pre_result:
                e = xml_engine(e)
                if regex.search(e.text()):
                    return e
            return None

        self.actions.append(_regex_filter)
        return self

    def selector(self, selector=None):
        return self.css(selector)

    def css(self, selector=None):
        if not selector:
            self.actions.append(noop)
            return self

        def _selector(pre_result):
            return pre_result.find(selector) or None

        self.actions.append(_selector)
        return self

    def xpath(self, selector):
        if not selector:
            self.actions.append(noop)
            return self

        def _selector(pre_result):
            return xml_engine(pre_result.root.find(selector)) or None

        self.actions.append(_selector)
        return self

    def call(self, func):
        def _call(pre_result):
            return func(pre_result)

        self.actions.append(_call)
        return self

    def type(self, clazz):
        return self.call(clazz)

    def attr(self, attr=None):
        if not attr:
            self.actions.append(to_text)
            return self

        def _attr(pre_result):
            return pre_result.attr(attr)

        self.actions.append(_attr)
        return self

    def prefix(self, fragment):

        def _prefix(e):
            return fragment + e

        self.actions.append(_prefix)
        return self

    def suffix(self, fragment):

        def _suffix(e):
            return e + fragment

        self.actions.append(_suffix)
        return self

    def build(self):
        return CompositeCollector(*self.actions)


class ObjectCollector(object):
    def __init__(self, *args, **kwargs):
        self.nested_collectors = args
        self.collectors = kwargs

    async def __call__(self, item, robot) -> dict:
        obj = dict()
        for index, collector in enumerate(self.nested_collectors):
            result = await collector(item, robot)
            if not result:
                continue
            if isinstance(result, dict):
                obj.update(result)
            else:
                key = 'arg_%d' % index
                obj[key] = result
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
        if hasattr(selector, '__call__'):
            self.selector = selector
        else:
            self.selector = CollectorBuilder().css(selector).call(href_or_text).build()
        self.collector = collector

    async def __call__(self, item, robot) -> any:
        new_robot = robot.clone()
        url = await self.selector(item, robot)
        if not url:
            return None
        url = robot.prepare_url(url)
        new_robot.first_url = urlparse(url)
        try:
            html = await robot.fetch(url)
            document = xml_engine(html)
            return await self.collector(document, new_robot)
        except:
            return None


class CollectorFactory(object):
    collector_builder = CollectorBuilder
    array_class = ArrayCollector
    obj_class = ObjectCollector
    remote_class = RemoteCollector
    const_collector = ConstCollector

    def array(self, *args, **kwargs):
        return self.array_class(*args, **kwargs)

    def attr(self, selector=None, attr=None, **kwargs):
        params = dict(**locals(), **kwargs)
        keys = [
            'selector',
            'css',
            'xpath',
            'regex_filter',
            'attr',
            'regex',
            'prefix',
            'suffix',
            'type',
            'call'
        ]
        builder = self.collector_builder()
        for k in [k for k in keys if k in params]:
            getattr(builder, k)(params[k])
        return builder.build()

    def obj(self, *args, **kwargs):
        return self.obj_class(*args, **kwargs)

    def remote(self, *args, **kwargs):
        return self.remote_class(*args, **kwargs)

    def const(self, const):
        return self.const_collector(const)


@dataclass()
class RobotImpl(Robot):
    context: Context = field(default_factory=ContextImpl)

    async def run(self, collector: Collector[XmlNode, Y], url: str) -> Y:
        url = self.context.resolve_url(url)
        sub_context, xml_node = await self.context.http_get(url)
        return await collector(sub_context, xml_node)

    async def run_many(self, collector: Collector[XmlNode, Y], *urls: str) -> List[Y]:
        return await asyncio.gather(*[
            self.run(collector, url)
            for url in urls
        ])

    def sync_run(self, collector: Collector[XmlNode, Y], url: str) -> Y:
        return self.sync_run_many(collector, url)[0]

    def sync_run_many(self, collector: Collector[XmlNode, Y], *urls: List[str]) -> List[Y]:
        cpu_count = multiprocessing.cpu_count()
        thread_pool = ThreadPoolExecutor(cpu_count)

        with thread_pool:
            loop = asyncio.get_event_loop()
            loop.set_default_executor(thread_pool)
            result = loop.run_until_complete(self.run_many(collector, *urls))
            return result
