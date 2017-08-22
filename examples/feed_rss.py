import json

import aiohttp

from robot.core import CollectorFactory
from robot.core import Robot

url = 'https://elvisfusco.com.br/feed/'

collector_factory = CollectorFactory()

collector = collector_factory.array(
    'item', collector_factory.obj(
        title=collector_factory.attr('title'),
        author=collector_factory.attr('author'),
        description=collector_factory.attr('description'),
        link=collector_factory.attr('link'),
        link_title=collector_factory.remote('link', collector_factory.attr('title')),
        tags=collector_factory.array('category')
    )
)

robot = Robot(aiohttp, collector)

result = robot.run(url)
print(json.dumps(list(result), indent=4))
