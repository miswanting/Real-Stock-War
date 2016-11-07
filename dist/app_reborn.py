import re
import urllib
import threading
import configparser
import logging
import http.cookiejar
import csv
import bs4
import tkinter as tk
import time
import os
import hashlib
import glob
import json
import lib_spider
import lib_gui


class App():
    def __init__(self):
        isRunning = {}
        isRunning['app'] = True
        
        logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w',
                            format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        
        self.firstRun()
    
    def firstRun(self):
        if not os.path.isdir('log'):
            os.mkdir('log')
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')
        if not os.path.isdir('storage'):
            os.mkdir('storage')
        for file in glob.glob('tmp/*'):
            os.remove(file)


if __name__ == '__main__':
    I = App()
