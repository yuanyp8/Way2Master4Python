#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      custom_ls.py
# @Time:      2021/3/9 8:50


from pathlib import Path
import datetime
import argparse
import stat
import os



parse = argparse.ArgumentParser(prog='pls', description="List all files and directory", add_help=False)

parse.add_argument('-l', action='store_true', help='use a long listing format')
parse.add_argument('dir', nargs='?', default='./', help="give the directory what you want to list")
parse.add_argument('-a', '--all', action='store_true', help='show all list above Hidden files')
parse.add_argument('-h', '--human-readable', action='store_true', dest='h',
                   help='print sizes in human readable format(e.g.,1K,234M,2G)')

args = parse.parse_args()


def _getfiletype(p: Path):
    if p.is_dir():
        return 'd'
    elif p.is_fifo():
        return 'f'
    elif p.is_socket():
        return 's'
    elif p.is_block_device():
        return 'b'
    elif p.is_symlink():
        return 'l'
    elif p.is_char_device():
        return 'c'
    else:
        return '-'


def timestamp2time(stamp, timezone=datetime.timezone.utc, strf="%b-%d %H:%M:%S"):
    """reverse timestamp to datetime"""
    return datetime.datetime.fromtimestamp(stamp, tz=timezone).strftime(strf)


def _getmode1(_stat, defaultstr='rwxrwxrwx'):
    """利用字符串format方法实现获取权限字符串"""
    mode, modestr = _stat.st_mode, ''
    for i, j in enumerate("{:09b}".format(mode)[-9:]):
        modestr += defaultstr[i] if j == '1' else '-'
    return modestr


def _getmode2(_stat, defaultstr='rwxrwxrwx'):
    """利用移位计算方法获取权限字符串"""
    mode, modestr = _stat.st_mode, ''
    for i in range(8, -1, -1):
        modestr += defaultstr[8-i] if mode >> i & 1 else '-'
        return modestr


def _getsize(_stat, unitset=('',  'KB', 'MB', 'GB', 'TB')):
    """获取文件大小"""
    count, size = 0, _stat.st_size
    length = len(unitset)
    while size >= 1000 and count + 1 < length:
        size /= 1000
        count += 1
    return f"{size:.01f}{unitset[count]}"


def _out4fmt(fp: Path, hide):
    """整合输出模式"""
    sys4type = False if os.name == 'nt' else True
    _stat = fp.stat()
    atime = timestamp2time(_stat.st_atime)
    ctime = timestamp2time(_stat.st_ctime)
    mtime = timestamp2time(_stat.st_mtime)
    _type = _getfiletype(fp)
    _mode = _getmode1(_stat)
    _size = _getsize(_stat) if hide else _stat.st_size
    _nlink = _stat.st_nlink
    _own = fp.owner() if sys4type else '-'
    _group = fp.group() if sys4type else '-'
    return "{}{} {} {} {} {}  {}  {}".format(_type, _mode, _nlink, _own, _group,  _size, mtime, fp.name)


def listdir(path, detail=False, hide=True):
    p = Path(path)
    ret = []
    for f in p.iterdir():
        # _mode = stat.filemode(f.stat().st_mode)  #  可实现f"{_type}{_mode}"
        if not hide and f.name.startswith('.'):
            continue
        if not detail:
            yield f.name
        else:
            yield _out4fmt(f, hide)


print(*listdir(path=args.dir, detail=args.l, hide=args.h), sep='\n\n')


