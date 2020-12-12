from aiounittest import AsyncTestCase

from robot.collector.shortcut import *
from robot.xml_engine.pyquery_engine import PyQueryAdapter

raw_html = """
<html>
<ul>
    <li>
        <a href="//fuu">fuu</a>
    </li>
    <li>
        <a>unknown</a>
    </li>
</ul>
</html>
"""


class DefaultCollectorTest(AsyncTestCase):

    async def test_get_link_or_text(self):
        xml_engine = PyQueryAdapter()
        collector = array(
            css('ul > li > a'),
            default(
                attr('href'),
                text(),
            )
        )
        html = xml_engine(raw_html)
        expected = [['//fuu'], ['unknown']]
        result = await collector(None, html)
        self.assertEqual(expected, list(result))
