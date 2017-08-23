from unittest import TestCase
from robot.core import xml_engine
import asyncio

from robot import CollectorFactory


class ObjectCollectorTest(TestCase):
    loop = asyncio.get_event_loop()
    cf = None

    def setUp(self):
        self.cf = CollectorFactory()

    def test_from_div(self):
        collector = self.cf.obj(
            title=self.cf.attr('div.title'),
            summary=self.cf.attr('div.summary'),
        )
        html = xml_engine('<div class="title">title content</div><div class="summary">summary content</div>')
        expected = dict(title="title content", summary="summary content")
        result = self.loop.run_until_complete(collector(html, None))
        self.assertEqual(expected, result)
