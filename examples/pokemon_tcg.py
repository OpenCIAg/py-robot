import json

from robot import Robot
from robot.collector.shortcut import *
import logging

logging.basicConfig(level=logging.DEBUG)

main_url = 'https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/'
expansion_search_url = 'https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/{page}?{expansion}='

expansion_collector = pipe(
    const(main_url),
    get(),
    css('.expansions-category ul li input'),
    attr('name'),
    foreach(fn(lambda it: (it, expansion_search_url.format(page=1, expansion=it),))),
)

with Robot() as robot:
    result = robot.sync_run(expansion_collector)
    for expansion_value, expansion_first_page in result:
        page_collector = pipe(
            const(expansion_first_page),
            get(),
            css('#cards-load-more span'),
            as_text(),
            regex(r'\d+ of (\d+)'),
            fn(int),
            fn(lambda total_pages: range(1, total_pages + 1)),
            foreach(pipe(
                fn(lambda page: expansion_search_url.format(page=page, expansion=expansion_value)),
                get(),
                css('section.card-results ul.cards-grid li a[href]'),
                foreach(pipe(
                        attr('href'), any(), url(),
                        get(),
                        dict(
                            url=pipe(context(), jsonpath('$.url'), any()),
                            name=pipe(css('.card-description h1'), as_text()),
                            type=pipe(css('.card-type h2'), as_text()),
                            picture=pipe(
                                css('.card-detail .card-image img'),
                                attr('src'),
                                any(),
                                download(),
                            )
                        )
                ))
            )),
            flat(),
            tap(dict_csv(const('{}.csv'.format(expansion_value)))),
        )
        page_result = robot.sync_run(page_collector)
        print(json.dumps(list(page_result), indent=4))
