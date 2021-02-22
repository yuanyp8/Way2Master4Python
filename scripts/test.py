#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      test.py
# @Time:      2021/2/18 8:41

from functools import reduce
import inspect


def add(*args, a=5, y:int=8):
    return reduce(lambda x, y: x+y, args)


print(add(4,5,6,7, y=9))
sig = inspect.signature(add)
print(sig, sig.parameters, sig.parameters.items(), sig.parameters.values(), sig.parameters.keys())