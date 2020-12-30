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
class UrlCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> Tuple[Context, str]:
        return context, context.resolve_url(item)
