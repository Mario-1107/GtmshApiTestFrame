# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:apiTest.py
@time:2021/03/08
@describe：
"""
import requests,jsonpath,json,random,string,redis
from time import *
# 生成32位随机数
randoms = ''.join(random.sample(string.digits + string.ascii_letters,32))
#连接redis
conn_redis = redis.Redis(host='localhost',port='6379',db=0)

#获取品牌token
def gettoken(custid):
    '''
    获取品牌token
    :param custid: 品牌编码
    :return:token
    '''
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
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
    payload = 'custid='+custid+'&act=GetToken&random='+randoms+'&username='+username+'&password='+password
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    responses = json.loads(response.content)
    token = jsonpath.jsonpath(responses,"$.data")
    conn_redis.set('token'+'_'+custid,token[0])
    return token[0]

#获取redis_token
def get_redis_token(custid):
    token = conn_redis.get("token"+'_'+custid).decode("utf-8")
    code = GetDynamicCode(custid,token,"18682241673")
    if code == '0005':
        token = gettoken(custid)
    return token

#会员充值
def VipFillMoney(custid,token,cardnumber,fillmoney="10000",):
    '''
    会员充值
    :param custid: 品牌编码
    :param token:
    :param cardnumber:会员号&手机号
    :param fillmoney:充值金额，默认1000
    :return:充值结果
    '''
    if len(cardnumber) == 11:
       cardnumber=GetVipInfoByTele(custid,cardnumber,token)
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
    #payload = 'custid='+custid+'&act=VipFillMoney&random='+randoms+'&token='+token+'&cardnumber='+cardnumber+'&fillmoney='+fillmoney+'&transaction_id='+randoms+'&out_trade_no='+randoms+'&type=0'
    payload = {'custid':custid,'act':'VipFillMoney','random':randoms,'token':token,'cardnumber':cardnumber,'fillmoney':fillmoney,'transaction_id':randoms,'out_trade_no':randoms,'type':0}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

#根据手机号获取会员接口
def GetVipInfoByTele(custid,mobile,token):
    '''
    根据手机号获取会员接口
    :param custid:品牌编码
    :param mobile:手机号
    :param token:
    :return:会员号
    '''
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
    payload={'custid':custid,'act':'GetVipInfoByTele','random':randoms,'token':token,'mobile':mobile}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    responses = json.loads(response.content)
    vipno = jsonpath.jsonpath(responses,'$.data.CardNo')
    status_code = jsonpath.jsonpath(responses,'$.code')
    if status_code[0] == '0005':
        return status_code[0]
    else:
        return vipno[0]

#积分操作接口
def ScoreOperate(custid,token,cardnumber,score="10000"):
    '''
    积分操作接口
    :param custid: 商户编号
    :param token:
    :param cardnumber:会员号
    :param score:积分数额；默认10000
    :return:接口返回结果
    '''
    if len(cardnumber) == 11:
       cardnumber=GetVipInfoByTele(custid,cardnumber,token)
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
    payload={'custid':custid,'act':'ScoreOperate','random':randoms,'token':token,'cardnumber':cardnumber,'score':score,'type':'101'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

#拉取账单接口
def GetBills(custid,token,branchno,tableno,unionid='oxvw21QlHBkA289XhFbHIL1MolJw'):
    '''
    拉取账单接口
    :param custid:商户编号
    :param token:
    :param branchno:门店号
    :param tableno:台位号
    :param unionid:用户uid；默认自己
    :return:接口返回结果
    '''
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
    payload={'custid':custid,'act':'GetBills','random':randoms,'token':token,'unionid':unionid,'branchno':branchno,'tableno':tableno}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

#外带/餐前付款-退款接口
def WDBackOrder(custid,token,thirdno,branchno,ordertype=1):
    '''
    外带/餐前付款-退款接口
    :param custid: 商户编号
    :param token:
    :param thirdno:订单号
    :param branchno:门店号
    :param ordertype:订单类型 外带 = 1, 餐前付款 = 2;
    :return:接口返回结果
    '''
    url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/WDHandler.ashx"
    payload={'custid':custid,'act':'WDBackOrder','random':randoms,'token':token,'thirdno':thirdno,'branchno':branchno,'ordertype':ordertype}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

#获取会员动态码接口
def GetDynamicCode(custid,token,cardnumber):
    '''
    获取会员动态码接口
    :param custid: 品牌编码
    :param token:
    :param cardnumber:会员卡号
    :return:会员动态码
    '''
    if len(cardnumber) == 11:#如果长度为11位，先调用手机号获取会员接口
        cardnumber = GetVipInfoByTele(custid,cardnumber,token)
        if cardnumber == '0005':
            status_code = cardnumber
            return status_code
        else:
            url = "http://km-test.gtmsh.com/WX_Food_Tanyu/ThirdApiHandler/VipHandler.ashx"
            payload = {'custid':custid,'act':'GetDynamicCode','random':randoms,'token':token,'cardnumber':cardnumber}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.request("POST", url, headers=headers, data=payload)
            responses = json.loads(response.content)
            vipcode = jsonpath.jsonpath(responses,"$.data")
            status_code = jsonpath.jsonpath(responses,"$.code")
            #print("会员动态码为："+vipcode[0])
            return vipcode[0]




