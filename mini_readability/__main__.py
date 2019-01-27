#!/usr/bin/env python3

import argparse
import logging

from mini_readability.article_parser import SiteArticleParser

if __name__ == "__main__":
    # command line parsing
    cl_parser = argparse.ArgumentParser(
        usage='mini_readability [-h] [-l {notset,debug,info,warning,error,critical}] url',
    )
    cl_parser.add_argument('url', help='URL to parse')
    cl_parser.add_argument('-l', '--log', help='log level',
                           choices=['notset', 'debug', 'info', 'warning', 'error', 'critical'], default='info')
    args = cl_parser.parse_args()
    url = args.url
    loglevel = args.log

    # logging setting
    if loglevel is None:
        loglevel = 'info'
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=numeric_level)

    # site parsing
    content_parser = SiteArticleParser()
    content_parser.parse(url)
