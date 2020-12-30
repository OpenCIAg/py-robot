from aiounittest import AsyncTestCase
from tempfile import NamedTemporaryFile

from robot.collector.shortcut import *

content = """
a,b,c
1,2,3
3,2,1
""".lstrip()


class DictCsvCollectorTest(AsyncTestCase):

    async def test_dict_csv(self):
        file = NamedTemporaryFile()
        collector = dict_csv(
            const(file.name)
        )
        _, result = await collector(None, [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 3, 'b': 2, 'c': 1},
        ])
        self.assertEqual(file.name, result)
        with open(file.name) as input_stream:
            read_content = input_stream.read()
            self.assertEqual(content, read_content)
        file.close()
