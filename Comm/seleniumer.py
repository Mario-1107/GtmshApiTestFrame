# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:seleniumer.py
@time:2021/05/14
@describe：
"""
from selenium import webdriver
import os,time
class selenium():
    #截图文件保存路径:
    # 基础目录
    _baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 定义截图文件存放目录，在log目录下建一个Screen目录，按天存放截图
    _today = time.strftime("%Y%m%d")
    _screen_path = os.path.join(_baseHome, 'Log', 'Screen', _today)
    _code_image = '{0}_{1}.png'.format(_screen_path,str(round(time.time() * 1000)))
    def __init__(self):
        self.browser = webdriver.Chrome(r'/Users/air/Desktop/Test/chromedriver')
        self.browser.maximize_window()

    def get_image_code(self):
        self.browser.save_screenshot(self._code_image)




