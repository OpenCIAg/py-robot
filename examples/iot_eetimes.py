import requests
import json

from lxml import html
from pyquery.pyquery import PyQuery as pq

page = requests.get('https://iot.eetimes.com/')
dom = pq(html.fromstring(page.content.decode()))

result = []
for link in dom.find('.theiaStickySidebar ul li'):
    news = {
        'category': pq(link).find('span').text(),
        'url': pq(link).find('a[href]').attr('href'),
    }
    news_page = requests.get(news['url'])
    dom = pq(news_page.content.decode())
    news['body'] = dom.find('p').text()
    news['title'] = dom.find('h1.post-title').text()
    result.append(news)

print(json.dumps(result, indent=4))
