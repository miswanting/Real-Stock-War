# coding=utf-8
import tkinter as tk
import threading
import time
import os, hashlib, glob, json
import logging
class GUI(object):
    """docstring for GUI"""
    isRunning = True
    root = tk.TK()
    def __init__(self):
        self.log = logging.getLogger('GUI')
        handler = logging.FileHandler('gui.log', 'w')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(relativeCreated)d[%(levelname).4s][%(threadName)-.10s]%(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.root.withdraw()
        self.showLoginPage()
    def showLoginPage(self):
        loginPage = tk.Toplevel()
