from aiounittest import AsyncTestCase
from robot import Robot
from robot.collector.shortcut import *


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
