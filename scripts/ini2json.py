#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      ini2json.py
# @Time:      2021/3/8 12:42


from pathlib import Path
from configparser import ConfigParser
import json


def ini2json(src: str):
    cfg = ConfigParser()
    cfg.read(src)
    return {s: dict(cfg.items(s)) for s in cfg.sections()}


def dump2file(src2name: str, src2dict: dict, encoding='utf-8'):
    file = Path(src2name)
    dest_name = file.with_suffix('.json')  # 更换后缀
    with dest_name.open("w+", encoding=encoding) as f:
        json.dump(src2dict, f)


dump2file('./grafana.ini', ini2json('./grafana.ini'))





