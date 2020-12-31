from aiounittest import AsyncTestCase
from typing import Sequence
from robot.api import HttpEngine, HttpSession, XmlNode, XmlEngine, Context, Collector, Robot


class ApiTestCase(AsyncTestCase):

    def check_abstract_method(self, cls, method_name, parameters: Sequence[str] = ()):
        try:
            self.assertTrue(hasattr(cls, method_name))
            self.assertTrue(callable(getattr(cls, method_name)))
            with self.assertRaises(NotImplementedError):
                getattr(cls, method_name)(None, **dict((p, None,) for p in parameters))
        except AssertionError as error:
            raise AssertionError(
                f'{cls.__name__}.{method_name} not looks like an abstract method',
                error
            )

    async def check_async_abstract_method(self, cls, method_name, parameters: Sequence[str] = ()):
        try:
            self.assertTrue(hasattr(cls, method_name))
            self.assertTrue(callable(getattr(cls, method_name)))
            with self.assertRaises(NotImplementedError):
                await getattr(cls, method_name)(None, **dict((p, None,) for p in parameters))
        except AssertionError as error:
            raise AssertionError(
                f'{cls.__name__}.{method_name} not looks like an abstract method',
                error
            )


class HttpEngineTest(ApiTestCase):

    def test_api(self):
        self.check_abstract_method(HttpEngine, 'session')


class HttpSessionTest(ApiTestCase):

    async def test_api(self):
        await self.check_async_abstract_method(
            HttpSession, 'download', ('url', 'filename',)
        )
        await self.check_async_abstract_method(
            HttpSession, 'get', ('url',)
        )
        await self.check_async_abstract_method(
            HttpSession, '__aenter__',
        )
        await self.check_async_abstract_method(
            HttpSession, '__aexit__', ('exc_type', 'exc_val', 'exc_tb',)
        )
        await self.check_async_abstract_method(
            HttpSession, 'close',
        )


class XmlNodeTest(ApiTestCase):

    def test_api(self):
        self.check_abstract_method(
            XmlNode, '__iter__'
        )
        self.check_abstract_method(
            XmlNode, 'find_by_css', ('css',)
        )
        self.check_abstract_method(
            XmlNode, 'find_by_xpath', ('xpath',)
        )
        self.check_abstract_method(
            XmlNode, 'as_text',
        )
        self.check_abstract_method(
            XmlNode, 'text',
        )
        self.check_abstract_method(
            XmlNode, 'attr', ('attr',)
        )


class XmlEngineTest(ApiTestCase):

    def test_api(self):
        self.check_abstract_method(
            XmlEngine, '__call__', ('raw_xml',)
        )


class ContextTest(ApiTestCase):

    async def test_api(self):
        await self.check_async_abstract_method(
            Context, 'close'
        )
        self.check_abstract_method(
            Context, 'resolve_url', ('url',)
        )
        await self.check_async_abstract_method(
            Context, 'download', ('url', 'filename',)
        )
        await self.check_async_abstract_method(
            Context, 'http_get', ('url',)
        )
        self.check_abstract_method(
            Context, '__iter__',
        )


class CollectorTest(ApiTestCase):
    async def test_api(self):
        await self.check_async_abstract_method(
            Collector, '__call__', ('context', 'item',)
        )


class RobotTest(ApiTestCase):
    async def test_api(self):
        self.check_abstract_method(
            Robot, 'sync_run', ('collector',)
        )
        await self.check_async_abstract_method(
            Robot, 'run', ('collector',)
        )
        self.check_abstract_method(
            Robot, '__enter__',
        )
        self.check_abstract_method(
            Robot, '__exit__', ('exc_type', 'exc_val', 'exc_tb',)
        )
