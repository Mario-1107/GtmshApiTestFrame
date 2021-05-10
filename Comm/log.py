# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:log.py
@time:2021/04/19
@describe：日志处理
"""
import os
import logging
from Conf.config import log_cfg

_baseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
