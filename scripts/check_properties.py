#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      check_properties.py
# @Time:      2021/2/2 9:17


import functools
import inspect
from inspect import Parameter


def check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        MSG = "Param {} type wrong, except {} but receive {}"
        sig = inspect.signature(func)
        params = sig.parameters

        # 检查位置传参
        for real_value, (arg, value) in zip(args, params.items()):
            if not isinstance(real_value, value.annotation) and value.annotation != inspect._empty:
                raise TypeError(MSG.format(arg, value.annotation, type(real_value)))

        # 检查关键字传参
        for index, value in kwargs.items():
            anno = params[index].annotation
            if not isinstance(value, anno) and anno != inspect._empty:
                raise TypeError(MSG.format(index, anno, type(value)))

        return func(*args, **kwargs)
    return wrapper


@check
def add(x: int, y: int = 6, *args, m, n: int = 7, **kwargs) -> int:
    pass


add(3, 5, 3, 3, 3, m=9, n="s", z=8)
