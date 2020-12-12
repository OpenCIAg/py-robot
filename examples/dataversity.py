from robot import RobotImpl
from robot.collector.shortcut import *

collector = array(
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

with RobotImpl() as robot:
    result = robot.sync_run(collector, 'http://www.dataversity.net/category/education/daily-data/')

for r in result:
    print(r)
