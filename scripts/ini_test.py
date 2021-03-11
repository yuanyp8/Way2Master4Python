#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author:    Gavin
# @Email:     GeniusGavin@163.com
# @File:      ini_test.py
# @Time:      2021/3/3 14:50

from pathlib import Path
import configparser


grafana_body = """
    [DEFAULT]
    name = grafana


    [auth.github]
    enabled = false
    allow_sign_up = false
    client_id = some_id
    client_secret = some_secret
    scopes = user:email


    [auth.google]
    enabled = false
    allow_sign_up = false
    client_id = some_client_id
    client_secret = some_client_secret
    scopes = https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email
    auth_url = https://accounts.google.com/o/oauth2/auth
    token_url = https://accounts.google.com/o/oauth2/token
    api_url = https://www.googleapis.com/oauth2/v1/userinfo
    """

p = Path('D:/test/grafana.int')

with p.open('w+') as f:
    f.write(grafana_body)
    f.seek(0)
    f.flush()
    print("grafana.ini", f.read(), "-"*30, sep='\n')

cfg = configparser.ConfigParser()
cfg.read(p)

print("查看缺省sections", cfg.sections(), "-"*30, sep='\n')
print("查看_section", cfg._sections, "-"*30, sep='\n')
print("查看缺省items", cfg.items(), "-"*30, sep='\n')
print("查看auth.google", cfg.items('auth.google'), "-"*30, sep='\n')
print("查看auth.google,覆盖DEFAULT参数", cfg.items('auth.google', vars={'name': 'changed'}), "-"*30, sep='\n')
print("cfg.get()", cfg.get('auth.google', 'enabled'), "-"*30, sep='\n')
print("cfg.get()抑制查不到的报错", cfg.get('auth.google', 'not_found', fallback='Do not care'), "-"*30, sep='\n')
print("设置kv参数", cfg.set('auth.google', 'additions', 'values->additions'))
print("验证设置的参数", cfg.get('auth.google', 'additions'),"-"*30, sep='\n')
with p.open('w+') as f:
    cfg.write(f)
print("增加section", cfg.add_section('add_section'), cfg.sections(), "-"*30, sep='\n')
print("增加kv", cfg.set('add_section', 'new', 'true'), "-"*30, sep='\n')
print("删除section", "-"*30, sep='\n')
if cfg.has_section('add_section'):
    cfg.remove_section('add_section')