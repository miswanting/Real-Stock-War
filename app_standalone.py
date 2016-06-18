# coding=utf-8

import re, urllib, threading, configparser, logging, http.cookiejar, csv, bs4, tkinter as tk, time, os

class app(object):
    """docstring for app"""

    timeout = 10

    shProgress = '未开始'
    szProgress = '未开始'

    def __init__(self):
        super(app, self).__init__()

        self.setting = configparser.ConfigParser()
        self.urls = configparser.ConfigParser()

        self.cookie = http.cookiejar.CookieJar()
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler)

        self.loadConfig()
        # self.loadUser()
        self.show()
        self.fetchData()

        # self.analyzeData()
        # self.show()
        # self.loop()
    def loadConfig(self):
        self.urls.read('prefab/urls.cfg')
        self.setting.read('prefab/setting.cfg')
        logging.basicConfig(filename='log/app_standalone.log', format='[%(msecs)d][%(levelname)s][%(threadName)s]%(message)s', filemode='w', level=int(self.setting['setting']['logLevel']))
    def fetchData(self):
        def getHL():
            redo = True
            while redo:
                try:
                    logging.info('正在获取汇率…')
                    huilvURL = self.urls['urls']['美元人民币汇率']
                    # 构建请求
                    request = urllib.request.Request(huilvURL)
                    # 获取响应
                    response = self.opener.open(request, timeout=self.timeout)
                    # 解码
                    huilv = response.read().decode('gbk')
                    pattern = re.compile('"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)"')
                    huilvInfo = re.findall(pattern, str(huilv))
                    with open('tmp/huilv.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(huilvInfo[0])
                    redo = False
                    logging.info('汇率获取完毕。')
                except Exception as e:
                    logging.error(str(e))
        def getGPCode():
            redo = True
            while redo:
                try:
                    logging.info('正在获取股票代码…')
                    stockListURL = self.urls['urls']['股票代码']
                    # 构建请求
                    request = urllib.request.Request(stockListURL)
                    # 获取响应
                    response = self.opener.open(request, timeout=self.timeout)
                    # 解码
                    stockList = response.read().decode('gbk')
                    soup = bs4.BeautifulSoup(stockList, 'lxml')
                    pattern = re.compile('">(.*?)\((.*?)\)<')
                    self.shInfo = re.findall(pattern, str(soup.find_all('ul')[7]))
                    self.szInfo = re.findall(pattern, str(soup.find_all('ul')[8]))
                    with open('tmp/shList.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        for i in self.shInfo:
                            writer.writerow(i)
                    with open('tmp/szList.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        for i in self.szInfo:
                            writer.writerow(i)
                    redo = False
                except Exception as e:
                    logging.error(str(e))
        def getDPStatus():
            redo = True
            while redo:
                try:
                    logging.info('正在获取查询大盘指数…')
                    self.DPStatusURL = self.urls['urls']['大盘指数查询']
                    # 构建请求
                    request = urllib.request.Request(self.DPStatusURL)
                    # 获取响应
                    response = self.opener.open(request, timeout=self.timeout)
                    # 解码
                    dpStatusList = response.read().decode('gbk')
                    self.dpList = []
                    for i, v in enumerate(dpStatusList.split('\n')):
                        if v != '':
                            info = v.split('"')[1]
                            if info == '':
                                pass
                            else:
                                tmp = info.split(',')
                                logging.debug('已获取大盘指数"%s"的信息。(%s/%s)' % (tmp[0], i, len(dpStatusList.split('\n'))))
                                self.dpList.append(tmp)
                    with open('tmp/dpStatus.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        for i in self.dpList:
                            writer.writerow(i)
                    redo = False
                    logging.info('大盘指数获取完毕。')
                except Exception as e:
                    logging.error(str(e))
        def getSHStatus():
            redo = True
            while redo:
                try:
                    logging.info('正在获取上海股票行情…')
                    self.statusURL = self.urls['urls']['行情查询']
                    self.shList = []
                    for i, v in enumerate(self.shInfo):
                        # 构建请求
                        request = urllib.request.Request(self.statusURL + 'sh' + v[1])
                        # 获取响应
                        response = self.opener.open(request, timeout=self.timeout)
                        # 解码
                        shStatusList = response.read().decode('gbk')
                        info = shStatusList.split('"')[1]
                        if info == '':
                            pass
                        else:
                            tmp = info.split(',')
                            logging.debug('已获取上海"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.shInfo)))
                            self.shProgress = '%s/%s' % (i, len(self.shInfo))
                            self.shList.append(tmp)
                    with open('tmp/shStatus.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        for i in self.shList:
                            writer.writerow(i)
                    redo = False
                    self.shProgress = '刷新完成'
                    logging.info('上海股票行情获取完毕。')
                except Exception as e:
                    self.szProgress = '出现问题，等待重试'
                    logging.error(str(e))
        def getSZStatus():
            redo = True
            while redo:
                try:
                    logging.info('正在获取深圳股票行情…')
                    self.szList = []
                    for i, v in enumerate(self.szInfo):
                        # 构建请求
                        request = urllib.request.Request(self.statusURL + 'sz' + v[1])
                        # 获取响应
                        response = self.opener.open(request, timeout=self.timeout)
                        # 解码
                        szStatusList = response.read().decode('gbk')
                        info = szStatusList.split('"')[1]
                        if info == '':
                            pass
                        else:
                            tmp = info.split(',')
                            logging.debug('已获取深圳"%s"的股票行情。(%s/%s)' % (tmp[0], i, len(self.szInfo)))
                            self.szProgress = '%s/%s' % (i, len(self.szInfo))
                            self.szList.append(tmp)
                    with open('tmp/szStatus.csv', 'w') as csvFile:
                        writer = csv.writer(csvFile)
                        for i in self.szList:
                            writer.writerow(i)
                    redo = False
                    self.szProgress = '刷新完成'
                    logging.info('深圳股票行情获取完毕。')
                except Exception as e:
                    self.szProgress = '出现问题，等待重试'
                    logging.error(str(e))
        HLSpider = threading.Thread(target=getHL, name='HLSpider', daemon=True)
        HLSpider.start()
        CodeSpider = threading.Thread(target=getGPCode, name='CodeSpider', daemon=True)
        CodeSpider.start()
        DPSpider = threading.Thread(target=getDPStatus, name='DPSpider', daemon=True)
        DPSpider.start()
        CodeSpider.join()
        SHSpider = threading.Thread(target=getSHStatus, name='SHSpider', daemon=True)
        SHSpider.start()
        SZSpider = threading.Thread(target=getSZStatus, name='SZSpider', daemon=True)
        SZSpider.start()
        # HLSpider.join()
        # DPSpider.join()
        # SHSpider.join()
        # SZSpider.join()

    def show(self):
        try:
            def showGUI():
                running = True
                def say_hi():
                    print("hi there, everyone!")

                def createLoginPage():
                    def userEntryReady(e):
                        userName.set('')
                    def passEntryReady(e):
                        password.set('')
                        passEntry.config(show='*')
                    userName.set('请输入用户名')
                    password.set('请输入密码')
                    repeat.set('请再次输入密码')
                    repeEntry.place_forget()
                    userEntry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
                    passEntry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                    loginB.place(relx=0.45, rely=0.6, anchor=tk.CENTER)
                    regisB.place(relx=0.55, rely=0.6, anchor=tk.CENTER)
                    userEntry.bind('<Button-1>', userEntryReady)
                    passEntry.bind('<Button-1>', passEntryReady)

                def login():
                    saveFileList = os.walk('save')
                    isExist = False
                    for rootPath, dirs, files in saveFileList:
                        for each in files:
                            if each == userName.get():
                                isExist = True
                    if isExist:
                        userFile = configparser.ConfigParser()
                        userFile.read('save/' + userName.get())
                        if userFile['Account']['pw'] == password.get():
                            userEntry.place_forget()
                            passEntry.place_forget()
                            loginB.place_forget()
                            regisB.place_forget()
                            createMenu()
                        else:
                            print('密码错误！')
                    else:
                        print('用户不存在！')

                def regis():
                    def repeEntryReady(e):
                        repeat.set('')
                        repeEntry.config(show='*')

                    loginB.place_forget()
                    repeEntry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
                    regisB.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

                    if repeat.get() == '请再次输入密码':
                        repeEntry.bind('<Button-1>', repeEntryReady)
                    else:
                        if password.get() == repeat.get():
                            saveFileList = os.walk('save')
                            isExist = False
                            for rootPath, dirs, files in saveFileList:
                                for each in files:
                                    if each == userName.get():
                                        isExist = True
                            if isExist:
                                print('用户已存在！')
                            else:
                                userFile = configparser.ConfigParser()
                                userFile['Account'] = {
                                'pw' : password.get(),
                                'group' : 'player',
                                'total_assets' : ''
                                }
                                with open('save/' + userName.get(), 'w') as configFile:
                                    userFile.write(configFile)
                                    repeEntry.place_forget()
                                    userEntry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
                                    passEntry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                                    loginB.place(relx=0.45, rely=0.6, anchor=tk.CENTER)
                                    regisB.place(relx=0.55, rely=0.6, anchor=tk.CENTER)
                        else:
                            print('两次输入密码不一致，请重新输入')
                            password.set('')
                            repeat.set('')
                    # createLoginPage()

                def createMenu():
                    menuBar = tk.Menu(root)

                    gameMenu = tk.Menu(menuBar, tearoff=0)
                    gameMenu.add_command(label="开始新游戏", command=say_hi)
                    gameMenu.add_command(label="继续游戏", command=say_hi)
                    gameMenu.add_separator()
                    gameMenu.add_command(label="注销账号", command=say_hi)
                    gameMenu.add_separator()
                    gameMenu.add_command(label="退出游戏", command=exit)
                    menuBar.add_cascade(label="游戏", menu=gameMenu)

                    editMenu = tk.Menu(menuBar, tearoff=0)
                    editMenu.add_command(label="刷新", command=say_hi)
                    editMenu.add_separator()
                    editMenu.add_command(label="游戏设置", command=say_hi)
                    menuBar.add_cascade(label="编辑", menu=editMenu)

                    viewMenu = tk.Menu(menuBar, tearoff=0)
                    viewMenu.add_command(label="TODO", command=say_hi)
                    menuBar.add_cascade(label="视图", menu=viewMenu)

                    toolMenu = tk.Menu(menuBar, tearoff=0)
                    toolMenu.add_command(label="TODO", command=say_hi)
                    menuBar.add_cascade(label="工具", menu=toolMenu)

                    helpMenu = tk.Menu(menuBar, tearoff=0)
                    helpMenu.add_command(label="帮助文档", command=say_hi)
                    helpMenu.add_separator()
                    helpMenu.add_command(label="手册", command=say_hi)
                    helpMenu.add_command(label="教程", command=say_hi)
                    helpMenu.add_separator()
                    helpMenu.add_command(label="检查更新", command=say_hi)
                    helpMenu.add_separator()
                    helpMenu.add_command(label="关于", command=say_hi)
                    menuBar.add_cascade(label="帮助", menu=helpMenu)

                    root.config(menu=menuBar)

                def updateLoadingStatus():
                    root.title('散户王章涵:上海[%s]，深圳[%s]' % (self.shProgress, self.szProgress))
                    if running:
                        root.after(1000, updateLoadingStatus)

                def exit():
                    running = False
                    root.withdraw()
                    time.sleep(2)
                    root.destroy()

                root = tk.Tk()
                root.protocol('WM_DELETE_WINDOW', exit)
                root.title('散户王章涵')
                root.geometry('600x400')
                root.resizable(0,0)
                userName = tk.StringVar()
                password = tk.StringVar()
                repeat = tk.StringVar()
                userEntry = tk.Entry(root, textvariable=userName, justify=tk.CENTER)
                passEntry = tk.Entry(root, textvariable=password, justify=tk.CENTER)
                repeEntry = tk.Entry(root, textvariable=repeat, justify=tk.CENTER)
                loginB = tk.Button(root, text='登录', command=login)
                regisB = tk.Button(root, text='注册', command=regis)
                # gui = GUI(master=root)
                createLoginPage()
                # createMenu()
                updateLoadingStatus()
                root.mainloop()
            GUISpider = threading.Thread(target=showGUI, name='GUI')
            GUISpider.start()

        except Exception as e:
            logging.error(str(e))

if __name__ == '__main__':
    I = app()
