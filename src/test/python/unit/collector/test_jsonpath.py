from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class JsonPathCollectorTest(AsyncTestCase):

    async def test_context(self):
        any_value = {'key': 'value'}
        collector = jsonpath('$.key')
        result = await collector(None, any_value)
        self.assertEqual(result, ['value'])
