#!/usr/bin/env python3

import logging

from mini_readability.article_parser import SiteArticleParser

urls = [
    'https://meduza.io/feature/2019/01/25/ya-dumal-chto-s-moey-vneshnostyu-i-moim-golosom-igrat-etogo-parnya-prosto-samoubiystvo',
    'https://meduza.io/feature/2019/01/22/oni-stali-pravitelstvom-i-my-nachali-rabotat-na-nih-irakskiy-geolog-prigovorennyy-k-kazni-rasskazal-o-razrabotke-himoruzhiya-dlya-ig',
    'https://meduza.io/feature/2019/01/27/ya-ponyal-pochemu-konservatory-schitayut-liberalov-egoistami',
    'https://lenta.ru/articles/2019/01/25/genetic_weapon/',
    'https://lenta.ru/news/2019/01/25/sleepless/',
    'https://lenta.ru/articles/2019/01/08/article/',
    'https://habr.com/ru/post/437458/',
    'https://habr.com/ru/company/1cloud/blog/437620/',
    'https://habr.com/ru/company/dsec/blog/437092/',
    'https://habr.com/ru/post/437018/',
    'https://habr.com/ru/post/435652/',
    'https://geekbrains.ru/posts/digital_2018_resume_part2',
    'https://geekbrains.ru/posts/ms_google_about_ai',
    'https://geekbrains.ru/posts/10_movies_motivates_to_learn',
    'https://www.svoboda.org/a/29722577.html',
    'https://www.svoboda.org/a/29710752.html',
    'https://www.svoboda.org/a/29492505.html',
    'https://gorobzor.ru/novosti/obschestvo/21993-v-ufe-proydut-velosipednye-sorevnovaniya-pervyy-na-snegu-2019',
    'https://gorobzor.ru/novosti/obschestvo/22004-v-ufe-sozdali-peticiyu-za-sohranenie-kinoteatra-pobeda',
    'https://gorobzor.ru/novosti/ekonomika/21958-bashkiriya-sredi-liderov-v-pfo-po-vvodu-zhilya-v-2018-godu',
]


def main():
    for url in urls:
        loglevel = 'info'
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=numeric_level)
        parser = SiteArticleParser()
        parser.parse(url)


if __name__ == "__main__":
    main()
