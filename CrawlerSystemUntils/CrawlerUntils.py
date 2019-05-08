#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/15 14:35
# @Author : yingchao.wang
# @describe :


import re
def classify(map_list,str):
    # 分类
    for k,v in map_list.items():
        if re.search(v,str):
            return k

def cookieUntils(cookie_str):
    cookie = {}
    for tupe in re.findall("(.*?)=(.*?);", cookie_str):
        k, v = tupe
        cookie[k] = v
    return cookie

def extract_re(expression,str,group_num=1):
    try:
        return re.search(expression, str).group(group_num)
    except:return ""


import socket
def get_current_ip():
    '''获取本机IP'''
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)