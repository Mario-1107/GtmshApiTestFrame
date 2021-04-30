# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:functions.py
@time:2021/04/30
@describe：公用方法
"""
import random,string,jsonpath,json

def _randoms(length):
    '''
    生成指定位数随机数
    :param length:长度
    :return:返回随机数
    '''
    randoms = ''.join(random.sample(string.digits + string.ascii_letters, length))
    return randoms

def _jsonpath(response,value):
    '''
    提取JSON的部分内容
    :param response:内容
    :param value:提取操作符
    :return:提取内容
    '''
    #先把传入的值转换为json格式
    responses = json.loads(response.content)
    #将需要提取的值提取出来
    result = jsonpath.jsonpath(responses,"%s" % value)
    return result

