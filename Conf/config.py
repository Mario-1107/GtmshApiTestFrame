# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:config.py
@time:2021/05/10
@describe：读写config.ini文件
"""
import os
from configparser import ConfigParser

#使用相对目录确定文件位置
_conf_dir = os.path.dirname(__file__)
_conf_file = os.path.join(_conf_dir,'config.ini')

#继承ConfigParser，写一个将结果转为dict的方法
#https://www.cnblogs.com/ming5218/p/7965973.html  --ConfigParser常用方法
class MyParser(ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d

#读取所有配置，以字典方式输出结果
def _get_all_conf():
    #引用继承ConfigParser的MyParser类
    _config = MyParser()
    #定义一个空字典装读取后的结果
    result = {}
    #os.path.isfile判断对象是否为文件
    if os.path.isfile(_conf_file):
        try:
            #读写配置文件，并编译为UTF-8
            _config.read(_conf_file,encoding='UTF-8')
            #引用MyParser类的as_dist方法把结果转化为字典类型
            result = _config.as_dict()
        #如果出现OS错误捕获并输出结果
        except OSError:
            raise ValueError('读写文件失败：%s'%OSError)
    return result

#将各配置读取出来，放在变量里面，后续其他文件直接引用这些变量
config = _get_all_conf()
sys_cfg = config['sys']
log_cfg = config['log']
tapd_cfg = config['tapd']
