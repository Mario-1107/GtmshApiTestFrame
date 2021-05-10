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
    #定义基本属性
    custid = ''
    token = ''
    def __init__(self,custid):
        self.custid = custid
        self.token = self.get_redis_token()


    def get_token(self):
        '''
        获取token接口
        :return: 返回token
        '''
        if self.custid == "823882":
            username = 'shangyou'
            password = 'gtmsh123@..'
        elif self.custid == "823883":
            username = 'SaJiaoSmallAPP'
            password = 'SaJiaoSmallAPP001'
        elif self.custid == "823884":
            username = 'CLYNF'
            password = 'CLYNF123'
        elif self.custid == "823885":
            username = 'gsdx'
            password = 'gsdx123'
        url = self.prod_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = 'custid='+self.custid+'&act=GetToken&random='+self.randoms+'&username='+username+'&password='+password
        response = requests.request('post',url,headers=self.headers,data=payload)
        token = _jsonpath(response,'$.data')
        try:
            # 把获取到的token存入redis
            self.conn_redis.set('token'+'_'+self.custid,token[0])
            # 把存入redis的token设置失效时间
            self.conn_redis.expire('token'+'_'+self.custid,6600)
        except:
            print("插入redis失败")
        return token[0]

    def get_redis_token(self):
        '''
        获取redis token
        :param custid:品牌码
        :return:返回token
        '''
        try:
            token = self.conn_redis.get("token"+"_"+self.custid).decode("utf-8")
        except:
            #如果出现错误重新获取token
            token = self.get_token()
        return token

    def get_VipInfoByTele(self,mobile):
        '''
        根据手机号获取会员
        :param custid:品牌号
        :param token:
        :param mobile:手机号
        :return:会员号
        '''
        url = self.sit_url + 'WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'GetVipInfoByTele','random':self.randoms,'token':self.token,'mobile':mobile}
        response = requests.request("POST",url, headers=self.headers, data=payload)
        vipno = _jsonpath(response,'$.data.CardNo')
        return vipno[0]

    def scoreOperate(self,cardnumber,score='1000',type='101'):
        '''
        积分操作接口
        :param cardnumber:会员号
        :param score:积分值
        :return:接口请求结果
        '''
        #如果传入的是手机号，先调用「根据手机号获取会员」接口获取到会员号
        if len(cardnumber) == 11:
            cardnumber = self.get_VipInfoByTele(cardnumber)
        url = self.prod_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid': self.custid, 'act': 'ScoreOperate', 'random': self.randoms, 'token':self.token, 'cardnumber': cardnumber,'score': score, 'type': type}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print("操作会员为：%s"%cardnumber+";操作积分数：%s"%score+";接口响应结果："+response.text)

# c = member('823882')
# vipno = c.scoreOperate("18682241673","-1000")




