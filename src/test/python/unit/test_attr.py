import asyncio
import re
from aiounittest import AsyncTestCase

from robot import CollectorFactory
from robot.core import xml_engine


class AttributeCollectorTest(AsyncTestCase):
    
    cf = None

    def setUp(self):
        self.cf = CollectorFactory()

    async def test_from_div(self):
        collector = self.cf.attr('div.title')
        html = xml_engine('<div class="title">title content</div><div class="summary">summary content</div>')
        expected = "title content"
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_xpath_from_div(self):
        collector = self.cf.attr(xpath='//div[@class="title"]')
        html = xml_engine('<div class="title">title content</div><div class="summary">summary content</div>')
        expected = "title content"
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_with_regex(self):
        collector = self.cf.attr('div', regex=re.compile(r'user:[\W]*.+', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = r"User:[\W]*username"
        result = await (collector(html, None))
        self.assertRegex(result, expected)

    async def test_with_regex_single(self):
        collector = self.cf.attr('div', regex=re.compile(r'user:[\W]*(.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = "username"
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_with_regex_multiple(self):
        collector = self.cf.attr('div', regex=re.compile(r'([a-z_-]+):[\W]*(.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = ("User", "username",)
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_with_regex_dict(self):
        collector = self.cf.attr('div', regex=re.compile(r'(?P<key>[a-z_-]+):[\W]*(?P<value>.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = dict(key="User", value="username")
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_with_regex_filter(self):
        collector = self.cf.attr('tr', regex_filter=re.compile(r'user:', re.IGNORECASE),
                                 regex=re.compile(r'user:[\W]*(.*)'))
        html = xml_engine('<table><tr><td>user:</td><td>username</td></tr><tr><td>age:</td><td>24</td></tr></table>')
        expected = 'username'
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_with_regex_filter_not_match(self):
        collector = self.cf.attr(
            'tr',
            regex_filter=re.compile(r'otherfield:', re.IGNORECASE),
            regex=re.compile(r'otherfield:[\W]*(.*)')
        )
        html = xml_engine('<table><tr><td>user:</td><td>username</td></tr><tr><td>age:</td><td>24</td></tr></table>')
        expected = None
        result = await (collector(html, None))
        self.assertEqual(expected, result)
