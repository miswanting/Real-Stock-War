# coding=utf-8

import bs4
import http.cookiejar
import threading
import urllib
import logging


class Spider(object):
    """docstring for Spider"""
    
    def __init__(self):
        self.log = logging.getLogger('Spider')
        handler = logging.FileHandler('spider.log', 'w')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
