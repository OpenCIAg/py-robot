import aiohttp

from robot import CollectorFactory
from robot import Robot

cf = CollectorFactory()

collector = cf.array('.listing .post', cf.obj(
    cf.remote(cf.attr('a[href]', attr='href'), cf.obj(
            corpo=cf.attr('.entry p')
    )),
    titulo=cf.attr('.posttitle'),
    url=cf.attr('a[href]', attr='href'),
))

robot = Robot(aiohttp, collector)
result = robot.run('http://www.dataversity.net/category/education/daily-data/')

for r in result:
    print(r)
