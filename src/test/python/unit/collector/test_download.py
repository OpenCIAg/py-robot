from tempfile import NamedTemporaryFile

from aiounittest import AsyncTestCase
from pytest_httpserver import HTTPServer

from robot.collector.shortcut import *
from robot.context.core import ContextImpl

h1_hello = b"""
<html>
   <h1>Hello</h1>
</html>
"""


class DownloadCollectorTest(AsyncTestCase):

    async def test_hello(self):
        file = NamedTemporaryFile()
        context = ContextImpl()
        collector = download(const(file.name))
        with HTTPServer() as server:
            server.expect_request("/", method='GET').respond_with_data(
                response_data=h1_hello
            )
            url = server.url_for('/')
            result = await collector(context, url)
        self.assertEqual(result, file.name)
        with open(file.name, 'rb') as input_stream:
            self.assertEqual(h1_hello, input_stream.read())
        file.close()
        await context.http_session.close()
