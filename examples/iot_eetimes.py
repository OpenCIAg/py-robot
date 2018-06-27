import requests

from lxml import html
from pyquery.pyquery import PyQuery as pq

page = requests.get('https://iot.eetimes.com/')
dom = pq(html.fromstring(page.content.decode()))

noticias = []
for link in dom.find('.theiaStickySidebar ul a[href]'):
    noticia = {
        'titulo':pq(link).find('span').text(),
        'url': pq(link).attr('href')
    }
    noticia_pagina = requests.get(noticia['url'])
    dom = pq(noticia_pagina.content.decode())
    noticia['corpo'] = dom.find('p').text()
    noticias.append(noticia)

for n in noticias:
    print(n)




