from aiounittest import AsyncTestCase

from robot.collector.pagination import AsyncIterableAdapter


class TestAsyncIterableAdapter(AsyncTestCase):

    async def test_for(self):
        result = []
        iterable = AsyncIterableAdapter(range(10))
        async for i in iterable:
            result.append(i)
        self.assertEqual(result, list(range(10)))
