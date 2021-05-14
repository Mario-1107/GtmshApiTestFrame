# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:Screenshot.py
@time:2021/05/14
@describe：截图相关功能
"""
import time,os
from PIL import ImageGrab,Image
#基础目录
_baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#定义截图文件存放目录，在log目录下建一个Screen目录，按天存放截图
_today = time.strftime("%Y%m%d")
_screen_path = os.path.join(_baseHome,'Log','Screen',_today)



def area_screen(x1,y1,x2,y2):
    '''
    指定区域截图
    :param x1:开始截图的x坐标
    :param y1:开始截图的y坐标
    :param x2:结束截图的x坐标
    :param y2:结束截图的y坐标
    :return:none
    '''
    bbox = (x1, y1, x2, y2)
    im = ImageGrab.grab(bbox)
    # 判断文件夹是否存在，不存在就新建一个文件夹
    if not os.path.exists(_screen_path):
        os.makedirs(_screen_path)
    image_name = os.path.join(_screen_path)
    im.save('{0}_{1}.png'.format(image_name,str(round(t * 1000))))

def screen(name):
    '''
    截图
    :param name:
    :return:none
    '''
    t = time.time()
    png = ImageGrab.grab()
    #判断文件夹是否存在，不存在就新建一个文件夹
    if not os.path.exists(_screen_path):
        os.makedirs(_screen_path)
    image_name = os.path.join(_screen_path,name)
    #文件名后面加一个时间戳，避免重名
    png.save('{0}_{1}.png'.format(image_name,str(round(t * 1000))))


