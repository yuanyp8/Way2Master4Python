#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      list_dir.py
# @Time:      2021/3/1 9:19


from os import path
from pathlib import Path


def list_parents(src: str) -> iter:
    """将指定路径的中的所有父目录都遍历出"""
    ret = []
    pre_path = path.dirname(src)
    while pre_path != src:
        src, pre_path = pre_path, path.dirname(pre_path)
        ret.append(src)
    yield from ret




