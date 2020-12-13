from aiounittest import AsyncTestCase

from robot.api import XmlEngine
from robot.xml_engine.pyquery_engine import PyQueryAdapter

raw_html = b"""
    <table>
        <tr>
            <td row="0" col="0">1</td>
            <td row="0" col="1">2</td>
        </tr>
        <tr>
            <td row="1" col="1">3</td>
            <td row="1" col="1">4</td>
        </tr>
    </table>
"""


class PyQueryEngineTest(AsyncTestCase):
    xml_engine: XmlEngine

    @classmethod
    def setUpClass(cls):
        cls.xml_engine = PyQueryAdapter()

    def test_parse_table(self):
        result = self.xml_engine(raw_html)
        self.assertIsNotNone(result)

    def test_as_text(self):
        result = self.xml_engine(raw_html).as_text()
        self.assertEqual(result, "1\n2\n3\n4")

    def test_nested_as_text(self):
        result = self.xml_engine(raw_html).find_by_css('tr td').as_text()
        self.assertEqual(result, "1 2 3 4")

    def test_xpath(self):
        result = self.xml_engine(raw_html).find_by_xpath("//td").as_text()
        self.assertEqual(result, "1 2 3 4")

    def test_array_text(self):
        result = self.xml_engine(raw_html).find_by_css("tr").text()
        self.assertEqual(list(result), ["1\n2", "3\n4"])

    def test_array_attr(self):
        result = self.xml_engine(raw_html).find_by_css("td").attr('row')
        self.assertEqual(list(result), ["0", "0", "1", "1"])
