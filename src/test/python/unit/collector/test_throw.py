from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class ThrowCollectorTest(AsyncTestCase):

    async def test_throw(self):
        collector = throw()
        with self.assertRaises(Exception):
            await collector(None, None)
