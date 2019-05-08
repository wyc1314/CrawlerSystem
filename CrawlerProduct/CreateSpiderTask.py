#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/4/23 16:36
# @Author : yingchao.wang
# @describe :
import copy,time
from twisted.internet import task, defer
from Crawler.items.MeiTuanReview import MeiTuanZongHeItem
from Crawler.items.CtripReview import CtripZongHeItem
from scrapy.utils.reactor import CallLaterOnce
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerRunner import cf
from CrawlerSystemConnector.CrawlerSystem_Redis.RedisClient import RedisHelper
from CrawlerSystemUntils.CrawlerUntils import extract_re
from CrawlerSystemUntils.getCtripEleven import getElevenURL
from scrapy import Request

@defer.inlineCallbacks
def CtripPrice(site_info,results,CHECK_POINT):
    rds = RedisHelper()
    try:
        result = next(results)
    except Exception:
        return
    item = {
        "ctrip_hotel_id" : extract_re("REGEX_COLUMNS1\":\"(.*?)\"", result[2]),
        "BIG_DATA_HOTEL_ID" : result[0],
        "SITE_ID" : str(result[1]),
        "CHECK_POINT":CHECK_POINT
    }
    print("CtripPrice", time.time(), item)
    yield rds.lpush(
        key="{}:requests".format(site_info["SpiderName"]),
        request=Request(url=getElevenURL().format(item["ctrip_hotel_id"]),meta={"item":copy.deepcopy(item)},priority=-10,dont_filter=True)
    )

@defer.inlineCallbacks
def CtripReview(site_info,results,CHECK_POINT):
    rds = RedisHelper()
    try:
        result = next(results)
    except Exception:
        return
    item = {
        "ctrip_hotel_id" : extract_re("REGEX_COLUMNS1\":\"(.*?)\"", result[2]),
        "bigDataHotelId" : result[0],
        "siteId" : str(result[1]),
        "CHECK_POINT":CHECK_POINT
    }
    ctripZongHeItem = CtripZongHeItem()
    ctripZongHeItem["BIG_DATA_HOTEL_ID"] = result[0]
    ctripZongHeItem["SITE_ID"] = str(result[1])
    ctripZongHeItem["CHECK_POINT"] = CHECK_POINT
    print("CtripReview",time.time(),item)
    yield rds.lpush(
        key="{}:requests".format(site_info["SpiderName"]),
        request=Request(url=getElevenURL().format(item["ctrip_hotel_id"]),
                        meta={"item":item,"ctripZongHeItem":ctripZongHeItem},priority=-10,dont_filter=True)
    )

@defer.inlineCallbacks
def MeiTuanReview(site_info,results,CHECK_POINT):
    rds = RedisHelper()
    try:
        result = next(results)
    except Exception:
        return
    meiTuanZongHeItem = MeiTuanZongHeItem()
    meiTuanZongHeItem["BIG_DATA_HOTEL_ID"] = result[0]
    meiTuanZongHeItem["SITE_ID"] = str(result[1])
    meiTuanZongHeItem["CHECK_POINT"] = CHECK_POINT
    item = {
        "meiTuan_hotel_id" : extract_re("REGEX_COLUMNS1\":\"(.*?)\"", result[2]),
        "bigDataHotelId" : result[0],
        "siteId" : str(result[1]),
        "CHECK_POINT": CHECK_POINT
    }
    print("MeiTuanReview", time.time(), item)
    url = "http://www.meituan.com/jiudian/{}/#comment".format(item.get("meiTuan_hotel_id",""))
    yield rds.lpush(
        key="{}:requests".format(site_info["SpiderName"]),
        request=Request(url=url,meta={"item":copy.deepcopy(item),"meiTuanZongHeItem":meiTuanZongHeItem,"is_need_proxy":True},priority=-10,dont_filter=True)
    )


def select(settings,SITE_ID):
    # todo 查询所有需要抓取的门店信息
    mysql_client = SQLServer.from_settings(settings, cf.get("MYSQL_SERVER", "type"), "bigdata")
    sql = "SELECT BIG_DATA_HOTEL_ID,SITE_ID,URL_CRAWL_INFO FROM `MS_EST_WH_HOTEL_SITE_REL` WHERE `STATUS`='NORMAL' AND SITE_ID={SITE_ID};".format(SITE_ID=SITE_ID)
    results = mysql_client.select(sql)
    hotel_id = ['WYN5180672', 'WYN5180201', 'WYN5181316', 'WYN5180311', 'WYN5181313', 'WYN5181092', 'WYN5181311', 'WYN5181081', 'WYN5181153', 'WYN5181112', 'WYN5181111', 'WYN5181161', 'WYN5181125', 'WYN5181041', 'WYN5181281', 'WYN5104701', 'WYN5282312', 'WYN5282531', 'WYN5419991', 'WYN5410022', 'WYN5102351', 'WYN5114951', 'WYN4300221', 'WYN5238431', 'WYN5240001', 'WYN4100051', 'WYN5300004', 'WYN0300021', 'WYN3000501', 'WYN7100002', 'WYN2018242', 'WYN2016001', 'WYN2154001', 'WYN2151013', 'WYN2151681', 'WYN3100141', 'WYN3100171', 'WYN3300021', 'WYN2230011', 'WYN3500071', 'WYN2610111', 'WYN2100361', 'WYN2132991']

    results = [x for x in results if x[0] in hotel_id]
    # print(results)
    mysql_client.close()
    return results


def createSpiderTask(site_info,settings,CHECK_POINT):
    results = iter(select(settings,SITE_ID=site_info["site_id"]))
    nextcall = CallLaterOnce(eval(site_info["SpiderName"]),site_info,results,CHECK_POINT)
    heartbeat = task.LoopingCall(nextcall.schedule)
    # TODO delay 秒后开始回调
    nextcall.schedule(delay=0.5)
    TaskTimer = 3
    # TODO 每 TaskTimer秒 产生一次任务
    heartbeat.start(TaskTimer)
