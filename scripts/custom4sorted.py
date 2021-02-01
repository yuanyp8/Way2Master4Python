#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      custom4sorted.py
# @Time:      2021/2/1 9:05

def custom4sort(iterobj, reverse=False, key=None):
    """
    自定义排序算法
    :param iterobj: 传入可迭代对象
    :param reverse: 排序顺序，默认从大到小排序
    :param key: 比较大小的关键字，可传入lambda对象
    :return: 返回一个列表
    """
    ordlist = []
    for src in iterobj:
        src2key = key(src) if key else src

        for index, dest in enumerate(ordlist):
            _ord = src2key < dest if reverse else src2key > dest
            if _ord:
                ordlist.insert(index, src)
                break
        else:
            ordlist.append(src)
    return ordlist


print(custom4sort([2, 5, 6, 1, 5, 9, 4, 3, 2, 7], reverse=True, key=lambda x: 6-x))