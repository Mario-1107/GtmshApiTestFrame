# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:Key_word_tooler.py
@time:2021/05/14
@describe：
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from Comm.log import log_init
import os, time, logging, datetime
from PIL import ImageGrab, Image

log_init()
logger = logging.getLogger('Mario.selenium')


def open_browser(type_):
    '''
    打开一个指定的浏览器：
    :param type_: 浏览器类型
    :return:
    '''
    # 基于反射的形式来简化代码
    try:
        browser = getattr(webdriver, type_)()
    except Exception as e:
        logger.error(f"打开指定浏览器失败，自动打开谷歌浏览器～错误信息：{e}，")
        browser = webdriver.Chrome(r'/Users/air/Desktop/Test/chromedriver',options=self.options())
    return browser


class KeyWordTooler():
    # 截图文件保存路径:
    # 基础目录
    _baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 定义截图文件存放目录，在log目录下建一个Screen目录，按天存放截图
    _today = time.strftime("%Y%m%d")
    _screen_path = os.path.join(_baseHome, 'Log', 'Screen', _today)
    _image_path = '{0}_{1}.png'.format(_screen_path, str(round(time.time() * 1000)))

    def __init__(self, type_):
        '''
        构造函数
        :param type_: 考虑到不同的driver对象可能是任意一种浏览器
        '''
        # self.browser = webdriver.Chrome(r'/Users/air/Desktop/Test/chromedriver',options=self.options())
        self.browser = open_browser(type_)

    def options(self):
        '''
        ChromeOptions配置
        :return: options
        '''
        # ChromeOptions配置
        options = webdriver.ChromeOptions()
        # 最大化窗口
        options.add_argument('start-fullscreen')
        # 去掉浏览器自动化警告条
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 加载浏览器缓存：/Users/air/Library/Application Support/Google/Chrome/
        options.add_argument(r'--user-data-dir=/Users/air/Library/Application Support/Google/Chrome/')
        # 无界面模式
        #options.add_argument('headless')
        # 隐身模式
        # options.add_argument('incognito')
        # 禁止图片加载
        # options.add_argument('blink-settings=imagesEnabled=false')
        # 关闭密码框
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option('prefs', prefs)

        return options

    def get_image_code(self):
        '''
        验证码截取
        :return:图片路径
        '''
        # 截图整个屏幕并保存
        self.browser.save_screenshot(self._code_image_path)
        # 定位到验证码元素
        code_element = self.browser.find_element_by_class_name("verify_code_img___1Mei_")
        # 定位到截图位置
        left = code_element.location['x']
        top = code_element.location['y']
        right = code_element.location['width'] + left
        bottom = code_element.location['height'] + top
        # 从文件读取截图，截取验证码位置再次保存
        im = Image.open(self._code_image_path)
        img = im.crop((left, top, right, bottom))
        img.save(self._image_path)
        return self._image_path

    def open_url(self, url, doc=''):
        '''
        打开对应网站
        :param url:需要访问的地址
        :return:none
        '''
        logger.info(f"{doc}:正在打开网址:{url}")
        self.browser.get(url)

    def quit_browser(self, doc=''):
        '''
        关闭浏览器
        :return:none
        '''
        logger.info(f"{doc}:正在关闭浏览器～")
        self.browser.quit()

    def wait_element_visible(self, locator, doc='', times=30, poll_frequency=0.5):
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
            # 开始等待时间
            start_time = datetime.datetime.now()
            '''
            https://blog.csdn.net/zyooooxie/article/details/84561783
            visibility_of_element_located():
            判断某个locator元素是否可见。可见代表非隐藏、可显示，并且元素的宽和高都大于0,
            如果定位到就返回WebElement，
            找不到元素 报错Message: no such element: Unable to locate element
            '''
            WebDriverWait(self.browser, times, poll_frequency).until(
                expected_conditions.visibility_of_element_located(locator))
            # 结束等待时间
            end_time = datetime.datetime.now()
            # 求差值，结束减去开始时间，写在日志当中，查看等待了多久（单位转换成秒seconds）
            time_wait = (start_time - end_time).seconds
            # 打印日志
            logger.info(f"{doc}:元素{locator}可见，等待结束。等待开始时间：{start_time},等待结束时间：{end_time}，等待时长为：{time_wait}")
        except:
            # 捕获异常到日志中
            logger.exception("等待可见元素失败～")
            # 截图，一旦元素不可见（失败）就出现截图操作，保存到指定的目录
            self.browser.save_screenshot(self._image_path)
            # 抛出异常
            raise

    def get_element(self, locator, doc=''):
        '''
        查找元素
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param doc:模块名——页面名称——操作名称
        :return:返回查找到的元素
        '''
        logger.info(f"{doc}:查找元素：{locator}")
        try:
            return self.browser.find_element(*locator)
        except:
            logger.exception("查找元素失败！")
            self.browser.save_screenshot(self._image_path)
            raise

    def click_element(self, locator, doc=''):
        '''
        点击元素操作
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param doc:模块名——页面名称——操作名称
        :return:
        '''
        # 找到对应元素
        ele = self.get_element(locator, doc)
        # 元素点击操作
        logger.info(f"{doc}:点击元素：{locator}")
        try:
            ele.click()
        except:
            logger.exception("元素点击操作失败！")
            self.browser.save_screenshot(self._image_path)
            raise

    def input_text(self, locator, text, doc=''):
        '''
        输入操作
        :param locator: 定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param text: 输入内容
        :param doc: 模块名——页面名称——操作名称
        :return:
        '''
        # 找到对应元素
        ele = self.get_element(locator, doc)
        # 输入对应内容
        logger.info(f"{doc}:元素：{locator}输入内容:{text}")
        try:
            ele.send_keys(text)
        except:
            logger.exception("内容输入操作失败！")
            self.browser.save_screenshot(self._image_path)
            raise

    def compulsory_wait(self, times=3, doc=''):
        '''
        页面强制等待
        :param time:等待时间。默认3秒
        :return:none
        '''
        logger.info(f"{doc}:强制等待中，共计{times}秒")
        time.sleep(times)

    def get_element_txt(self, locator, doc=''):
        '''
        获取元素文本内容
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param doc:模块名——页面名称——操作名称
        :return:元素文本内容
        '''
        ele = self.get_element(locator, doc)
        logger.info(f"{doc}:进行获取{locator}元素文本内容操作")
        try:
            return ele.text
        except:
            logger.exception("获取元素文本内容操作失败～")
            self.browser.save_screenshot(self._image_path)
            raise

    def element_clear(self, locator, doc=''):
        '''
        清空元素内容
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param doc:模块名——页面名称——操作名称
        :return:none
        '''
        try:
            self.get_element(locator, doc).clear()
            logger.info(f'{doc}:清空{locator}元素内容')
        except:
            logger.exception("清除元素内容操作失败～")
            self.browser.save_screenshot(self._image_path)
            raise

    def keyboard_keys(self, locator, keys, doc=''):
        '''
        键盘按键操作
        :param locator:定位器，元素定位（元祖类型：元素定位类型，元素定位方式）
        :param keys:需要操作的按键名，大写
        :param doc:模块名——页面名称——操作名称
        :常用按键有：
                BACK_SPACE - 退格按钮
                TAB - Tab 按钮
                SHIFT - Shift 按钮
                ALT - Alt按钮
                SPACE - 空格按钮
                PAGE_UP - 向上翻页按钮
                PAGE_DOWN - 向下翻页按钮
                F12 - 打开控制台
                COMMAND - Win 按钮
        '''
        if keys == 'END':
            self.get_element(locator, doc).send_keys(Keys.END)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'HOME':
            self.get_element(locator, doc).send_keys(Keys.HOME)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'BACK_SPACE':
            self.get_element(locator, doc).send_keys(Keys.BACK_SPACE)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'TAB':
            self.get_element(locator, doc).send_keys(Keys.TAB)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'SHIFT':
            self.get_element(locator, doc).send_keys(Keys.SHIFT)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'ALT':
            self.get_element(locator, doc).send_keys(Keys.ALT)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'SPACE':
            self.get_element(locator, doc).send_keys(Keys.SPACE)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'PAGE_UP':
            self.get_element(locator, doc).send_keys(Keys.PAGE_UP)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'PAGE_DOWN':
            self.get_element(locator, doc).send_keys(Keys.PAGE_DOWN)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'F12':
            self.get_element(locator, doc).send_keys(Keys.F12)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
        elif keys == 'COMMAND':
            self.get_element(locator, doc).send_keys(Keys.COMMAND)
            logger.info(f'{doc}:对页面元素{locator}操作{keys}操作～')
