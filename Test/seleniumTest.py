# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:seleniumTest.py
@time:2021/05/14
@describe：selenium功能测试
"""
from selenium import webdriver
import time
from Conf.config import sys_cfg

import os
from PIL import ImageGrab,Image
#基础目录
_baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#定义截图文件存放目录，在log目录下建一个Screen目录，按天存放截图
_today = time.strftime("%Y%m%d")
_screen_path = os.path.join(_baseHome,'Log','Screen',_today)
if not os.path.exists(_screen_path):
    os.makedirs(_screen_path)

browser = webdriver.Chrome(r'/Users/air/Desktop/Test/chromedriver')
url = sys_cfg['oa_url']
browser.get(url)
browser.maximize_window()

time.sleep(2)
browser.find_element_by_class_name('tjingtai').click()
browser.find_element_by_id('username').send_keys('V_wuyanwen')
browser.find_element_by_id('pwd').send_keys('GT123')

browser.save_screenshot("{}.png".format(_screen_path)) # 截取整个屏幕并保存
code_element = browser.find_element_by_class_name("yzimg") # 定位到验证码元素
left = code_element.location['x'] # 定位到截图位置
top = code_element.location['y']
right = code_element.size['width'] + left
bottom = code_element.size['height'] + top
im = Image.open("{}.png".format(_screen_path)) # 从文件读取截图，截取验证码位置再次保存
img = im.crop((left, top, right, bottom))
img.save("{}.png".format(_screen_path))

browser.find_element_by_id('login').click()
time.sleep(3)
browser.quit()

# def get_code_image(file_name):
#      driver.save_screenshot(file_name) # 截取整个屏幕并保存
#      code_element = driver.find_element_by_class_name("verify_code_img___1Mei_") # 定位到验证码元素
#      left = code_element.location['x'] # 定位到截图位置
#      top = code_element.location['y']
#      right = code_element.size['width'] + left
#      bottom = code_element.size['height'] + top
#      im = Image.open(file_name) # 从文件读取截图，截取验证码位置再次保存
#      img = im.crop((left, top, right, bottom))
#      img.save(file_name)
#      return file_name