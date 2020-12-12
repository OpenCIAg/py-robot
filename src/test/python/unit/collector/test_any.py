from aiounittest import AsyncTestCase

from robot.collector.shortcut import *
from robot.xml_engine.pyquery_engine import PyQueryAdapter


class AnyCollectorTest(AsyncTestCase):

    async def test_from_table_to_attr(self):
        xml_engine = PyQueryAdapter()
        collector = any()
        html = xml_engine('<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')
        result = await collector(None, html)
        self.assertEqual(result, html)
