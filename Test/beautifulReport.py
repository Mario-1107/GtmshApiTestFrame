# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:beautifulReport.py
@time:2021/05/18
@describe：BeautifulReport_test
"""
import unittest
from BeautifulReport import BeautifulReport

if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('/Users/air/PycharmProjects/GtmshApiTestFrame/Test',pattern='seleniumTest.py')
    result = BeautifulReport(test_suite)
    result.report(filename='测试报告',description='测试deresult报告')