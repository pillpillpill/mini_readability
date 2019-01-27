#!/usr/bin/env python3

import argparse
import logging
import os
import re

import requests
from bs4 import BeautifulSoup


class SiteArticleInformation:
    def __init__(self, url, location, content):
        self.url = url
        self.location = location
        self.content = content


class SiteArticleParser:
    def __init__(self):
        pass

    def __resolve_url(self, url) -> str:
        # checking and formatting URL to the processed format
        if re.match(r'^https://.+', url) is None and re.match(r'^http://.+', url) is None:
            url = 'http://' + url
        return url

    def __return_content(self, url) -> str:
        # trying to get site content
        try:
            req = requests.get(url)
            return req.text
        except requests.RequestException as e:
            logging.info('An error occurred while trying to get site content')
            logging.error(e.__str__())

    def __format_text(self, text, max_symbols_on_line=80) -> str:
        # formatting text to necessary format
        result_text = ''
        text = text.replace('\r', '')
        text_list = text.split('\n')
        for line in text_list:
            if line == '':
                continue
            current_line = ''
            words_list = line.split(' ')
            for word in words_list:
                length_with_word = len(current_line + word)
                if length_with_word < max_symbols_on_line:
                    current_line += word + ' '
                elif length_with_word == max_symbols_on_line:
                    result_text += current_line + word + '\r\n'
                    current_line = ''
                else:
                    result_text += current_line.strip() + '\r\n'
                    current_line = word + ' '
            if current_line != '':
                result_text += current_line.strip() + '\r\n'
            result_text += '\r\n'
        return result_text

    def __replace_in_str(self, regexp_to_replace, str_to_place, string):
        result_string = string
        counter = 0
        while re.search(regexp_to_replace, result_string, re.M | re.S) and counter < 10:
            result_string = re.sub(regexp_to_replace, str_to_place, result_string, re.M)
            counter += 1
        return result_string

    def __parse_article(self, text) -> str:
        result_text = ''
        text = re.sub(r'<a [^>]*href=\"(.+?)\".*?>(.*?)</a>', r'\2 [\1]', text, re.M | re.S)
        re_result_list = re.findall(
            r'<p(| .*?)>(.*?)</p>|<h(\d).*?>(.*?)</h\3>|<div[^>]*?text[^>]*?>(.*?)</div>',
            text, re.S | re.M)
        for item in re_result_list:
            if item[1] != '':
                string = item[1]
            elif item[3] != '':
                string = item[3]
            elif item[4] != '':
                string = item[4]
            else:
                continue
            string = self.__replace_in_str(r'&.*?;', ' ', string)
            string = self.__replace_in_str(r'<img.*?>', '', string)
            string = self.__replace_in_str(r'<br/>', '', string)
            string = self.__replace_in_str(r'</?ul>', '', string)
            string = self.__replace_in_str(r'</?blockquote>', '', string)
            string = self.__replace_in_str(r'<iframe.*?>.*?</iframe>', '', string)
            string = self.__replace_in_str(r'<div[^>]*?>', '', string)
            string = self.__replace_in_str(r'<hr/>', '', string)

            string = self.__replace_in_str(r'<a [^>]*href=\"(.+?)\".*?>(.*?)</a>', r'\2 [\1]', string)
            string = self.__replace_in_str(r'<pre[^>]*?>(.*?)</pre>', r'\1', string)
            string = self.__replace_in_str(r'<code[^>]*?>(.*?)</code>', r'\1', string)
            string = self.__replace_in_str(r'<a.*?>(.*?)</a>', '', string)
            string = self.__replace_in_str(r'<i>(.*?)</i>', r'\1', string)
            string = self.__replace_in_str(r'<i>(.*?)\s</i>', r'\1', string)
            string = self.__replace_in_str(r'<h(\d)[^>]*?>(.*?)</h\1>', r'\2', string)
            string = self.__replace_in_str(r'<li>(.*?)</li>', r'- \1', string)
            string = self.__replace_in_str(r'<li>(.*?)\s</li>', r'- \1', string)
            string = self.__replace_in_str(r'<span[^>]*?>(.+?)</span.*>', r'\1', string)
            string = self.__replace_in_str(r'<b[^>]*?>(.*?)</b>', r'\1', string)
            string = self.__replace_in_str(r'<strong>(.*?)</strong>', r'\1', string)
            string = self.__replace_in_str(r'<em>(.*?)</em>', r'\1', string)
            string = self.__replace_in_str(r'<font[^>]*?>(.*?)</font>', r'\1', string)
            string = self.__replace_in_str(r'<p[^>]*?>(.*?)</p>', r'\1\n', string)

            string = self.__replace_in_str(r'</?i>', '', string)
            string = self.__replace_in_str(r'</?p>', '', string)
            string = self.__replace_in_str(r'</?math>', '', string)
            string = self.__replace_in_str(r'</?table>', '', string)
            string = self.__replace_in_str(r'</?thead>', '', string)
            string = self.__replace_in_str(r'</?tr>', '', string)
            string = self.__replace_in_str(r'</?th>', '', string)
            string = self.__replace_in_str(r'</?tbody>', '', string)
            string = self.__replace_in_str(r'</?td>', '', string)
            string = self.__replace_in_str(r'</?ol>', '', string)
            string = self.__replace_in_str(r'</?pre[^>]*?>', '', string)
            string = self.__replace_in_str(r'</?code[^>]*?>', '', string)
            string = self.__replace_in_str(r'<br/>', '', string)
            result_text += string + '\n'
        return result_text

    def __process_content(self, text) -> str:
        # parsing site content for useful information

        soup = BeautifulSoup(text, 'lxml')

        # search h1
        title_text = soup.h1.text.strip()

        # search article
        if soup.article:
            article_soup = soup.article
        else:
            article_soup = soup.find('div', itemprop=re.compile(r'.*article.*', re.IGNORECASE))
            if article_soup is None:
                article_soup = soup.find('div', id=re.compile(r'.*article.*', re.IGNORECASE))
                if article_soup is None:
                    article_soup = soup.find('div', class_=re.compile(r'.*article.*', re.IGNORECASE))
                    if article_soup is None:
                        article_soup = soup.body
                        if article_soup is None:
                            article_soup = soup
        article_text = str(article_soup)
        logging.debug(article_text)

        # parse article
        result_text = self.__parse_article(article_text)
        result_text = result_text.strip()
        if not re.match(title_text, result_text):
            result_text = title_text + '\n' + result_text

        result_text = self.__format_text(result_text).strip()
        return result_text

    def __write_text_to_file(self, url, text) -> str:
        # resolving path
        suffix = '.txt'
        path = os.path.join(os.getcwd(), 'articles')
        url_to_path = re.sub(r'.+://', '', url).split('?', 1)[0].strip('/')
        url_path_list = url_to_path.split('/')
        for item in url_path_list:
            path = os.path.join(path, item[0:255])
        filename = path + suffix

        # making directories and file and writing
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as file:
                file.write(text)
            return filename
        except PermissionError as e:
            logging.info('An error occurred while trying to make file in that directory, try another directory')
            logging.error(e.__str__())

    def parse(self, url) -> SiteArticleInformation:
        url = self.__resolve_url(url)
        logging.debug(url)

        site_content = self.__return_content(url)
        logging.debug(site_content)

        if site_content:
            result_text = self.__process_content(site_content)
            logging.debug(result_text)
            if result_text:
                result_file_location = self.__write_text_to_file(url, result_text)
                logging.debug(result_file_location)
                if result_file_location:
                    result_article = SiteArticleInformation(url, result_file_location, site_content)
                    logging.info('File with result: ' + result_article.location)
                    return result_article
            else:
                logging.info('Parsing returns no information')
        else:
            logging.info('Site returns no information')
