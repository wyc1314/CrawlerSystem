#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/15 10:25
# @Author : yingchao.wang
# @describe : 

from CrawlerSystemUntils.CrawlerUntils import extract_re
from CrawlerSystemUntils.getCtripEleven import getElevenURL

class ElevenMiddler(object):
    def process_request(self, request, spider):
        if request.url.__contains__("172.25."):
            hotelId = extract_re("hotelId=(\d+)", request.url)
            request._set_url(getElevenURL().format(hotelId))

    def process_exception(self,request, exception, spider):
        pass


import time,copy

class ElevenServer():
    eleven_set = dict()
    @classmethod
    def get_eleven(cls,key):
        eleven_set_ = copy.copy(cls.eleven_set)
        cls.eleven_set.clear()
        for k,v in eleven_set_.items():
            if time.time() < v["time"]:
                cls.eleven_set[k] = v
        eleven_info = cls.eleven_set.get(key,{})
        if not eleven_info:
            return ""
        else:
            return eleven_info.get("eleven","")

    @classmethod
    def set_eleven(cls,key,eleven,ex=20):
        cls.eleven_set[key] = {"eleven":eleven,"time":int(time.time())+ex}









