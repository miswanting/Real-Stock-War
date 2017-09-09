# coding=utf8

import os
import glob
import socket
import threading

spacial_char = '↑↓←→↖↙↗↘↕'

url_stock_code = 'http://quote.eastmoney.com/stocklist.html'
url_currency_acronyms = 'http://www.easy-forex.com/int/zh-hans/currencyacronyms/'

api_sinajs = 'http://hq.sinajs.cn/rn={}&list={}'

key_stock_code = '">(.*?)\((.*?)\)<'

HOST = '127.0.0.1'
PORT = 6969


class App:
    """
    1. 自检；
    2. 架设服务器；
    3. 响应客户端要求。
    """
    isRunning = {}
    isRunning['app'] = True

    def __init__(self):
        self.self_check()
        self.start_server()
        self.loop()

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
                        data = conn.recv(1024)
                        if not data:
                            break
                        print('收到信息：{}'.format(data))
                        conn.sendall(data)
                    conn.close()
                    print('连接断开')
                    print()

    def loop(self):
        pass


if __name__ == '__main__':
    I = App()
