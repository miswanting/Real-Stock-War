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
import queue
import pathlib
import socket

spacial_char = '↑↓←→↖↙↗↘↕'

url_stock_code = 'http://quote.eastmoney.com/stocklist.html'
url_currency_acronyms = 'http://www.easy-forex.com/int/zh-hans/currencyacronyms/'

api_sinajs = 'http://hq.sinajs.cn/rn={}&list={}'

key_stock_code = '">(.*?)\((.*?)\)<'

HOST = '127.0.0.1'
PORT = 6969

def get_current_time():
    return str(int(time.time()))


class App:
    """
    1. 自检；
    2. 更新数据；
    3. 架设服务器；
    4. 响应客户端要求。
    """
    isRunning = {}
    isRunning['app'] = True

    timeout = 10

    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    taskQueue = queue.Queue()

    def __init__(self):
        logging.basicConfig(filename='app.log', level=logging.DEBUG, filemode='w',
                            format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        self.gameData = {}
        self.userData = {}
        self.userData['own_stock'] = {}

        self.self_check()
        self.fetch_current_data()
        self.start_server()

    def self_check(self):
        # 检查首次运行
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')  # 用于临时数据储存
        if not os.path.isdir('cache'):
            os.mkdir('cache')  # 用于当前数据储存
        if not os.path.isdir('storage'):
            os.mkdir('storage')  # 用于永久数据储存
        if not os.path.isdir('save'):
            os.mkdir('save')  # 用于存档
        if not os.path.isdir('ai'):
            os.mkdir('ai')  # 用于储存外部AI脚本
        for file in glob.glob('tmp/*'):
            os.remove(file)  # 清除临的外部数据储存

        # 读取存档

        # 载入AI

        # 恢复缓存
        if os.path.isfile('cache/data.json'):  # 判断——缓存文件存在：加载
            with open('cache/data.json', 'r')as cache_file:
                self.gameData = json.loads(cache_file.read())

    def start_server(self):
        send_func = None
        recv_func = None
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen(1)
                print('主机建立于：{}:{}'.format(HOST, PORT))
                conn, addr = s.accept()
                with conn:
                    print('建立连接：{}'.format(addr))
                    send_func = conn.send
                    recv_func = conn.recv
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        print('收到信息：{}'.format(data))
                        conn.sendall(json.dumps(self.gameData).encode())
                    conn.close()
                    print('连接断开')
                    print()

    def fetch_current_data(self):
        # 根据游戏内容，综合当前网络速度与延迟，拟决定用10个线程处理以下任务：
        # 以下任务同时进行：
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
                    self.gameData['stockCode_sh'] = re.findall(
                        pattern, str(soup.find_all('ul')[7]))
                    self.gameData['stockCode_sz'] = re.findall(
                        pattern, str(soup.find_all('ul')[8]))
                    self.isRunning['fetchStockCode'] = False
                    with open('cache/data.json', 'w') as cache_file:
                        cache_file.write(json.dumps(self.gameData))
                except Exception as e:
                    logging.debug('fetchStockCode崩溃')

        def fetchSHStock():
            """用已保存的股票代码查询上证综合股票当前信息"""
            self.isRunning['fetchSHStock'] = True
            while self.isRunning['fetchSHStock']:
                if 'stockCode_sh' not in self.gameData:
                    time.sleep(0.1)
                else:
                    load_list = []
                    for each in self.gameData['stockCode_sh']:
                        load_list.append(each)
                    ###
                    newList = []
                    for each in load_list:
                        newList.append('sh' + each[1])
                    self.gameData['new_data_sh'] = self.api_get_sinajs(
                        get_current_time(), newList)
                    self.isRunning['fetchSHStock'] = False
                    with open('cache/data.json', 'w') as cache_file:
                        cache_file.write(json.dumps(self.gameData))
            newList = []
            for each in self.gameData['new_data_sh'].keys():
                newList.append(self.gameData['new_data_sh'][each][0])
            self.ui.clean_set_list_widget_sh(newList)

        def fetchSZStock():
            """用已保存的股票代码查询深证成份股票当前信息"""
            self.isRunning['fetchSZStock'] = True
            while self.isRunning['fetchSZStock']:
                if 'stockCode_sz' not in self.gameData:
                    time.sleep(0.1)
                else:
                    load_list = []
                    for each in self.gameData['stockCode_sz']:
                        load_list.append(each)
                    ###
                    newList = []
                    for each in load_list:
                        newList.append('sz' + each[1])
                    self.gameData['new_data_sz'] = self.api_get_sinajs(
                        get_current_time(), newList)
                    self.isRunning['fetchSZStock'] = False
                    with open('cache/data.json', 'w') as cache_file:
                        cache_file.write(json.dumps(self.gameData))
            newList = []
            for each in self.gameData['new_data_sz'].keys():
                newList.append(self.gameData['new_data_sz'][each][0])
            self.ui.clean_set_list_widget_sz(newList)

        dapan = threading.Thread(target=fetchDaPanData)
        stockCode = threading.Thread(target=fetchStockCode)
        shStock = threading.Thread(target=fetchSHStock)
        szStock = threading.Thread(target=fetchSZStock)
        dapan.start()
        stockCode.start()
        shStock.start()
        szStock.start()

    def api_get_sinajs(self, time, codeList):
        """
        :param time:int
        :param codeList:string_list
        :return info_dict:list_dict
        """
        num_of_each_ask = 10  # 每次网络请求所询问的资料数量
        ask_times = int(len(codeList) / num_of_each_ask) + 1  # 计算出一共需请求多少次
        # 把请求进行组合
        request_code_dict = {}
        for i in range(ask_times):
            request_code_dict[','.join(
                codeList[i * num_of_each_ask:i * num_of_each_ask + num_of_each_ask])] = False
        # 生成代码与回复对应的字典
        code_raw_dict = {}
        retry = True
        while retry:
            for each in request_code_dict.keys():
                # 构建请求
                request = urllib.request.Request(api_sinajs.format(time, each))
                # 获取响应
                response = self.opener.open(request, timeout=self.timeout)
                # 解码
                try:
                    raw_respond = response.read().decode('gbk')
                except urllib.error.URLError as e:
                    pass
                else:
                    respond_string_list = raw_respond.split('\n')
                    for i, every in enumerate(respond_string_list):
                        if every != '':
                            code_raw_dict[each.split(',')[i]] = every
                        else:
                            pass
                    request_code_dict[each] = True
                finally:
                    retry = False
                    for every in request_code_dict.keys():
                        if not request_code_dict[every]:
                            retry = True
        # 生成列表
        code_info_dict = {}
        for each in code_raw_dict.keys():
            value = code_raw_dict[each].split('"')[1]
            if value == '':
                text = 'api返回Null。{}'
                text = text.format(each)
                logging.debug(text)
            elif value == 'FAILED':
                text = 'api返回FAILED。{}'
                text = text.format(each)
                logging.debug(text)
            else:
                info = value.split(',')
                info[0] = info[0].replace(' ', '')
                code_info_dict[each] = info
        return code_info_dict


if __name__ == '__main__':
    I = App()
