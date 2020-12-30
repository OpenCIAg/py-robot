from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class FlatCollectorTest(AsyncTestCase):

    async def test_flat(self):
        item = [
            [0, 1, 2, 3],
            [4, 5],
            (6, 7,),
            [8],
            (9,),
        ]
        expected = list(range(10))
        collector = flat()
        _, result = await collector(None, item)
        self.assertEqual(result, expected)
