#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      prime_number.py
# @Time:      2021/1/23 17:36


"""
计算给定范围内的素数
"""

n, count = 1000, 2
list4prime = [2]

for index in range(3, n, 2):
    flag, num2middle = False, index**0.5
    for prime in list4prime:

        if not index % prime:
            break
        if prime > num2middle:
            flag = True
            break

    if flag:
        list4prime.append(index)
print(*list4prime)