from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, AsyncIterable

from robot.api import Collector, Context, XmlNode, Tuple, X, Y
from robot.collector.core import PipeCollector, ConstCollector

__logger__ = logging.getLogger(__name__)


@dataclass()
class GetCollector(Collector[str, XmlNode]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> Tuple[Context, XmlNode]:
        sub_context, sub_item = await context.http_get(item)
        return sub_context, sub_item


@dataclass()
class GetManyCollector(Collector[Any, Any]):
    urls: Collector[Any, AsyncIterable[str]]
    collector: Collector[Any, Any]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        tasks = []
        _, urls = await self.urls(context, item)
        async for url in urls:
            collector = PipeCollector(ConstCollector(url), UrlCollector(), GetCollector(), self.collector)
            coro = collector(context, item)
            task = asyncio.create_task(coro)
            tasks.append(task)
        values = await asyncio.gather(*tasks)
        return context, list(map(lambda it: it[1], values))


@dataclass()
class UrlCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> Tuple[Context, str]:
        return context, context.resolve_url(item)
