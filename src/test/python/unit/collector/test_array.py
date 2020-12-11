from aiounittest import AsyncTestCase
import asyncio
import os

from robot.xml_engine.pyquery_engine import PyQueryAdapter
from robot import CollectorFactory
from robot.collector.shortcut import *


class ArrayCollectorTest(AsyncTestCase):

    async def test_from_table_to_attr(self):
        xml_engine = PyQueryAdapter()
        collector = array(
            css('tr'),
            pipe(
                css('td:nth-child(2)'),
                text(),
                any()
            )
        )
        html = xml_engine('<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')
        expected = ['2', '4']
        result = await collector(None, html)
        self.assertEqual(expected, list(result))
