import json
from robot import Robot
from robot.collector.shortcut import *

collector = get(
    const('https://iot.eetimes.com/'),
    array(
        css('.theiaStickySidebar ul li'),
        dict(
            get(
                pipe(css('a[href]'), attr('href'), any()),
                dict(
                    body=pipe(css('p'), as_text()),
                    title=pipe(css('h1.post-title'), as_text()),
                )
            ),
            category=pipe(css('span'), as_text()),
            url=pipe(css('a[href]'), attr('href'), any(), url())
        )
    )
)

with Robot() as robot:
    result = robot.sync_run(collector)
print(json.dumps(result, indent=4))
