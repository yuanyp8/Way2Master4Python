#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      format_triangle.py
# @Time:      2021/1/26 23:44

def triangle(n=10):
    for i in range(1, n+1):
        for j in range(n, 0, -1):
            print("{:>{}}".format(
                j,
                len(str(n))),
                end='\n' if j == 1 else " ") if j <= i else print("{}".format(' '*len(str(n))), end=" ")


triangle()