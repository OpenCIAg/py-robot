from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class AsyncTapCollectorTest(AsyncTestCase):
    _call = None

    def async_mock_method(self):
        async def method(*args, **kwargs):
            self._call = (args, kwargs,)
            return None

        return method

    async def test_atap(self):
        value = 'any value'
        method = self.async_mock_method()
        collector = atap(method)
        result = await collector(None, value)
        self.assertIs(result, value)
        self.assertEqual(self._call, ((value,), {},))
