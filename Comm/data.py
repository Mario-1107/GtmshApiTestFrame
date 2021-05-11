# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:data.py
@time:2021/05/11
@describe：文件读写
"""
import pandas as pd

def read_excel(file,**kwargs):
    '''
    读取Excel内容
    :param file:文件
    :param kwargs:打包关键字参数成dict给函数体调用
    :return:
    '''
    data_dict = []
    try:
        data = pd.read_excel(file,**kwargs)
        data_dict = data.to_dict('records')
    finally:
        return data_dict


# sheet1 = read_excel('baidu_fanyi.xlsx')
# sheet2 = read_excel('baidu_fanyi.xlsx',sheet_name='Sheet2')
# print(sheet1)
# print(sheet2)