from aiounittest import AsyncTestCase

from robot.collector.shortcut import *
from robot.xml_engine.pyquery_engine import PyQueryAdapter

raw_html = b"""
<html>
    <table>
        <tr>
            <td>1</td>
            <td>2</td>
        </tr>
        <tr>
            <td>3</td>
            <td>4</td>
        </tr>
    </table>
</htm>
"""


class FilterCollectorTest(AsyncTestCase):

    async def test_filter(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td:nth-child(2)'),
            text(),
            filter(lambda it: int(it) > 2),
        )
        html = xml_engine(raw_html)
        expected = ['4']
        result = await collector(None, html)
        self.assertEqual(expected, list(result))
