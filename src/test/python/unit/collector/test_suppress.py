from aiounittest import AsyncTestCase

from robot.collector.shortcut import *


class SuppressCollectorTest(AsyncTestCase):

    async def test_default_should_suppress_with_none(self):
        collector = suppress(
            throw(),
        )
        _, result = await collector(None, None)
        self.assertIsNone(result)

    async def test_should_not_suppress_outside_throw(self):
        collector = pipe(
            throw(),
            suppress(const(1), handler=const(None)),
        )
        with self.assertRaises(Exception):
            await collector(None, None)

    async def test_should_suppress_inside_throw(self):
        any_value = {}
        collector = suppress(
            throw(),
            handler=const(any_value)
        )
        _, result = await collector(None, None)
        self.assertIs(result, any_value)

    async def test_should_not_suppress_different_exception(self):
        class CustomException(Exception):
            pass

        any_value = {}
        collector = suppress(
            throw(),
            handler=const(any_value),
            error_type=CustomException
        )
        with self.assertRaises(Exception):
            await collector(None, None)

    async def test_should_suppress_custom_exception(self):
        class CustomException(Exception):
            pass

        any_value = {}
        collector = suppress(
            throw(CustomException),
            handler=const(any_value),
        )
        _, result = await collector(None, None)
        self.assertIs(result, any_value)
