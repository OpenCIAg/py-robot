import json
import re
import aiohttp

from robot import CollectorFactory
from robot import Robot
from itertools import chain

url = 'http://www.visaonoticias.com/noticias/mundo/%d/'

cf = CollectorFactory()

collector = cf.array(
    'table.textos table tr:first > td:first > div',
    cf.obj(
        cf.remote('a[href]', cf.obj(
            summary=cf.attr('.resumo'),
            content=cf.attr('.conteudo p'),
            images=cf.array('.conteudo img', cf.attr(attr='src', prefix='http://www.visaonoticias.com/')),
        )),
        title=cf.attr('.titulos'),
        link=cf.attr('a[href]', attr='href', prefix='http://www.visaonoticias.com/'),
    )
)

robot = Robot(aiohttp, collector)

pages = range(1, 11)
result = list(chain(*robot.run_many(*[url % p for p in pages])))
print(json.dumps(result, indent=4))
