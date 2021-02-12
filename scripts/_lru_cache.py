#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      _lru_cache.py
# @Time:      2021/2/5 0:07


import time
from functools import lru_cache


@lru_cache(maxsize=256)
def add(x, y, z):
    time.sleep(5)
    return x+y+z


print(add(4,5,6))
print(add(4,6,5))
print(add(4,5,6))
print(add(3,5,6))