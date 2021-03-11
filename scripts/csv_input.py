#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      csv_input.py
# @Time:      2021/3/3 9:40


from pathlib import Path
import csv

path = Path('D:/test/test.csv')

csv_body = """\
Name, Age, Sex, Birth, Scool
Gavin, 28, 男, 2021/03/03, 华北电力大学
Xiaoming, 22, 男, 2020/02/02, “清华大学”
"""

with path.open(mode='w+') as f:
    f.write(csv_body)


with path.open() as f:
    body = csv.reader(f)
    for line in body:
        print(line, type(line))


lst = [[i for i in range(20) if i % 2] for _ in range(5)]
with Path('D:/test/t1.csv').open('w+') as f:
    write = csv.writer(f)
    write.writerow(lst)

with Path('D:/test/t2.csv').open('w+', newline='') as f:
    write = csv.writer(f)
    write.writerows(lst)