from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class NoopCollectorTest(AsyncTestCase):

    async def test_noop(self):
        any_value = 'any value'
        collector = noop()
        _, result = await collector(None, any_value)
        self.assertEqual(result, any_value)
