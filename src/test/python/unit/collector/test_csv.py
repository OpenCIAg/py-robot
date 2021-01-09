from aiounittest import AsyncTestCase
from tempfile import NamedTemporaryFile

from robot.collector.shortcut import *

content = """
a,b,c
1,2,3
3,2,1
""".lstrip()


class CsvCollectorTest(AsyncTestCase):

    async def test_csv(self):
        file = NamedTemporaryFile()
        collector = csv(
            const(file.name)
        )
        _, result = await collector(None, [
            ['a', 'b', 'c'],
            [1, 2, 3],
            [3, 2, 1],
        ])
        self.assertEqual(file.name, result)
        with open(file.name) as input_stream:
            read_content = input_stream.read()
            self.assertEqual(content, read_content)
        file.close()

    async def test_empty(self):
        file = NamedTemporaryFile()
        collector = csv(
            const(file.name)
        )
        _, result = await collector(None, [])
        self.assertEqual(file.name, result)
        with open(file.name) as input_stream:
            read_content = input_stream.read()
            self.assertEqual('', read_content)
        file.close()
