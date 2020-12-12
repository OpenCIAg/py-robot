import aiohttp
from robot.api import HttpSession, HttpEngine


class AioHttpSessionAdapter(HttpSession):
    client_session: aiohttp.ClientSession

    def __init__(self, client_session: aiohttp.ClientSession):
        self.client_session = client_session

    async def get(self, url):
        async with self.client_session.get(url, allow_redirects=True) as response:
            return await response.content.read()


class AioHttpAdapter(HttpEngine):
    def __init__(self, aiohttp=aiohttp):
        self.aiohttp = aiohttp

    def session(self) -> HttpSession:
        return AioHttpSessionAdapter(
            self.aiohttp.ClientSession()
        )
