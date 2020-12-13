from robot import Robot
from robot.collector.shortcut import *

collector = array(
    css('.theiaStickySidebar ul li'),
    dict(
        get(
            pipe(css('a[href]'), attr('href'), any()),
            dict(
                body=pipe(css('p'), as_text())
            )
        ),
        title=pipe(css('span'), as_text()),
        url=pipe(css('a[href]'), attr('href'), any(), url())
    )
)

with Robot() as robot:
    result = robot.sync_run(collector, 'https://iot.eetimes.com/')

for r in result:
    print(r)
