import aiohttp

from robot import CollectorFactory
from robot import Robot

cf = CollectorFactory()

collector = cf.array('.theiaStickySidebar ul li', cf.obj(
    cf.remote(cf.attr('a[href]', attr='href'), cf.obj(
            corpo=cf.attr('p')
    )),
    titulo=cf.attr('span'),
    url=cf.attr('a[href]', attr='href'),
))

robot = Robot(aiohttp, collector)
result = robot.run('https://iot.eetimes.com/')

for r in result:
    print(r)
