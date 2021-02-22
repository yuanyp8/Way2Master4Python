#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      json2excle.py
# @Time:      2021/2/20 11:20


import xlwt
from pathlib import Path
import json
from datetime import datetime


def getfile(path, mode='r+', encoding='utf-8'):
    fileobj = Path(path)
    with fileobj.open(mode='r+', encoding=encoding) as f:
        return json.load(f)


def dict2xls(srcdate):
    dest = path.cwd()
    time = datetime.now().strftime('%Y-%m-%d')
    date = datetime.now().strftime('%Y-%m-%d-%H-%M')
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(time)
    First = True
    for i, _dict in enumerate(data, start=1):
        for index, (k, v) in enumerate(_dict.items()):
            if First:
                worksheet.write(i-1, index, k)
                worksheet.write(i, index, v)
            if not First:
                worksheet.write(i, index, v)
        First = False
    workbook.save("{}.xls".format(date))  # 保存文件


def filename():
    yield from Path().cwd().rglob('*.json')


for path in filename():
    data = getfile(path=path)
    dict2xls(data)
