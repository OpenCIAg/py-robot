from aiounittest import AsyncTestCase

from robot.collector.io import FileNameCollector


class FileNameCollectorTest(AsyncTestCase):

    async def test_filename(self):
        value = 'http://example.org/assets/file.txt'
        collector = FileNameCollector()
        result = await collector(None, value)
        self.assertEqual(result, './assets/file.txt')
