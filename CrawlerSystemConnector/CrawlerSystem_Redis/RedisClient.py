#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/21 13:41
# @Author : yingchao.wang
# @describe :
from scrapy.utils.reqser import request_to_dict
from scrapy_redis import picklecompat


def _encode_request(request):
    """Encode a request object"""
    obj = request_to_dict(request)
    serializer = picklecompat
    return serializer.dumps(obj)

import redis
import demjson
from settings import REDIS_HOST,REDIS_PORT,REDIS_PARAMS
class RedisHelper(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PARAMS["password"]):
        self.__redis = redis.StrictRedis(host, port, password=password)
    def get(self):
        data = self.__redis.lpop("CtripPriceSpider:start_urls")
        return data
        # return demjson.decode(data)

    def get_len(self,key):
        lenSnap = self.__redis.llen(key)
        return lenSnap

    def delete(self,key):
        self.__redis.delete(key)

    def lpush(self,key,request):
        self.__redis.lpush(key, _encode_request(request))


    def set(self, value):
        self.__redis.rpush("Snap", value)

    def get_repeat(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key).decode()
        else:
            return ""

    def set_repeat(self, key, value):
        self.__redis.set(key, value,ex=60*60*8)

    def get_snap_violate(self):
        try:
            data = self.__redis.blpop("Snap_Violate",timeout=5)[1].decode()
        except:
            return None
        return demjson.decode(data)

    def get_hotel_info_list(self):
        try:
            data = self.__redis.blpop("excel_list",timeout=2)[1].decode()
        except:
            return None
        return demjson.decode(data)

    def set_hotel_info_list(self,value):
        self.__redis.rpush("excel_list", value)

    def get_hash(self,name):
        try:
            return self.__redis.hget(name=name,key="HotelIdMap").decode()
        except:
            return None

    def set_hash(self,name,value):
        self.__redis.hset(name=name,key="HotelIdMap",value=value)

    def getString(self):
        return self.__redis.get("VerifyFlag").decode()

    def setString(self,value):
        # 状态为 True 时，启动验证
        self.__redis.set("VerifyFlag",value)



rds = RedisHelper()
# print(rds.get_hash("BD0023-2"))
print(rds.get_len("CtripReview:requests"))
print(rds.get_len("CtripPrice:requests"))
print(rds.get_len("MeiTuanReview:requests"))
#
# rds.delete("CtripReview:requests")
# rds.delete("CtripPrice:requests")
# rds.delete("MeiTuanReview:requests")

# print(rds.get_len("CtripReview:requests"))