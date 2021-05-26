# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:Log.py
@time:2021/04/19
@describe：日志处理
"""
import os
import logging
from Conf.config import log_cfg
from logging.handlers import TimedRotatingFileHandler

# 基础目录
_baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 读取log配置
# 日志等级：log_level取过来是个字符串，没法直接用，通过eval执行后，就变成了logging定义的对象
_log_level = eval(log_cfg['log_level'])
_log_path = log_cfg['log_path']  # 日志目录
_log_format = log_cfg['log_format']  # 日志格式
# 日志文件存放路径
_log_file = os.path.join(_baseHome, _log_path, 'log.txt')


# 实现滚动日志
def log_init():
    # 创建日志器
    logger = logging.getLogger('Mario')
    # 设置日志等级
    logger.setLevel(level=_log_level)
    # 设置输入日志格式
    formatter = logging.Formatter(_log_format)
    '''
        handler用于向日志文件打印日志;
        filename:日志文件
        when:切割条件(按周(W)、天(D)、时(H)、分(M)、秒(S)切割)
        interval:间隔(就是几个when切割一次。when是W，interval是3的话就代表3周切割一次)
        backupCount:日志备份数量(就是保留几个日志文件，起过这个数量，就把最早的删除掉，从而滚动删除)
    '''
    handler = TimedRotatingFileHandler(filename=_log_file, when='D', interval=1, backupCount=7)
    # 向日志文件打印日志
    handler.setLevel(_log_level)  # 日志等级
    handler.setFormatter(formatter)  # 日志格式
    logger.addHandler(handler)
    # 向控制台打印日志
    console = logging.StreamHandler()
    console.setLevel(_log_level)
    console.setFormatter(formatter)
    logger.addHandler(console)
