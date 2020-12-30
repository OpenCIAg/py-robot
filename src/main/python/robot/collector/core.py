from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import List, Any, Callable, Iterable, Dict, Tuple, Awaitable, AsyncIterable, Sequence

from robot.api import Collector, Context, X, Y

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class PipeCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        for collector in self.collectors:
            context, item = await collector(context, item)
        return context, item


@dataclass(init=False)
class DefaultCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    def is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, (str,)):
            if value.strip() == '':
                return True
            return False
        if isinstance(value, Iterable):
            for item in value:
                if not self.is_empty(item):
                    return False
            return True
        return False

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        for collector in self.collectors:
            context, result = await collector(context, item)
            if not self.is_empty(result):
                return context, result
        return context, None


@dataclass()
class FnCollector(Collector[X, Y]):
    fn: Callable[[X], Y]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        return context, self.fn(item)


@dataclass()
class AsyncFnCollector(Collector[X, Y]):
    fn: Callable[[X], Awaitable[Y]]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        return context, await self.fn(item)


@dataclass()
class NoopCollector(Collector[X, X]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        return context, item


NOOP_COLLECTOR = NoopCollector()


@dataclass()
class ConstCollector(Collector[Any, Y]):
    value: Y
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Y]:
        return context, self.value


@dataclass()
class ForeachCollector(Collector[Sequence[X], Sequence[Y]]):
    collector: Collector[X, Y]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Sequence[X]) -> Tuple[Context, Sequence[Y]]:
        collected_items = await asyncio.gather(*[
            self.collector(context, i) for i in item
        ])
        return context, list(map(lambda it: it[1], collected_items))


@dataclass()
class AsyncForeachCollector(Collector[AsyncIterable[X], Sequence[Y]]):
    collector: Collector[X, Y]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: AsyncIterable[X]) -> Tuple[Context, Sequence[Y]]:
        tasks = []
        async for i in item:
            coro = self.collector(context, i)
            task = asyncio.create_task(coro)
            tasks.append(task)
        values = await asyncio.gather(*tasks)
        return context, list(map(lambda it: it[1], values))


@dataclass()
class ArrayCollector(Collector[X, List[Y]]):
    splitter: Collector[X, Iterable[Any]]
    item_collector: Collector[Any, Y] = NOOP_COLLECTOR
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Iterable[Y]]:
        context, sub_items = await self.splitter(context, item)
        collected_items = await asyncio.gather(*[
            self.item_collector(context, sub_item)
            for sub_item in sub_items
        ])
        return context, list(map(lambda it: it[1], collected_items))


@dataclass(init=False)
class TupleCollector(Collector[X, Tuple]):
    collectors: Tuple[Collector[X, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[X, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Tuple]:
        collected_items = await asyncio.gather(*[
            collector(context, item)
            for collector in self.collectors
        ])
        return context, tuple(map(lambda it: it[1], collected_items))


@dataclass()
class DelayCollector(Collector[X, X]):
    delay: float
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        await asyncio.sleep(self.delay)
        return context, item


@dataclass()
class DictCollector(Collector[X, Dict[str, Any]]):
    nested_collectors: Tuple[Collector[X, Dict[str, Any]]] = ()
    field_collectors: Dict[str, Collector[X, Any]] = field(default_factory=dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Dict[str, Any]]:
        obj = dict()
        collected_items = await asyncio.gather(*[
            collector(context, item)
            for collector in self.nested_collectors
        ])
        for _, collected_item in collected_items:
            obj.update(collected_item)
        if not self.field_collectors:
            return context, obj
        keys, collectors = zip(*self.field_collectors.items())
        values = await asyncio.gather(*[
            collector(context, item)
            for collector in collectors
        ])
        values = map(lambda it: it[1], values)
        obj.update(dict(zip(keys, values)))
        return context, obj


@dataclass()
class ContextCollector(Collector[Any, Dict[str, Any]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Dict[str, Any]]:
        return context, dict(context)


CONTEXT = ContextCollector()


@dataclass()
class TapCollector(Collector[X, X]):
    fn: Collector[X, Any]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        await self.fn(context, item)
        return context, item
