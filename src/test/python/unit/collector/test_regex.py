from aiounittest import AsyncTestCase
import re

from robot.collector.shortcut import *


class RegexCollectorTest(AsyncTestCase):

    async def test_with_compiled(self):
        collector = regex(re.compile(r'[a-z]+'))
        result = await collector(None, 'abc123')
        self.assertEqual(result, 'abc')

    async def test_with_raw(self):
        collector = regex(r'[a-z]+')
        result = await collector(None, 'abc123')
        self.assertEqual(result, 'abc')

    async def test_no_match(self):
        collector = regex(r'[a-z]+')
        result = await collector(None, '123')
        self.assertEqual(result, None)

    async def test_named_group(self):
        collector = regex(r'(?P<main>[a-z]+)')
        result = await collector(None, 'abc123')
        self.assertEqual(result, {'main': 'abc'})

    async def test_unnamed_group(self):
        collector = regex(r'([a-z]+)')
        result = await collector(None, 'abc123')
        self.assertEqual(result, 'abc')

    async def test_multiple_unnamed_group(self):
        collector = regex(r'([a-z]+)([0-9]+)')
        result = await collector(None, 'abc123')
        self.assertEqual(result, ('abc', '123',))
