# coding=utf8

url_stock_code = 'http://quote.eastmoney.com/stocklist.html'
url_currency_acronyms = 'http://www.easy-forex.com/int/zh-hans/currencyacronyms/'

api_sinajs = 'http://hq.sinajs.cn/rn={}&list={}'

key_stock_code = '">(.*?)\((.*?)\)<'


class Star:
    """
    独立完成爬虫任务
    """
    isRunning = {}
    isRunning['star'] = True

    def __init__(self, mission):
        self.mission = mission
        self.start()
        self.analyze()

    def start(self):
        # 分析任务
        if mission[0] == 'get':
            pass

        # 读取存档

        # 载入AI

        # 恢复缓存

    def analyze(self):
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


if __name__ == '__main__':
    I = App()
