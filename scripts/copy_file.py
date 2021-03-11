#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      copy_file.py
# @Time:      2021/3/5 7:49


from pathlib import Path


with Path('D:/test/t1.py').open('w+') as f:
    f.writelines('\n'.join([str(i) for i in range(100, 1000) if not i % 5]))


def custom_copy(src, dest, length=16*1024, ):
    with Path(src).open('rb') as f1:
        with Path(dest).open('wb') as f2:
            while True:
                buf = f1.read(length)
                if not buf:
                    break
                f2.write(buf)

