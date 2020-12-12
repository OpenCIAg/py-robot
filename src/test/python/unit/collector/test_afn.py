from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class AsyncFnCollectorTest(AsyncTestCase):

    async def test_afn(self):
        any_value = 'any value'

        async def async_fn(_):
            return any_value

        collector = afn(async_fn)
        result = await collector(None, None)
        self.assertEqual(result, any_value)
