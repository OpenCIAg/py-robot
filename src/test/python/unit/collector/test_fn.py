from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class FnCollectorTest(AsyncTestCase):

    async def test_fn(self):
        any_value = 'any value'
        collector = fn(lambda _: any_value)
        _, result = await collector(None, None)
        self.assertEqual(result, any_value)
