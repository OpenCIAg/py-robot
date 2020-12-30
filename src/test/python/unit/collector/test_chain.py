from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class ChainCollectorTest(AsyncTestCase):

    async def test_chain(self):
        item = [
            [0, 1, 2, 3],
            [4, 5],
            (6, 7,),
            [8],
            (9,),
        ]
        expected = range(10)
        collector = chain()
        result = await collector(None, item)
        self.assertEqual(list(result), list(expected))
