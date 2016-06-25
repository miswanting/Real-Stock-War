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
        super(GUI, self).__init__()
        self.root.withdraw()
        self.showLoginPage()
    def showLoginPage(self):
        loginPage = tk.Toplevel()
        username
