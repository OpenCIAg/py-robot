from aiounittest import AsyncTestCase
from robot.core import xml_engine
import asyncio
import os

from robot import CollectorFactory


class ArrayCollectorTest(AsyncTestCase):
    
    cf = None

    def setUp(self):
        self.cf = CollectorFactory()

    async def test_from_table_to_attr(self):
        collector = self.cf.array(
            'tr', self.cf.attr('td:nth-child(2)')
        )
        html = xml_engine('<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')
        expected = ['2', '4']
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_from_table_to_obj(self):
        collector = self.cf.array(
            'tr', self.cf.obj(
                col1=self.cf.attr('td:nth-child(1)'),
                col2=self.cf.attr('td:nth-child(2)'),
            )
        )
        html = xml_engine('<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')
        expected = [dict(col1='1', col2='2'), dict(col1='3', col2='4')]
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_from_table_to_array(self):
        collector = self.cf.array(
            'li'
        )
        html = xml_engine('<ul><li>a</li><li>b</li><li>c</li><li>d</li></ul>')
        expected = ['a', 'b', 'c', 'd']
        result = await (collector(html, None))
        self.assertEqual(expected, result)

    async def test_from_table_to_array_with_type(self):
        collector = self.cf.array(
            'li', self.cf.attr(type=int)
        )
        html = xml_engine('<ul><li>1</li><li>2</li><li>3</li><li>4</li></ul>')
        expected = [1, 2, 3, 4]
        result = await (collector(html, None))
        self.assertEqual(expected, result)
