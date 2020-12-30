from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class ConstCollectorTest(AsyncTestCase):

    async def test_const(self):
        any_value = 'any value'
        collector = const(any_value)
        _, result = await collector(None, None)
        self.assertEqual(result, any_value)
