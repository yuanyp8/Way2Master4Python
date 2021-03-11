#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      copy_dir.py
# @Time:      2021/3/5 8:08


import random
import shutil
from pathlib import Path
from string import ascii_lowercase


def dir2copy4test(basedir, sub='a/b/c/d', num=50):
    path = Path(basedir)/sub
    path.mkdir(parents=True, exist_ok=True)  # 生成目录
    files = (''.join(random.choices(ascii_lowercase, k=4)) for _ in range(50))  # 获取50个文件名

    for file in files:
        p = Path(basedir) / random.choice([Path(sub)] + list(Path(sub).parents)[:-1]) / file
        p.touch(exist_ok=True)

    def _ignore_file(src, names, exclude=set('xyz')):
        return {name for name in names if name[0] not in exclude and Path(src, name).is_file()}

    shutil.copytree(Path(basedir) / 'a', Path(basedir) / 'dst', ignore=_ignore_file)


dir2copy4test(basedir='D:/test')

