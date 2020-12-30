import json
from robot import Robot
from robot.collector.shortcut import *
import logging

logging.basicConfig(level=logging.DEBUG)

collector = pipe(
    const('https://iot.eetimes.com/'),
    get(),
    css('.theiaStickySidebar ul li'),
    foreach(dict(
        pipe(
            css('a[href]'), attr('href'), any(),
            get(),
            dict(
                body=pipe(css('p'), as_text()),
                title=pipe(css('h1.post-title'), as_text()),
            )
        ),
        category=pipe(css('span'), as_text()),
        url=pipe(css('a[href]'), attr('href'), any(), url())
    ))
)

with Robot() as robot:
    result = robot.sync_run(collector)
print(json.dumps(result, indent=4))
