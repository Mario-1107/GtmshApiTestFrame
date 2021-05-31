# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:seleniumTest.py
@time:2021/05/14
@describe：selenium功能测试
"""
import unittest
from Comm.Key_word_tooler import KeyWordTooler
from Conf.config import sys_cfg
import time


class backstageTest():
    def modify_StoreInfo(self, custid, branchno):
        '''
        修改门店经纬度
        :param custid: 品牌
        :return:
        '''
        doc = '运营_门店管理_修改门店经纬度'
        browser = KeyWordTooler()
        # 登录餐饮中台
        browser.open_url(sys_cfg['oa_url'], doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(3, doc=doc)
        # 定位并点击到运营模块
        browser.click_element(('xpath', '//span[text()="运营"]'), doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(1, doc=doc)
        # 定位并点击门店管理
        browser.click_element(('xpath', '//*[@id="root"]/div/aside/div[2]/div/a[3]/span'), doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(1, doc=doc)
        # 根据用户调用修改门店坐标
        browser.click_element(('xpath', f'//span[text()="{custid}"]'), doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(1, doc=doc)
        # 输入门店编码
        browser.input_text(('id', 'kmShopCode'), text=branchno, doc=doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(2, doc=doc)
        # 点击筛选按钮
        browser.click_element(('xpath',
                               '//*[@id="root"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[2]/div/form/div/div[5]/button[1]'),
                              doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(1, doc=doc)
        # 点击编辑按钮
        browser.click_element(('xpath', ' //a[text()="编辑"]'), doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(1, doc=doc)
        # 输入经纬度
        browser.element_clear(('id', 'longitude'), doc)
        browser.input_text(('id', 'longitude'), '113.940887', doc)
        browser.element_clear(('id', 'latitude'), doc)
        browser.input_text(('id', 'latitude'), '22.506521', doc)
        browser.keyboard_keys(('id', 'address'), 'END', doc)
        # 点击保存按钮
        browser.click_element(('xpath', '//*[@id="root"]/div/div/div[2]/div[1]/div/div[2]/div/form/div[46]/button[1]'),
                              doc)
        # 退出浏览器
        browser.compulsory_wait(10, doc=doc)
        browser.quit_browser(doc)

    def loging_(self):
        '''
        登录模块
        :return:
        '''
        doc = '首页-登录'
        browser = KeyWordTooler()
        # 登录餐饮中台
        browser.open_url(sys_cfg['oa_url'], doc)
        # 强制等待，等待页面元素加载完成
        browser.compulsory_wait(3, doc=doc)
        #点击二维码选择手动登录
        browser.click_element(('xpath','//*[@id="jingtaimima"]/a'),doc)
        #输入账号密码
        browser.input_text(('id','username'),'V_wuyanwen',doc)
        browser.input_text(('id','pwd'),'GT123',doc)
        browser.compulsory_wait(3,doc)
        #截取验证码
        img_code = browser.get_image_code()
        print(img_code)


        # 退出浏览器
        browser.compulsory_wait(3, doc=doc)
        browser.quit_browser(doc)








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
