from unittest import TestCase
from robot.core import xml_engine
import asyncio
import re

from robot import CollectorFactory


class AttributeCollectorTest(TestCase):
    loop = asyncio.get_event_loop()
    cf = None

    def setUp(self):
        self.cf = CollectorFactory()

    def test_from_div(self):
        collector = self.cf.attr('div.title')
        html = xml_engine('<div class="title">title content</div><div class="summary">summary content</div>')
        expected = "title content"
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex(self):
        collector = self.cf.attr('div', regex=re.compile(r'user: *.+', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = "User: username"
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex_single(self):
        collector = self.cf.attr('div', regex=re.compile(r'user: *(.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = "username"
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex_multiple(self):
        collector = self.cf.attr('div', regex=re.compile(r'([a-z_-]+): *(.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = ("User", "username",)
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex_dict(self):
        collector = self.cf.attr('div', regex=re.compile(r'(?P<key>[a-z_-]+): *(?P<value>.+)', re.IGNORECASE))
        html = xml_engine('<html><div>User:<p>username</p></div></html>')
        expected = dict(key="User", value="username")
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex_filter(self):
        collector = self.cf.attr('tr', regex_filter=re.compile(r'user:', re.IGNORECASE),
                                 regex=re.compile(r'user: *(.*)'))
        html = xml_engine('<table><tr><td>user:</td><td>username</td></tr><tr><td>age:</td><td>24</td></tr></table>')
        expected = 'username'
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)

    def test_with_regex_filter_not_match(self):
        collector = self.cf.attr('tr', regex_filter=re.compile(r'otherfield:', re.IGNORECASE),
                                 regex=re.compile(r'otherfield: *(.*)'))
        html = xml_engine('<table><tr><td>user:</td><td>username</td></tr><tr><td>age:</td><td>24</td></tr></table>')
        expected = None
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)
