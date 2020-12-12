from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class DelayCollectorTest(AsyncTestCase):

    async def test_delay(self):
        any_value = 'any value'
        collector = delay(0.01)
        result = await collector(None, any_value)
        self.assertEqual(result, any_value)
