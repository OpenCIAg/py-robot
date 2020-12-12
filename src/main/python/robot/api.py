from __future__ import annotations

from typing import List, Callable, Iterable, Iterator
from typing import TypeVar, Generic

I = TypeVar('I')
O = TypeVar('O')


class HttpEngine():
    pass


class XmlNode(Iterable['XmlNode']):

    def __iter__(self) -> Iterator[XmlNode]:
        raise NotImplementedError()

    def find_by_css(self, css: str) -> XmlNode:
        raise NotImplementedError()

    def find_by_xpath(self, xpath: str) -> XmlNode:
        raise NotImplementedError()

    def cast(self, cast_fn: Callable[[XmlNode], O]) -> O:
        raise NotImplementedError()

    def cast_all(self, cast_fn: Callable[[XmlNode], O]) -> Iterable[O]:
        raise NotImplementedError()

    def as_text(self) -> Iterable[str]:
        raise NotImplementedError()

    def attr(self, attr) -> Iterable[str]:
        raise NotImplementedError()


class XmlEngine():

    def __call__(self, raw_xml: str) -> XmlNode:
        raise NotImplementedError()


class Context():
    xml_engine: XmlEngine
    http_engine: HttpEngine


class Collector(Generic[I, O]):

    async def __call__(self, context: Context, item: I) -> O:
        raise NotImplementedError()


class Robot():

    async def run(self, collector: Collector[XmlNode, O], url: str) -> O:
        raise NotImplementedError()

    async def run_many(self, collector: Collector[XmlNode, O], *url: List[str]) -> List[O]:
        raise NotImplementedError()

    def sync_run(self, collector: Collector[XmlNode, O], url: str) -> O:
        raise NotImplementedError()

    def sync_run_many(self, collector: Collector[XmlNode, O], *url: List[str]) -> List[O]:
        raise NotImplementedError()
