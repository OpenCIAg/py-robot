import aiohttp
from robot.api import HttpEngine
from robot.http_engine.aiohttp_engine import AioHttpAdapter
from aiounittest import AsyncTestCase
from pytest_httpserver import HTTPServer

h1_hello = b"""
<html>
   <h1>Hello</h1>
</html>
"""


class AioHttpTest(AsyncTestCase):

    async def test_hello(self):
        with HTTPServer() as server:
            server.expect_request("/", method='GET').respond_with_data(
                response_data=h1_hello
            )
            url = server.url_for('/')
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                result = await response.content.read()
                self.assertEqual(h1_hello, result)


class AioHttpEngineTest(AsyncTestCase):

    async def test_redirect(self):
        http_engine: HttpEngine = AioHttpAdapter()
        with HTTPServer() as server:
            server.expect_request("/", method='GET').respond_with_data(
                status=302,
                headers={
                    'Location': '/hello'
                }
            )
            server.expect_request("/hello", method='GET').respond_with_data(
                response_data=h1_hello
            )
            url = server.url_for('/')
            async with http_engine.session() as session:
                headers, result = await session.get(url)
                self.assertEqual(h1_hello, result)
