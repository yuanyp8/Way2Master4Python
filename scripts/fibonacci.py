#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      fibonacci.py
# @Time:      2021/1/23 12:08

"""
简单循环打印斐波那契数列
"""
n = 100
list4fib = [1, 1]

for index in range(2, n):
    list4fib.append(list4fib[index-1] + list4fib[index-2])
    print("The {:>3}'s fib number is {}".format(index+1, list4fib[index]))


"""
递归实现
"""


def fibonacci(num):
    """公式法"""
    return 1 if num < 3 else fibonacci(num-1) + fibonacci(num-2)






