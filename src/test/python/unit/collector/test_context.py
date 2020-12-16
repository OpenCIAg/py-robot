from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class ContextCollectorTest(AsyncTestCase):

    async def test_context(self):
        any_value = {'key': 'value'}
        collector = context()
        result = await collector(any_value, None)
        self.assertEqual(result, any_value)
        self.assertIsNot(result, any_value)
