# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:tapdApiTest.py
@time:2021/05/12
@describe：tapd相关
"""
import requests,logging
from Comm.log import log_init
from Conf.config import tapd_cfg
from Comm.functions import _jsonpath
log_init()
logger = logging.getLogger('Mario.tapd')

class tapd_bug_statistics():
    #定义基础属性
    user = tapd_cfg['user']
    password = tapd_cfg['password']
    url = 'https://api.tapd.cn/'
    workspace_id = [61673133]
    def __init__(self):
        pass

    def work_projects(self):
        '''
        获取公司所有项目
        :return:接口响应内容
        '''
        #深圳市甘棠明善餐饮有限公司：22034311。61673133
        url = self.url + 'workspaces/projects?company_id=22034311'
        response = requests.get(url,auth=(self.user,self.password))
        logger.info(response.text)
        data = _jsonpath(response,'$.data')

    def bug_status_distributed(self):
        '''
        缺陷状态分布情况
        :return:
        '''
        url = self.url + 'bugs/group_count?workspace_id='+str(self.workspace_id[0])+'&group_field=status'
        reponse = requests.get(url,auth=(self.user,self.password))
        print(reponse.text)
test = tapd_bug_statistics()
test.bug_status_distributed()