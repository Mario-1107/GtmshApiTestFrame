# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:unittetsTest.py
@time:2021/05/20
@describe：
"""
import unittest

#应用unittest框架：必须在类名继承unittest.TestCase
class unittestdemo(unittest.TestCase):

    def test_t1(self):
        print("测试用例1")

    def test_t2(self):
        print("测试用例2")


if __name__ == '__main__':
    unittest.main()