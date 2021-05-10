# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:memberApiTest.py
@time:2021/04/30
@describe：微平台相关接口
"""
import random,string,redis,requests
from Comm.functions import _randoms,_jsonpath,_orderNo
#from Conf.config
class member():
    #生成指定位数随机数
    randoms = _randoms(32)
    #连接本地redis
    conn_redis = redis.Redis(host='localhost',port='6379',db=0)
    #设置URL头部（测试环境）
    sit_url = 'http://km-test.gtmsh.com/WX_Food_Tanyu/'
    #设置URL头部（生产环境）
    prod_url = 'http://wxapi.gtmsh.com/'
    #请求头部信息
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #定义基本属性
    custid = ''
    token = ''

    def __init__(self,custid):
        '''
        构造函数，赋予初始值
        :param custid:品牌码
        '''
        self.custid = custid
        self.token = self.get_redis_token()

    def get_token(self):
        '''
        获取token接口
        :return: 返回token
        '''
        if self.custid == "823882":
            username = 'ThirdWM'
            password = 'ThirdWM003'
        elif self.custid == "823883":
            username = 'SaJiaoSmallAPP'
            password = 'SaJiaoSmallAPP001'
        elif self.custid == "823884":
            username = 'CLYNF'
            password = 'CLYNF123'
        elif self.custid == "823885":
            username = 'gsdx'
            password = 'gsdx123'
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
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
        根据手机号查询会员号
        :param mobile:手机号
        :return:会员号
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'GetVipInfoByTele','random':self.randoms,'token':self.token,'mobile':mobile}
        response = requests.request("POST",url, headers=self.headers, data=payload)
        vipno = _jsonpath(response,'$.data.CardNo')
        return vipno[0]

    def scoreOperate(self,cardnumber,score='1000',type='101'):
        '''
        积分操作接口
        :param cardnumber: 会员号或手机号
        :param score:积分数
        :param type:积分类型
        :return:请求结果
        '''
        #如果传入的是手机号，先调用「根据手机号获取会员」接口获取到会员号
        if len(cardnumber) == 11:
            cardnumber = self.get_VipInfoByTele(cardnumber)
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid': self.custid, 'act': 'ScoreOperate', 'random': self.randoms, 'token':self.token, 'cardnumber': cardnumber,'score': score, 'type': type}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print("操作会员为：%s"%cardnumber+";操作积分数：%s"%score+";接口响应结果："+response.text)

    def vip_FillMoney(self,cardnumber,fillmoney=1000,type=0):
        '''
        会员余额充值
        :param cardnumber: 会员号或手机号
        :param fillmoney:充值金额，默认1000
        :param type:小程序充值 = 0, 外带退款 = 1, 体验官活动 = 2
        :return:请求结果
        '''
        if len(cardnumber) == 11:
            cardnumber = self.get_VipInfoByTele(cardnumber)
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid': self.custid, 'act': 'VipFillMoney', 'random': self.randoms, 'token': self.token, 'cardnumber': cardnumber,'fillmoney': fillmoney, 'transaction_id': self.randoms, 'out_trade_no': self.randoms, 'type': type}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)

    def get_DynamicCode(self,cardnumber):
        '''
        获取会员动态码
        :param cardnumber: 会员号或手机号
        :return:会员动态码
        '''
        if len(cardnumber) == 11:
            cardnumber = self.get_VipInfoByTele(cardnumber)
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid': self.custid, 'act': 'GetDynamicCode', 'random': self.randoms, 'token': self.token,'cardnumber': cardnumber}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        #vipcode = _jsonpath(response,'$.data')
        print(response.text)

    def get_Bills(self,branchno,tableno,unionid='oxvw21QlHBkA289XhFbHIL1MolJw'):
        '''
        拉取账单接口
        :param branchno: 门店编号
        :param tableno:台位号
        :param unionid:用户unionid
        :return:接口返回结果
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid': self.custid, 'act': 'GetBills', 'random': self.randoms, 'token': self.token, 'unionid': unionid,'branchno': branchno, 'tableno': tableno}
        response = requests.request("POST", url, headers=self.headers, data=payload)
        print(response.text)

    def get_BillsByThirdNo(self,branchno,thirdno):
        '''
        拉取账单接口(根据第三方编号)
        :param branchno:门店编号
        :param thirdno:第三方订单编号
        :return:接口返回结果
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'GetBillsByThirdNo','random':self.randoms,'token':self.token,'branchno':branchno,'thirdno':thirdno}
        response = requests.request("POST",url,headers=self.headers,data=payload)
        print(response.text)

    def get_vipinfo(self,unionid='oxvw21QlHBkA289XhFbHIL1MolJw'):
        '''
        获取会员信息
        :param unionid:用户unionid
        :return:接口返回信息
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'GetVipInfo','random':self.randoms,'token':self.token,'unionid':unionid}
        response = requests.request("POST",url,headers=self.headers,data=payload)
        print(response.text)

    def get_AdvancedVipInfo(self,unionid='oxvw21QlHBkA289XhFbHIL1MolJw',type='0'):
        '''
        获取用户高级信息接口
        :param unionid:用户unionid
        :param type:渠道类型:微信=0,美团=1,不传默认为 0
        :return:接口返回结果
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'GetAdvancedVipInfo','random':self.randoms,'token':self.token,'unionid':unionid,'type':type}
        reponse = requests.request("POST",url,headers=self.headers,data=payload)
        print(reponse.text)

    def submitOrderMeal(self,branchno='5999'):
        '''
        点餐/加菜接口
        :param branchno:门店编号
        :param meal:菜品信息：参数为 json
        :return:接口响应内容
        '''
        url = self.sit_url + 'ThirdApiHandler/VipHandler.ashx'
        payload = {'custid':self.custid,'act':'SubmitOrderMeal','random':self.randoms,'token':self.token,'branchno':branchno,'meal':'{"tablenumber":"01","totalprice":101.00,"realprice":101.00,"order_id":'+_orderNo()+',"people":2,"as_cvipno":"990000007052","listmealdetail":[{"nPrc":20,"cfood_c":"18100021","bmainfood":0,"unionid":"oxvw21XMFjq5wOR5JiLeMieBIEBA","suitflag":0,"foodtime":"1","ndisrate":0,"ordernum":"1010000059344-2-1","sMade":"免薄荷叶##191","cfood_n":"半价柠檬冰桔茶","nqty":1,"sunit":"杯","order_id":'+_orderNo()+'},{"nPrc":20,"cfood_c":"10120008","bmainfood":0,"unionid":"oxvw21XMFjq5wOR5JiLeMieBIEBA","suitflag":0,"foodtime":"2","cfood_n":"金针菇","ndisrate":0,"ordernum":"1010000059344-2-2","nqty":1,"sunit":"份","order_id":'+_orderNo()+'},{"nPrc":20,"cfood_c":"10120035","bmainfood":0,"unionid":"oxvw21XMFjq5wOR5JiLeMieBIEBA","suitflag":0,"foodtime":"3","cfood_n":"血旺","ndisrate":0,"ordernum":"1010000059344-2-3","nqty":1,"sunit":"份","order_id":'+_orderNo()+'},{"nPrc":20,"cfood_c":"10110003","bmainfood":0,"unionid":"oxvw21XMFjq5wOR5JiLeMieBIEBA","suitflag":0,"foodtime":"4","ndisrate":0,"ordernum":"1010000059344-2-4-1","sMade":"香辣味+1.00,不加葱加辣##001,059","cfood_n":"大鮰鱼","nqty":1,"order_id":'+_orderNo()+'},{"nPrc":20,"cfood_c":"10120032","bmainfood":0,"unionid":"oxvw21XMFjq5wOR5JiLeMieBIEBA","suitflag":0,"foodtime":"4","cfood_n":"泡饼(辅菜)","ndisrate":0,"ordernum":"1010000059344-2-4-2","nqty":1,"order_id":'+_orderNo()+'}]}'}
        reponse = requests.request('POST',url,headers=self.headers,data=payload)
        print(payload)
        print(reponse.text)