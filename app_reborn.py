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


def get_current_time():
    return str(int(time.time()))


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
            main_window = PyQt5.QtWidgets.QMainWindow()
            self.ui = Main_Window()
            self.ui.setupUi(main_window)
            main_window.show()
            sys.exit(app.exec_())

        t_gui = threading.Thread(target=show)
        t_gui.start()

    def show_cache(self):
        pass

    def fetch_data(self):
        # 根据游戏内容，综合当前网络速度与延迟，拟决定用10个线程处理以下任务：
        # 以下任务同时进行：
        def Star():
            """伴飞卫星"""
            self.isRunning['Star'] = True
            shStatus = ''
            szStatus = ''
            while self.isRunning['Star']:
                if 'stockCode_sh' in self.gameData:
                    self.shStatus = '正在获取信息：{:.2f}%'
                    if 'new_data_sh' in self.gameData:
                        rate = len(self.gameData['new_data_sh'].items()) / len(self.gameData['stockCode_sh'])
                        self.shStatus = self.shStatus.format(rate * 100)
                else:
                    self.shStatus = '正在获取代码'

                if 'stockCode_sz' in self.gameData:
                    self.szStatus = '正在获取信息：{:.2f}%'
                    if 'new_data_sz' in self.gameData:
                        rate = len(self.gameData['new_data_sz'].items()) / len(self.gameData['stockCode_sz'])
                        self.szStatus = self.szStatus.format(rate * 100)
                else:
                    self.szStatus = '正在获取代码'

                if 'ui' in dir(self):
                    self.ui.statusbar.showMessage('上海：{}；深圳：{}。'.format(self.shStatus, self.szStatus))
                time.sleep(0.1)

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
                    soup = bs4.BeautifulSoup(stockList, 'lxml')
                    pattern = re.compile('">(.*?)\((.*?)\)<')
                    self.gameData['stockCode_sh'] = re.findall(pattern, str(soup.find_all('ul')[7]))
                    self.gameData['stockCode_sz'] = re.findall(pattern, str(soup.find_all('ul')[8]))
                    self.isRunning['fetchStockCode'] = False
                except Exception as e:
                    logging.debug('fetchStockCode崩溃')

        def fetchSHStock():
            """用已保存的股票代码查询上证综合股票当前信息"""
            self.isRunning['fetchSHStock'] = True
            if 'new_data_sh' not in self.gameData:
                self.gameData['new_data_sh'] = {}
            if 'data_sh' not in self.gameData:
                self.gameData['data_sh'] = {}
            if 'fail_sh' not in self.gameData:
                self.gameData['fail_sh'] = []
            while self.isRunning['fetchSHStock']:
                if 'stockCode_sh' not in self.gameData:
                    time.sleep(0.1)
                else:
                    try:
                        logging.info('正在获取上海股票信息…')
                        tmp = []
                        for each in self.gameData['new_data_sh'].items():
                            tmp.append(each[0])
                        remainList = []
                        for each in self.gameData['stockCode_sh']:
                            if each[0] not in tmp:
                                remainList.append(each)
                        for i, v in enumerate(remainList):
                            # 构建请求
                            request = urllib.request.Request(api_sinajs.format(get_current_time(), 'sh' + v[1]))
                            # 获取响应
                            response = self.opener.open(request, timeout=self.timeout)
                            # 解码
                            shStatusList = response.read().decode('gbk')
                            info = shStatusList.split('"')[1]
                            if info == '':
                                self.gameData['fail_sh'].append(v[0])
                            else:
                                tmp = info.split(',')
                                tmp[0] = tmp[0].replace(' ', '')
                                logging.debug(
                                    '已获取上海"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.gameData['stockCode_sh'])))
                                self.gameData['new_data_sh'][tmp[0]] = tmp

                        tmp = []
                        for each in self.gameData['new_data_sh'].items():
                            tmp.append(each[0])
                        remain = []
                        for each in self.gameData['stockCode_sh']:
                            if each[0] not in tmp:
                                remain.append(each[0])
                        text = '上海股票行情获取完毕。总数{}支，已加载{}支，未加载{}支。'
                        text = text.format(len(self.gameData['stockCode_sh']),
                                           len(self.gameData['new_data_sh'].items()),
                                           len(remain))
                        logging.info(text)
                        self.gameData['data_sh'] = self.gameData['new_data_sh']
                        self.isRunning['fetchSHStock'] = False

                    except urllib.error.URLError as e:
                        print(str(e))
                        logging.debug('fetchSHStock崩溃')
                        logging.error(str(e))
                        time.sleep(0.1)

        def fetchSZStock():
            """用已保存的股票代码查询深证成份股票当前信息"""
            self.isRunning['fetchSZStock'] = True
            if 'new_data_sz' not in self.gameData:
                self.gameData['new_data_sz'] = {}
            if 'data_sz' not in self.gameData:
                self.gameData['data_sz'] = {}
            if 'fail_sz' not in self.gameData:
                self.gameData['fail_sz'] = []
            while self.isRunning['fetchSZStock']:
                if 'stockCode_sz' not in self.gameData:
                    time.sleep(0.1)
                else:
                    try:
                        logging.info('正在获取深圳股票信息…')
                        tmp = []
                        for each in self.gameData['new_data_sz'].items():
                            tmp.append(each[0])
                        print(len(tmp))
                        remainList = []
                        for each in self.gameData['stockCode_sz']:
                            if each[0] not in tmp:
                                remainList.append(each)
                        for i, v in enumerate(remainList):
                            # 构建请求
                            request = urllib.request.Request(api_sinajs.format(get_current_time(), 'sz' + v[1]))
                            # 获取响应
                            response = self.opener.open(request, timeout=self.timeout)
                            # 解码
                            szStatusList = response.read().decode('gbk')
                            info = szStatusList.split('"')[1]
                            if info == '':
                                self.gameData['fail_sz'].append(v[0])
                            else:
                                tmp = info.split(',')
                                tmp[0] = tmp[0].replace(' ', '')
                                logging.debug(
                                    '已获取深圳"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.gameData['stockCode_sz'])))
                                self.gameData['new_data_sz'][tmp[0]] = tmp

                        tmp = []
                        for each in self.gameData['new_data_sz'].items():
                            tmp.append(each[0])
                        remain = []
                        for each in self.gameData['stockCode_sz']:
                            if each[0] not in tmp:
                                remain.append(each[0])
                        text = '深圳股票行情获取完毕。总数{}支，已加载{}支，未加载{}支。'
                        text = text.format(len(self.gameData['stockCode_sz']),
                                           len(self.gameData['new_data_sz'].items()),
                                           len(remain))
                        logging.info(text)
                        self.gameData['data_sz'] = self.gameData['new_data_sz']
                        self.isRunning['fetchSZStock'] = False
                    except urllib.error.URLError as e:
                        print(str(e))
                        logging.debug('fetchSZStock崩溃')
                        logging.error(str(e))
                        time.sleep(0.1)

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


class MainWindow(PyQt5.QtWidgets.QMainWindow, gui.MainWindow.Ui_MainWindow):
    def _set_status_bar_text(self, text):
        self.statusbar.showMessage(text)


if __name__ == '__main__':
    I = App()
