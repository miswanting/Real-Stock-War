# coding=utf-8
import os, glob, threading
import lib_spider.Spider as Spider
import lib_gui.GUI as GUI
class App(object):
    """docstring for App"""
    isRunning = True
    def __init__(self):
        super(App, self).__init__()
        self.clean()
        self.loadConfig()
        self.startSpider()
        self.startGUI()
    def clean(self):
        if not os.path.isdir('log'):
            os.mkdir('log')
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')
        if not os.path.isdir('storage'):
            os.mkdir('storage')
        for file in glob.glob('tmp/*'):
            os.remove(file)
    def loadConfig(self):
        pass
    def hook(self):
        pass
    def star(self):
        pass
    def startSpider(self):
        self.spider = Spider()
        self.spider.start()
    def startGUI(self):
        self.gui = GUI()
        self.gui.start()
if __name__ == '__main__':
    I = App()
