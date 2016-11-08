# coding=utf8

import sys
import re
import urllib
import threading
import configparser
import logging
import http.cookiejar
import csv
import bs4
import time
import os
import hashlib
import glob
import json

import PyQt5

import gui.MainWindow

spacial_char = '↑↓←→↖↙↗↘↕'

url_stock_code = 'http://quote.eastmoney.com/stocklist.html'
url_currency_acronyms = 'http://www.easy-forex.com/int/zh-hans/currencyacronyms/'

api_sinajs = 'http://hq.sinajs.cn/rn={}&list={}'

key_stock_code = '">(.*?)\((.*?)\)<'


class App:
    """

    """

    isRunning = {}
    isRunning['app'] = True

    timeout = 10

    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    def __init__(self):

        logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w',
                            format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')

        self.gameData = {}

        self.firstRun()
        self.load_config()
        self.load_user()
        self.load_cache()
        self.show_gui()
        self.show_cache()
        self.fetch_data()

    def firstRun(self):
        if not os.path.isdir('log'):
            os.mkdir('log')
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')
        if not os.path.isdir('save'):
            os.mkdir('save')
        if not os.path.isdir('data'):
            os.mkdir('data')
        if not os.path.isdir('gui'):
            os.mkdir('gui')
        if not os.path.isdir('ai'):
            os.mkdir('ai')
        for file in glob.glob('tmp/*'):
            os.remove(file)

    def load_config(self):
        pass

    def load_user(self):
        pass

    def load_cache(self):
        pass

    def show_gui(self):
        def show():
            app = PyQt5.QtWidgets.QApplication(sys.argv)
            MainWindow = PyQt5.QtWidgets.QMainWindow()
            ui = window_main()
            ui.setupUi(MainWindow)
            MainWindow.show()
            sys.exit(app.exec_())
        t_gui=threading.Thread(target=show)
        t_gui.start()

    def show_cache(self):
        pass

    def fetch_data(self):
        # 根据游戏内容，综合当前网络速度与延迟，拟决定用10个线程处理以下任务：
        # 以下任务同时进行：
        def Star():
            """伴飞卫星"""
            self.isRunning['Star'] = True
            while self.isRunning['Star']:
                try:
                    pass
                except:
                    pass

        def fetchDaPanData():
            """查询大盘信息"""
            self.isRunning['fetchDaPanData'] = True
            while self.isRunning['fetchDaPanData']:
                try:
                    logging.info('正在获取查询大盘指数…')
                    logging.info('大盘指数获取完毕。')
                    self.isRunning['fetchDaPanData'] = False
                except:
                    pass

        def fetchStockCode():
            """查询股票代码"""
            self.isRunning['fetchStockCode'] = True
            while self.isRunning['fetchStockCode']:
                try:
                    logging.info('正在获取股票代码…')
                    # 构建请求
                    request = urllib.request.Request(url_stock_code)
                    # 获取响应
                    response = self.opener.open(request, timeout=self.timeout)
                    # 解码
                    stockList = response.read().decode('gbk')
                    logging.debug(stockList)
                    soup = bs4.BeautifulSoup(stockList, 'lxml')
                    pattern = re.compile('">(.*?)\((.*?)\)<')
                    self.gameData['stockCode_sh'] = re.findall(pattern, str(soup.find_all('ul')[7]))
                    self.gameData['stockCode_sz'] = re.findall(pattern, str(soup.find_all('ul')[8]))
                    logging.debug(self.gameData['stockCode_sh'],self.gameData['stockCode_sz'])
                    self.isRunning['fetchStockCode'] = False
                except Exception as e:
                    pass

        def fetchSHStock():
            """用已保存的股票代码查询上证综合股票当前信息"""
            self.isRunning['fetchSHStock'] = True
            if 'data_sh' not in self.gameData:
                self.gameData['data_sh'] = {}
            while self.isRunning['fetchSHStock']:
                try:
                    logging.info('正在获取上海股票信息…')
                    for i, v in enumerate(self.gameData['stockCode_sh']):
                        # 构建请求
                        request = urllib.request.Request(api_sinajs + 'sh' + v[1])
                        # 获取响应
                        response = self.opener.open(request, timeout=self.timeout)
                        # 解码
                        shStatusList = response.read().decode('gbk')
                        logging.debug(shStatusList)
                        info = shStatusList.split('"')[1]
                        if info == '':
                            pass
                        else:
                            tmp = info.split(',')
                            logging.debug('已获取上海"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.gameData['stockCode_sh'])))
                            self.gameData['data_sh'][tmp[0]] = tmp
                    logging.info('上海股票行情获取完毕。')
                    self.isRunning['fetchSHStock'] = False
                except Exception as e:
                    pass

        def fetchSZStock():
            """用已保存的股票代码查询深证成份股票当前信息"""
            self.isRunning['fetchSZStock'] = True
            if 'data_sz' not in self.gameData:
                self.gameData['data_sz'] = {}
            while self.isRunning['fetchSZStock']:
                try:
                    logging.info('正在获取深圳股票信息…')
                    for i, v in enumerate(self.gameData['stockCode_sz']):
                        # 构建请求
                        request = urllib.request.Request(api_sinajs + 'sz' + v[1])
                        # 获取响应
                        response = self.opener.open(request, timeout=self.timeout)
                        # 解码
                        szStatusList = response.read().decode('gbk')
                        logging.debug(szStatusList)
                        info = szStatusList.split('"')[1]
                        if info == '':
                            pass
                        else:
                            tmp = info.split(',')
                            logging.debug('已获取深圳"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.szInfo)))
                            self.gameData['data_sz'][tmp[0]] = tmp
                    logging.info('深圳股票行情获取完毕。')
                    self.isRunning['fetchSZStock'] = False
                except Exception as e:
                    pass

        star = threading.Thread(target=Star)
        dapan = threading.Thread(target=fetchDaPanData)
        stockCode = threading.Thread(target=fetchStockCode)
        shStock = threading.Thread(target=fetchSHStock)
        szStock = threading.Thread(target=fetchSZStock)
        star.start()
        dapan.start()
        stockCode.start()
        shStock.start()
        szStock.start()

class window_main(PyQt5.QtWidgets.QMainWindow,gui.MainWindow.Ui_MainWindow):
    def go(self):
        print(self.label_accountName.text())

if __name__ == '__main__':
    I = App()
