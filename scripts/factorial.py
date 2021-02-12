#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      factorial.py
# @Time:      2021/1/28 11:19

from functools import reduce


def factorial(num: int, result=1) -> int:
    """阶乘计算"""
    result = result * num
    return factorial(num-1, result) if num != 1 else result


def reduce_factorial(num: int) -> int:
    """reduce计算方法"""
    return reduce(lambda x, y: x*y, range(1, num+1))
