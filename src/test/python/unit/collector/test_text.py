from aiounittest import AsyncTestCase

from robot.collector.shortcut import *
from robot.xml_engine.pyquery_engine import PyQueryAdapter

raw_html = b"""
<html>
<ul>
    <li>
        <a href="//fuu1">Fuu 1</a>
    </li>
    <li>
        <a href="//fuu2">Fuu 2</a>
    </li>
</ul>
</html>
"""


class TextCollectorTest(AsyncTestCase):

    async def test_get_link_text(self):
        xml_engine = PyQueryAdapter()
        collector = array(
            css('ul > li > a'),
            text(),
        )
        html = xml_engine(raw_html)
        expected = [['Fuu 1'], ['Fuu 2']]
        result = await collector(None, html)
        self.assertEqual(expected, list(result))
