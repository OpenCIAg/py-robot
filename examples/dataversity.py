from robot import Robot
from robot.collector.shortcut import *

collector = pipe(
    const('http://www.dataversity.net/category/education/daily-data/'),
    get(),
    array(
        css('#primary article'),
        dict(
            pipe(
                css('a[href]'), attr('href'), any(), url(),
                get(),
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
