import json

from robot import RobotImpl
from robot.collector.shortcut import *

url = 'https://elvisfusco.com.br/feed/'

collector = array(
    css('item'),
    dict(
        title=pipe(css('title'), as_text()),
        author=pipe(css('author'), as_text()),
        description=pipe(css('description'), as_text()),
        link=pipe(css('link'), as_text()),
        link_title=get(
            pipe(css('link'), as_text()),
            pipe(css('title'), as_text()),
        ),
        tags=pipe(css('category'), text()),
    )
)

with RobotImpl() as robot:
    result = robot.sync_run(collector, url)
    print(json.dumps(list(result), indent=4))
