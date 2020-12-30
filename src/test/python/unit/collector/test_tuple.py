from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class TupleCollectorTest(AsyncTestCase):

    async def test_const_in_tuple_collector(self):
        expected = (1, '2',)
        collector = tuple(
            const(1),
            const('2')
        )
        _, result = await collector(None, None)
        self.assertEqual(result, expected)
