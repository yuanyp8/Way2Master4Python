#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      simple_insert_sorting.py
# @Time:      2021/1/29 13:34


def insert2sort(src):
    """实现简单插入排序"""
    for index in range(2, len(src)):
        judge_index = index-1
        sentinel = src[index]
        while src[judge_index] > sentinel:
            src[judge_index] = src[judge_index+1]
            judge_index -= 1
        src[judge_index+1] = sentinel
    return src


print(insert2sort([1, 6, 3, 7, 4, 8]))
