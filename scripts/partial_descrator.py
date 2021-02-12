#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      partial_decorator.py
# @Time:      2021/2/4 10:04

from functools import partial
from inspect import signature


def add(x, y, z):
    return x + y + z


def newfunc(x, y):
    return partial(add, x, y)


x = newfunc(4, 5)
print(signature(x))
print(x(6))