import asyncio
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import List, Any, Callable, Iterable, Dict, Tuple

from robot.api import Collector, Context, XmlNode, I, O

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class PipeCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            item = await collector(context, item)
        return item


@dataclass(init=False)
class DefaultCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Any:
        for collector in self.collectors:
            item = await collector(context, item)
            if item:
                return item
        return item


@dataclass()
class FnCollector(Collector[I, O]):
    fn: Callable[[Context, I], O]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: I) -> O:
        return self.fn(context, item)


@dataclass()
class AsyncCollector(Collector[I, O]):
    fn: Callable[[Context, I], O]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: I) -> O:
        return await self.fn(context, item)


@dataclass()
class NoopCollector(Collector[I, I]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: I) -> I:
        return item


NOOP_COLLECTOR = NoopCollector()


@dataclass()
class ConstCollector(Collector[Any, O]):
    value: O
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> O:
        return self.value


@dataclass()
class ArrayCollector(Collector[I, List[O]]):
    splitter: Collector[I, Iterable[Any]]
    item_collector: Collector[Any, O] = NOOP_COLLECTOR
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: I) -> Iterable[O]:
        sub_items = await self.splitter(context, item)
        collected_items = await asyncio.gather(*[self.item_collector(context, sub_item) for sub_item in sub_items])
        return collected_items


@dataclass()
class DictCollector(Collector[I, Dict[str, Any]]):
    nested_collectors: Tuple[Collector[I, Dict[str, Any]]] = ()
    field_collectors: Dict[str, Collector[I, Any]] = field(default_factory=dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: I) -> Dict[str, Any]:
        obj = dict()
        for collector in self.nested_collectors:
            result = await collector(context, item)
            obj.update(result)
        for attr_name, collector in self.field_collectors.items():
            obj[attr_name] = await collector(context, item)
        return obj


@dataclass()
class CssCollector(Collector[XmlNode, XmlNode]):
    css_selector: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> XmlNode:
        return item.find_by_css(self.css_selector)


@dataclass()
class AsTextCollector(Collector[XmlNode, str]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> str:
        return self.prefix + item.as_text() + self.suffix


@dataclass()
class TextCollector(Collector[XmlNode, Iterable[str]]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            self.prefix + value + self.suffix
            for value in item.text()
        ]


@dataclass()
class AttrCollector(Collector[XmlNode, Iterable[str]]):
    attr: str
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Iterable[str]:
        return [
            self.prefix + value + self.suffix
            for value in item.attr(self.attr)
        ]


@dataclass()
class AnyCollector(Collector[Iterable[I], I]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[I]) -> I:
        return next(iter(item))
