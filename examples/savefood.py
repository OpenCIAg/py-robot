import aiohttp

from robot import CollectorFactory
from robot import Robot

base_url = 'https://www.savefoodbrasil.org'
source = 'Savefoodbrasil'

cf = CollectorFactory()
collector = cf.array(
    '.box-noticias', cf.obj(
        cf.remote(cf.attr('a', attr='href', prefix=base_url), cf.obj(cf.remote('#conteudo .texto a', cf.obj(
            content=cf.attr('body'),
        )))),
        origin=cf.attr('a', attr='href', prefix=base_url),
        title=cf.attr('.not-titulo'),
        summary=cf.attr('.not-resumo'),
        source=cf.const(source)
    )
)

url = 'https://www.savefoodbrasil.org/noticias'
robot = Robot(aiohttp, collector)
result = robot.run(url)
for r in result:
    print(r)
