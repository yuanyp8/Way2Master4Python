#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      monkey_peach.py
# @Time:      2021/1/28 11:51

"""
猴子吃桃
"""


def peach1(day=10):
    """公式法"""
    return 1 if day == 1 else 2*(peach1(day-1)+1)


def peach2(day=10, summary=1):
    """循环版"""
    if day == 1:
        return summary
    summary = 2*(summary+1)
    return peach2(day=day-1, summary=summary)
