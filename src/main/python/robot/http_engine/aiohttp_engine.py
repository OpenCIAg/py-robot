import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import TypeVar, Tuple, Any

import aiohttp

from robot.api import HttpSession, HttpEngine

__logger__: Logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass()
class AioHttpSessionAdapter(HttpSession):
    client_session: aiohttp.ClientSession
    logger: Logger = field(default=__logger__)

    async def download(self, url: str, filename: str):
        self.logger.debug(f'starting download {url} to {filename}')
        async with self.client_session.get(url, allow_redirects=True) as response:
            if response.status != 200:
                self.logger.warning(f'download {url} fail with status {response.status}')
                raise Exception()
            with open(filename, 'wb') as output:
                output.write(await response.read())

    async def get(self, url) -> Tuple[Any, str]:
        self.logger.debug(f'starting http get {url}')
        async with self.client_session.get(url, allow_redirects=True) as response:
            self.logger.info(f'http get {url} status {response.status}')
            content = await response.content.read()
            return response.headers, content

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def close(self):
        return await self.client_session.close()


class AioHttpAdapter(HttpEngine):
    def __init__(self, aiohttp=aiohttp):
        self.aiohttp = aiohttp

    def session(self) -> HttpSession:
        return AioHttpSessionAdapter(self.aiohttp.ClientSession())
