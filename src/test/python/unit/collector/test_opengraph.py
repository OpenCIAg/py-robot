from aiounittest import AsyncTestCase

from robot.collector.opengraph import dict_opengraph, obj_opengraph, OpenGraph
from robot.xml_engine.pyquery_engine import PyQueryAdapter

page = """
<!DOCTYPE html>
<html>
    <head>
        <meta property="og:title" content="OpenGraph Title" />
        <meta property="og:description" content="OpenGraph Description" />
    </head>
</html>
"""


class OpenGraphTest(AsyncTestCase):

    def test_init(self):
        og = OpenGraph(title='title')
        self.assertEqual(og.title, og['title'])


class OpenGraphCollectorTest(AsyncTestCase):

    async def test_dict_collector(self):
        xml_node = PyQueryAdapter()(page)
        collector = dict_opengraph
        _, result = await collector(None, xml_node)
        expected = {
            'title': 'OpenGraph Title',
            'type': None,
            'locale': None,
            'description': "OpenGraph Description",
            'url': None,
            'site_name': None,
            'image': None,
            'audio': None,
            'video': None,
            'app_id': None,
        }
        self.assertDictEqual(result, expected)

    async def test_obj_collector(self):
        xml_node = PyQueryAdapter()(page)
        collector = obj_opengraph()
        _, result = await collector(None, xml_node)
        expected = OpenGraph(
            title='OpenGraph Title',
            description='OpenGraph Description',
        )
        self.assertEqual(result, expected)
