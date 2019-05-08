#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 17:52
# @Author : yingchao.wang
# @describe :
import random

import requests,json

def getCtripEleven(hotel_id):
    while True:
        try:
            response = requests.get("http://internal-spy-onpromise-server-1905722480.cn-north-1.elb.amazonaws.com.cn:8080/myweb/getEleven?hotelId={}".format(hotel_id))
            eleven = json.loads(response)["ELEVEN"]
            break
        except:
            pass
    return eleven


def getElevenURL():
    urlList = [
        "http://172.25.45.227:9002/myweb/getEleven?hotelId={}",
        # "http://172.25.55.169:9002/myweb/getEleven?hotelId={}",
        # "http://172.25.45.228:9002/myweb/getEleven?hotelId={}",
        "http://172.25.55.170:9002/myweb/getEleven?hotelId={}",
    ]
    return random.choice(urlList)




