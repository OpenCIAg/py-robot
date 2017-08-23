import json

import aiohttp

from robot import CollectorFactory
from robot import Robot

url = 'http://g1.globo.com/'

cf = CollectorFactory()

collector = cf.obj(
    dolar=cf.obj(
        nome=cf.attr('[title^="Dólar"] .moeda-title'),
        valor=cf.attr('[title^="Dólar"] .moeda-valor', post_process=cf.regex('([0-9,\.]+)')),
        variacao=cf.attr('[title^="Dólar"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Dólar"]', attr='title'),
    ),
    euro=cf.obj(
        nome=cf.attr('[title^="Euro"] .moeda-title'),
        valor=cf.attr('[title^="Euro"] .moeda-valor'),
        variacao=cf.attr('[title^="Euro"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Euro"]', attr='title'),
    ),
    libra=cf.obj(
        nome=cf.attr('[title^="Libra"] .moeda-title'),
        valor=cf.attr('[title^="Libra"] .moeda-valor'),
        variacao=cf.attr('[title^="Libra"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Libra"]', attr='title'),
    ),
    peso=cf.obj(
        nome=cf.attr('[title^="Peso"] .moeda-title'),
        valor=cf.attr('[title^="Peso"] .moeda-valor'),
        variacao=cf.attr('[title^="Peso"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Peso"]', attr='title'),
    ),
)

robot = Robot(aiohttp, collector)

result = robot.run(url)
print(json.dumps(result, indent=4))
