from robot import Robot
from robot.collector.shortcut import *

collector = get(
    const('http://www.dataversity.net/category/education/daily-data/'),
    array(
        css('#primary article'),
        dict(
            get(
                pipe(css('a[href]'), attr('href'), any(), url()),
                dict(
                    body=pipe(css('.entry-content p'), as_text())
                )
            ),
            title=pipe(css('.entry-title'), as_text()),
            url=pipe(css('a[href]'), attr('href'), any(), url()),
        )
    )
)
with Robot() as robot:
    result = robot.sync_run(collector)

for r in result:
    print(r)
