#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      1.py
# @Time:      2021/1/25 20:17
def foo(a, b=100, *args, c=200, d=['abc']):
    b = 200
    c = 400
    d.append(123)
    print("~~~", a, b, c, d)


print(foo.__defaults__, foo.__kwdefaults__)
foo(5)
print(foo.__defaults__, foo.__kwdefaults__)