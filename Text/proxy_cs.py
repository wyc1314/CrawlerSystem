#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/13 19:39
# @Author : yingchao.wang
# @describe : 代理测试


import requests,json
num = 0
set_=set()
while True:
    if num >= 100:
        break
    num +=1
    ip_port = json.loads(requests.get("http://10.237.1.220:8888/resource?resourceId=1").text)["IP_PROXY"]
    set_.add(ip_port)
    # print(ip_port)
    print(set_.__len__())




