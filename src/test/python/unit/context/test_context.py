from aiounittest import AsyncTestCase
from urllib.parse import urlparse
from robot.api import Context
from robot.context.core import ContextImpl


class ResolveUrlContextImplTest(AsyncTestCase):
    context: Context = None

    @classmethod
    def setUpClass(cls):
        cls.context = ContextImpl(url=urlparse('http://example.com/path1/page1?q=query#element-1'))

    async def test_resolve_absolute_url(self):
        absolute_url = 'https://http.cat/102'
        result = self.context.resolve_url(absolute_url)
        self.assertEqual(absolute_url, result)

    async def test_resolve_scheme(self):
        url = '//http.cat/102'
        result = self.context.resolve_url(url)
        self.assertEqual('http:' + url, result)

    async def test_absolute_path(self):
        url = '/path2/page2'
        result = self.context.resolve_url(url)
        self.assertEqual(
            'http://example.com/path2/page2',
            result
        )

    async def test_relative_path(self):
        url = 'page2'
        result = self.context.resolve_url(url)
        self.assertEqual(
            'http://example.com/path1/page2',
            result
        )
