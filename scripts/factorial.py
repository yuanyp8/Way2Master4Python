#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      factorial.py
# @Time:      2021/1/28 11:19


def factorial(num: int, result=1) -> int:
    """阶乘计算"""
    result = result * num
    return factorial(num-1, result) if num != 1 else result
