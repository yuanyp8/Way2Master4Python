#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      gen_counter.py
# @Time:      2021/1/26 22:55

"""
循环计数器，带传入控制参数功能
"""

def counter():
    def wrapper():
        count = 0
        while True:
            count += 1
            response = yield count
            if isinstance(response, int):
                count = response
    c = wrapper()
    return lambda x=False: next(c) if not x else c.send(x)


gen = counter()
print(gen())
print(gen())
print(gen(-1))