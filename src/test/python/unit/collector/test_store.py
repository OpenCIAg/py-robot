import json
from aiounittest import AsyncTestCase
from tempfile import NamedTemporaryFile

from robot.collector.shortcut import *


class StoreCollectorTest(AsyncTestCase):

    async def test_store(self):
        obj = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        file = NamedTemporaryFile()
        collector = store(
            const(file.name)
        )
        _, result = await collector(None, obj)
        self.assertEqual(file.name, result)
        with open(file.name) as input_stream:
            read_content = json.loads(input_stream.read())
            self.assertEqual(obj, read_content)
        file.close()
