from aiounittest import AsyncTestCase

from unittest.mock import MagicMock
from robot.collector.shortcut import *


class TapCollectorTest(AsyncTestCase):

    async def test_tap(self):
        value = 'any value'
        method = MagicMock()
        collector = tap(method)
        result = await collector(None, value)
        self.assertIs(result, value)
        method.assert_called_with(value)
