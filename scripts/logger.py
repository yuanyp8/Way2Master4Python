#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      logger.py
# @Time:      2021/2/1 14:38


import datetime
import time
from functools import update_wrapper
from functools import wraps


def update_properties(src):
    def _update(dest):
        dest.__name__ = src.__name__
        dest.__doc__ = src.__doc__
        return dest
    return _update


def logger(func):
    """log function"""
    # @update_properties(func)
    @wraps(func)  # wraps替代update_wrapper, wraps 利用偏函数包裹update_wrapper
    def wrapper(*args, **kwargs):
        """wrapper function"""

        print("Start the Function: {}".format(func))
        start = datetime.datetime.now()

        ret = func(*args, **kwargs)
        delta = (datetime.datetime.now() - start).total_seconds()
        print("The function: {} took {:.2f}s".format(func, delta))

        return ret
    # update_wrapper(wrapper=wrapper, wrapped=func)   # 替代update_properties
    return wrapper


@logger  # add = logger(add) => add =  wrapper
def add(x, y):
    """add function"""
    time.sleep(3)
    return x + y


print(add.__doc__, add.__name__)
