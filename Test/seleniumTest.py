# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:seleniumTest.py
@time:2021/05/14
@describe：selenium功能测试
"""
import unittest
from Comm.seleniumer import selenium
from Conf.config import sys_cfg
import time
# doc = 'selenium功能测试'
# browser = selenium()
# browser.open_url(sys_cfg['oa_url'],doc)
# browser.wait_element_visible(('xpath','//*[@id="jingtaimima"]/a'),doc)
# browser.click_element(('xpath','//*[@id="jingtaimima"]/a/img'),doc)
# browser.wait_element_visible(('xpath','//*[@id="validateCode"]'),doc)
# browser.input_text(('id','username'),'V_wuyanwen',doc)
# browser.input_text(('id','pwd'),'GT123',doc)
# browser.click_element(('id','login'),doc)
# browser.compulsory_wait(doc=doc)
# browser.quit_browser(doc)

















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