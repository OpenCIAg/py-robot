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


class ForeachCollectorTest(AsyncTestCase):

    async def test_tr_with_css(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            xpath('//tr/td[position()=2]'),
            foreach(as_text()),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_tr_with_xpath(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td:nth-child(2)'),
            foreach(as_text()),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_auto_pipe(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td:nth-child(2)'),
            foreach(
                as_text(),
                fn(lambda it: str(it))
            ),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_limit(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td'),
            foreach(
                as_text(),
                limit=1,
            ),
        )
        html = xml_engine(raw_html)
        expected = ['1', '2', '3', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))
