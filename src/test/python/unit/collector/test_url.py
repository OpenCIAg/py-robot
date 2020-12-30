from aiounittest import AsyncTestCase

from robot.collector.shortcut import *
from unittest.mock import Mock, MagicMock


class UrlCollectorTest(AsyncTestCase):

    async def test_url(self):
        any_value = 'any value'
        expected = '/any/value'
        context = Mock()
        context.resolve_url = MagicMock(return_value=expected)
        collector = url()
        result = await collector(context, any_value)
        self.assertEqual(result, expected)
        context.resolve_url.assert_called_with(any_value)
