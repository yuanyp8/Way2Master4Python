#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      commands_dispatcher.py
# @Time:      2021/2/12 18:28


from functools import wraps
from functools import reduce


def commands_dispatcher():
    """定义一个装饰器，当你定义函数的时候，装饰器会把这个函数放入到字典中"""
    commands = {}

    def reg(name):
        def wrapper(func):
            commands[name] = func
            return func
        return wrapper

    def default_func():
        print('Unknown command')

    def dispatcher():
        while True:
            cmd = input('>>>')
            if cmd.strip() == "":
                continue
            if cmd in ('exit', 'EXIT', 'q', 'Q'):
                break
            commands.get(cmd.strip(), default_func)()

    return reg, dispatcher


# reg, dispatcher = commands_dispatcher()
# @reg('foo1')
# def foo1():
#     print('foo1')
#
# @reg('foo2')
# def foo2():
#     print('foo2')
#
# dispatcher()


def dispatcher4cmd():
    commands = {}

    def reg(name, *args, **kwargs):
        """注册函数，装饰器"""
        @wraps(reg)
        def wrapper(func):
            commands[name] = func, args, kwargs
            return func
        return wrapper

    def default_func():
        print("Unknown Command!")
        return

    def dispatcher():
        while True:
            cmd = input('>>>')
            if not cmd.strip():
                continue
            print(commands)
            func, args, kwargs = commands.get(cmd, (default_func, (), {}))
            func(*args, **kwargs)

    return reg, dispatcher


reg, dispatcher = dispatcher4cmd()


@reg('add1', 1, 2, 3, x=6)
def add1(*args, **kwargs):
    ret = reduce(lambda x, y: x+y, args) + reduce(lambda x, y: x+y, kwargs.values())
    print(ret)
    return ret


@reg('f1', 200, 300)
@reg('f2', 300, 400)
def foo1(x, y):
    print('foo1', x+y)


dispatcher()