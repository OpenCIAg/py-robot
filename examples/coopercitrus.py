import json
import re

import aiohttp

from robot import CollectorFactory
from robot import Robot

base_url = 'http://www.coopercitrus.com.br/'
source = 'Coopercitrus'
cf = CollectorFactory()
collector = cf.array(
    '#coluna_esquerda table', cf.obj(
        cf.remote('a', cf.obj(
            date=cf.attr('#conteudo h2 + p', regex=re.compile(r'[0-9]+/[0-9]+/[0-9]+')),
            content=cf.attr('#conteudo p'),
        )),
        origin=cf.attr('a', attr='href', prefix=base_url),
        title=cf.attr('a'),
        source=cf.const(source)
    )
)

url_template = 'http://www.coopercitrus.com.br/?pag=noticias&pgN={0}&categoria=&busca='
robot = Robot(aiohttp, collector)
for url in [url_template.format(page) for page in range(1, 460)]:
    result = robot.run(url)
    print(json.dumps(result, indent=4))
