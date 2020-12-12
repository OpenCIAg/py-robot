import aiohttp
from aiounittest import AsyncTestCase
from pytest_httpserver import HTTPServer


class AioHttpTest(AsyncTestCase):

    async def test_hello(self):
        content = """
        <html>
            <h1>Hello</h1>
        </html>
        """

        with HTTPServer() as server:
            server.expect_request("/", method='GET').respond_with_data(
                response_data=content
            )
            url = server.url_for('/')
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                result = await response.content.read()
                self.assertEqual(content, result.decode())

