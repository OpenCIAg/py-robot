from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class DictCollectorTest(AsyncTestCase):

    async def test_const_in_field_collectors(self):
        expected = {
            'a': 1,
            'b': '2'
        }
        collector = dict(
            a=const(1),
            b=const('2')
        )
        _, result = await collector(None, None)
        self.assertEqual(result, expected)

    async def test_const_in_nested_collectors(self):
        expected = {
            'a': 1,
            'b': '2'
        }
        collector = dict(
            const({'a': 1}),
            const({'b': '2'}),
        )
        _, result = await collector(None, None)
        self.assertEqual(result, expected)

    async def test_const_mixed(self):
        expected = {
            'a': 1,
            'b': '2'
        }
        collector = dict(
            const({'a': 1}),
            b=const('2'),
        )
        _, result = await collector(None, None)
        self.assertEqual(result, expected)
