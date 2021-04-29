# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:PushMsg.py
@time:2021/04/19
@describe：推送消息
"""
import requests
class workweixin_push_msg:
    #定义基础属性
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    get_response = requests.get()

    def gettoken(self):

