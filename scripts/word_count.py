#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      word_count.py
# @Time:      2021/3/5 15:12

from pathlib import Path
from collections import defaultdict


def _make_key(list4src: str, chars=set(r'''!~@#$%^&*(){}[]:-'"/\., ‘“''')):
    """处理split处理后的字符串"""
    # return ''.join([' ' if key in chars else key for key in list4src]).split()
    start = 0
    for index, word in enumerate(list4src):
        if word in chars:
            if start != index:
                yield list4src[start:index]
            start = index+1


def wordcount(filename, method, directory='./', encoding='utf-8') -> defaultdict:
    d = defaultdict(lambda: 0)
    drop_words = {'a', 'is', 'an', 'this', 'that', 'the'}

    try:
        with Path(f"{directory}/{filename}").open(encoding=encoding) as f:
            pass
    except Exception as e:
        print("Error, the given filename:{} or directory:{} were somethings wrong!".format(filename, directory))
    else:
        with Path(f"{directory}/{filename}").open(encoding=encoding) as f:
            for line in f:
                for i in filter(lambda key: key.lower() not in drop_words, method(line)):
                    d[i.lower()] += 1
    return d


def topn(src2dict: set, key, n, reverse=True):
    yield from sorted(src2dict, key=key, reverse=reverse)[:n]


d = wordcount('simple.txt', method=_make_key)
print(*topn(d.items(), lambda x: x[1], 10))

