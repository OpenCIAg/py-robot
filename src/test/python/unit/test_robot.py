from aiounittest import AsyncTestCase
from pytest_httpserver import HTTPServer

from robot import Robot
from robot.collector.shortcut import *

main_page = """
<html>
   <h1>Hello</h1>
   <a href="/list/">List</a>
</html>
"""

list_page = """
<html>
    <body>
        <ul>
            <li>
                <a href="/list/item/1">Link 1</a>
            </li>
            <li>
                <a href="/list/item/2">Link 2</a>
            </li>
        </ul>
    </body>
</html>
"""

item_page_template = """
<html>
    <body>
        <article id="main">
            <p>
                Item {}
            </p>
        </article>
    </body>
</html>
"""


def prepare_server(http_server: HTTPServer):
    http_server.expect_request('/', method='GET').respond_with_data(
        response_data=main_page,
    )
    http_server.expect_request('/list/', method='GET').respond_with_data(
        response_data=list_page,
    )
    for i in range(1, 3):
        http_server.expect_request(f'/list/item/{i}', method='GET').respond_with_data(
            status=302,
            headers={
                'Location': f'/list-item-{i}'
            }
        )
        http_server.expect_request(f'/list-item-{i}', method='GET').respond_with_data(
            response_data=item_page_template.format(i),
        )
    return http_server


class RobotTest(AsyncTestCase):
    robot: Robot = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.robot = Robot()

    def test_sync_run_noop(self):
        with self.robot as robot:
            result = robot.sync_run(noop())
            self.assertIsNone(result)

    async def test_async_run_noop(self):
        result = await self.robot.run(noop())
        self.assertIsNone(result)

    async def test_against_server(self):
        http_server = HTTPServer()
        http_server = prepare_server(http_server)
        with http_server as server:
            collector = pipe(
                const(server.url_for('/')),
                get(),
                css('a[href]'), attr('href'), any(),
                get(),
                css('ul > li > a[href]'),
                foreach(pipe(
                    attr('href'), any(),
                    get(),
                    css('#main p'), as_text(),
                ))
            )
            result = await self.robot.run(collector)
            expected = [
                "Item 1",
                "Item 2",
            ]
            self.assertEqual(result, expected)
