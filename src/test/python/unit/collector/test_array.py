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


class ArrayCollectorTest(AsyncTestCase):

    async def test_tr_with_css(self):
        xml_engine = PyQueryAdapter()
        collector = array(
            xpath('//tr/td[position()=2]'),
            as_text()
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_tr_with_xpath(self):
        xml_engine = PyQueryAdapter()
        collector = array(
            css('tr td:nth-child(2)'),
            as_text()
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        result = await collector(None, html)
        self.assertEqual(expected, list(result))
