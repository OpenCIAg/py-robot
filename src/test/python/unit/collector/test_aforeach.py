from typing import Iterable, Iterator

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


class AsyncIterableAdapter(object):
    iterator: Iterator[X]

    def __init__(self, iterable: Iterable[X]):
        self.iterator = iter(iterable)

    async def __anext__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            raise StopAsyncIteration

    def __aiter__(self) -> 'self':
        return self


class AsyncForeachCollectorTest(AsyncTestCase):

    async def test_tr_with_css(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            xpath('//tr/td[position()=2]'),
            fn(AsyncIterableAdapter),
            aforeach(as_text()),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_tr_with_xpath(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td:nth-child(2)'),
            fn(AsyncIterableAdapter),
            aforeach(as_text()),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))

    async def test_auto_pipe(self):
        xml_engine = PyQueryAdapter()
        collector = pipe(
            css('tr td:nth-child(2)'),
            fn(AsyncIterableAdapter),
            aforeach(
                as_text(),
                fn(lambda it: it)
            ),
        )
        html = xml_engine(raw_html)
        expected = ['2', '4']
        _, result = await collector(None, html)
        self.assertEqual(expected, list(result))
