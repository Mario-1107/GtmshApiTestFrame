# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:test.py
@time:2021/05/08
@describe：
"""
from Test.memberApiTest import member
from Comm.functions import _orderNo
test = member("823882")

test.get_VipIntegralFlowList("18682241673",begindate='2021-05-02')








#for循环两个列表使用zip
# for v,s in zip(vipno,score):
#     test.scoreOperate(v,s,"202104301518411841")

