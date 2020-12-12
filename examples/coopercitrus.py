import json

from robot import RobotImpl
from robot.collector.shortcut import *

base_url = 'http://www.coopercitrus.com.br/'
source = 'Coopercitrus'

collector = array(
    css('#coluna_esquerda table'),
    dict(
        get(
            pipe(css('a'), attr('href'), any()),
            dict(
                date=pipe(css('#conteudo h2 + p'), as_text(), regex(r'[0-9]+/[0-9]+/[0-9]+')),
                content=pipe(css('#conteudo p'), as_text())
            )
        ),
        origin=pipe(css('a'), attr('href'), any(), url()),
        title=pipe(css('a'), as_text()),
        source=const(source),
    )
)

url_template = 'http://www.coopercitrus.com.br/?pag=noticias&pgN={0}&categoria=&busca='
with RobotImpl() as robot:
    for url in [url_template.format(page) for page in range(1, 460)]:
        result = robot.sync_run(collector, url)
        print(json.dumps(result, indent=4))
