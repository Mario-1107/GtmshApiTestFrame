# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:seleniumer.py
@time:2021/05/14
@describe：
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from Comm.log import log_init
import os,time,logging,datetime
from PIL import ImageGrab,Image
log_init()
logger = logging.getLogger('Mario.selenium')
class selenium():
    #截图文件保存路径:
    # 基础目录
    _baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 定义截图文件存放目录，在log目录下建一个Screen目录，按天存放截图
    _today = time.strftime("%Y%m%d")
    _screen_path = os.path.join(_baseHome, 'Log', 'Screen', _today)
    _image_path = '{0}_{1}.png'.format(_screen_path,str(round(time.time() * 1000)))

    def __init__(self):
        self.browser = webdriver.Chrome(r'/Users/air/Desktop/Test/chromedriver')
        self.browser.maximize_window()

    def


    def get_image_code(self):
        '''
        验证码截取
        :return:图片路径
        '''
        #截图整个屏幕并保存
        self.browser.save_screenshot(self._code_image_path)
        #定位到验证码元素
        code_element = self.browser.find_element_by_class_name("verify_code_img___1Mei_")
        #定位到截图位置
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.location['width'] + left
        bottom = code_element.location['height'] + top
        #从文件读取截图，截取验证码位置再次保存
        im = Image.open(self._code_image_path)
        img = im.crop((left,top,right,bottom))
        img.save(self._image_path)
        return self._image_path

    def open_url(self,url):
        '''
        打开对应网站
        :param url:需要访问的地址
        :return:none
        '''
        logger.info(f"正在打开网址:{url}")
        self.browser.get(url)

    def quit_browser(self):
        '''
        关闭浏览器
        :return:none
        '''
        logger.info("正在关闭浏览器～")
        self.browser.quit()

    def wait_element_visible(self,locator,times=30,poll_frequency=0.5,doc=''):
        '''
        等待元素操作
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param times:等待时间上限：默认30秒
        :param poll_frequency:等待周期：默认0.5秒
        :param doc:模块名——页面名称——操作名称
        :return:none
        '''
        logger.info(f"等待元素{locator}可见~")
        try:
            #开始等待时间
            start_time = datetime.datetime.now()
            '''
            https://blog.csdn.net/zyooooxie/article/details/84561783
            visibility_of_element_located():
            判断某个locator元素是否可见。可见代表非隐藏、可显示，并且元素的宽和高都大于0,
            如果定位到就返回WebElement，
            找不到元素 报错Message: no such element: Unable to locate element
            '''
            WebDriverWait(self.browser,times,poll_frequency).until(expected_conditions.visibility_of_element_located(locator))
            #结束等待时间
            end_time = datetime.datetime.now()
            #求差值，结束减去开始时间，写在日志当中，查看等待了多久（单位转换成秒seconds）
            time_wait = (start_time - end_time).seconds
            #打印日志
            logger.info(f"{doc}:元素{locator}可见，等待结束。等待开始时间：{start_time},等待结束时间：{end_time}，等待时长为：{time_wait}")
        except:
            #捕获异常到日志中
            logger.exception("等待可见元素失败～")
            #截图，一旦元素不可见（失败）就出现截图操作，保存到指定的目录
            self.browser.save_screenshot(self._image_path)
            #抛出异常
            raise

    def