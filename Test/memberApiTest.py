# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:memberApiTest.py
@time:2021/04/30
@describe：微平台相关接口
"""
import random,string,redis,requests
from Comm.functions import _randoms,_jsonpath
class member():
    #生成指定位数随机数
    randoms = _randoms(32)
    #连接本地redis
    conn_redis = redis.Redis(host='localhost',port='6379',db=0)
    #设置URL头部（测试环境）
    sit_url = 'http://km-test.gtmsh.com/'
    #设置URL头部（生产环境）
    prod_url = 'http://wxapi.gtmsh.com/'
    #请求头部信息
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_token(self,custid):
        if custid == "823882":
            username = 'ThirdWM'
            password = 'ThirdWM003'
        elif custid == "823883":
            username = 'SaJiaoSmallAPP'
            password = 'SaJiaoSmallAPP001'
        elif custid == "823884":
            username = 'CLYNF'
            password = 'CLYNF123'
        elif custid == "823885":
            username = 'gsdx'
            password = 'gsdx123'
        url = self.sit_url + 'WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx'
        payload = 'custid='+custid+'&act=GetToken&random='+self.randoms+'&username='+username+'&password='+password
        response = requests.request('post',url,headers=self.headers,data=payload)
        token = _jsonpath(response,'$.data')
        return token[0]
c = member()
token=c.get_token("823882")
print(token)




