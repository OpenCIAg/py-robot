from aiounittest import AsyncTestCase
from robot.api import HttpEngine


class HttpEngineTest(AsyncTestCase):

    def test_session(self):
        self.assertTrue(hasattr(HttpEngine, 'session'))
        self.assertTrue(callable(HttpEngine.session))
        with self.assertRaises(NotImplementedError):
            HttpEngine.session(None)
