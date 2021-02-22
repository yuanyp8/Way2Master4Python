#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      base64encode.py
# @Time:      2021/2/18 14:07


alphabet = b'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789+/'


def base64encode(src: str):
    if isinstance(src, str):
        _src = src.encode()
    else:
        return
    length = len(_src)
    _bytearray = bytearray()
    for offset in range(0, length, 3):
        triple = _src[offset:offset+3]
        rsize = 3 - len(triple)
        if rsize:
            triple += b'\x00' * rsize
        num = int.from_bytes(triple, 'big') # 3*8 => 4*6
        for i in range(18, -1, -6):
            index = num >> i & 0x3F # 得到的是6位截取数字
            _bytearray.append(alphabet[index])
        if rsize:
            _bytearray[-rsize-1:] = b'='*rsize
    return bytes(_bytearray)


print(base64encode('abcd'))


