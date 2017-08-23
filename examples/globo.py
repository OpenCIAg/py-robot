import json
import re
import aiohttp

from robot import CollectorFactory
from robot import Robot

url = 'http://g1.globo.com/'

cf = CollectorFactory()

collector = cf.obj(
    dolar=cf.obj(
        nome=cf.attr('[title^="Dólar"] .moeda-title'),
        valor=cf.attr('[title^="Dólar"] .moeda-valor', regex=re.compile(r'([0-9,\.]+)')),
        variacao=cf.attr('[title^="Dólar"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Dólar"]', attr='title', regex=re.compile(r': *(.*)$')),
    ),
    euro=cf.obj(
        nome=cf.attr('[title^="Euro"] .moeda-title'),
        valor=cf.attr('[title^="Euro"] .moeda-valor', regex=re.compile(r'([0-9,\.]+)')),
        variacao=cf.attr('[title^="Euro"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Euro"]', attr='title', regex=re.compile(r': *(.*)$')),
    ),
    libra=cf.obj(
        nome=cf.attr('[title^="Libra"] .moeda-title'),
        valor=cf.attr('[title^="Libra"] .moeda-valor', regex=re.compile(r'([0-9,\.]+)')),
        variacao=cf.attr('[title^="Libra"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Libra"]', attr='title', regex=re.compile(r': *(.*)$')),
    ),
    peso=cf.obj(
        nome=cf.attr('[title^="Peso"] .moeda-title'),
        valor=cf.attr('[title^="Peso"] .moeda-valor', regex=re.compile(r'([0-9,\.]+)')),
        variacao=cf.attr('[title^="Peso"] .moeda-variacao'),
        atualizacao=cf.attr('[title^="Peso"]', attr='title', regex=re.compile(r': *(.*)$')),
    ),
)

robot = Robot(aiohttp, collector)

result = robot.run(url)
print(json.dumps(result, indent=4))
