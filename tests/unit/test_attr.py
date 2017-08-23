from unittest import TestCase
from robot.core import xml_engine
import asyncio

from robot import CollectorFactory


class AttributeCollectorTest(TestCase):
    loop = asyncio.get_event_loop()
    cf = None

    def setUp(self):
        self.cf = CollectorFactory()

    def test_from_div(self):
        collector = self.cf.attr('div.title')
        html = xml_engine('<div class="title">title content</div><div class="summary">summary content</div>')
        expected = "title content"
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)
