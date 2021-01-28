#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      recursion.py
# @Time:      2021/1/26 14:22


def foo1():
    print('foo1')


def foo2():
    foo3()
    print('foo2')


def foo3():
    print('foo3')


def main():
    print('main start')
    foo1()
    foo2()
    print('main end')


main()