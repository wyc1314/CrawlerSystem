#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 21:43
# @Author : yingchao.wang
# @describe :
import copy

import re,json,time

from scrapy.utils.log import logger

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerSystemUntils.DateFunctions import  getEveryDayTuple
from CrawlerSystemUntils.getCtripEleven import getElevenURL
from CrawlerSystemUntils.CrawlerUntils import classify, extract_re, get_current_ip


class CtripPriceSpider(RedisSpider):
    name = 'CtripPrice'
    allowed_domains = ['hotels.ctrip.com',"*"]
    redis_key = 'CtripPriceSpider:start_urls'
    logger.info("携程价格消费者！")
    def __init__(self, *args, **kwargs):

        super(CtripPriceSpider, self).__init__(*args, **kwargs)
        self.site_id = kwargs["site_id"]
        self.__class__.KinesisQueue = kwargs.get("KinesisQueue","")
        self.cf = kwargs["cf"]
        # self.CHECK_POINT = kwargs["CHECK_POINT"]
        self.__class__.download_delay = kwargs.get("DOWNLOAD_DELAY",1.5)
        self.dateTime = json.loads(kwargs.get("GlobalParams", "")).get("dateTime", 3)


    def parse(self, response):
        item = response.meta.get("item", "")
        eleven_dict = json.loads(response.body.decode())
        eleven = eleven_dict.get("ELEVEN","")
        if eleven:
            check_out_list = getEveryDayTuple(self.dateTime)
            for check_in,check_out in check_out_list:
                header = {"Referer":"http://hotels.ctrip.com/hotel/{hotelId}.html?isFull=F".format(hotelId = item["ctrip_hotel_id"]),"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
                ctrip_price_url = "http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?MasterHotelID={hotelId}&hotel={hotelId}&EDM=F&showspothotel=T&IsDecoupleSpotHotelAndGroup=F&startDate={check_in}&depDate={check_out}&RequestTravelMoney=F&contyped=0&priceInfo=-1&TmFromList=F&eleven={eleven}".format(hotelId = item["ctrip_hotel_id"],check_in=check_in,check_out=check_out,eleven=eleven)
                item["CHECKIN_DATE"] = check_in
                item["CHECKOUT_DATE"] = check_out
                yield Request(url=ctrip_price_url,headers=header,callback=self.get_price,priority=10,meta={"item":copy.deepcopy(item),"is_need_proxy":True})
        else:
            print("没有eleven",eleven_dict)

    def get_price(self,response):
        item = response.meta.get("item")
        # print("neirong:",response.body.decode())
        BLOCK = extract_re(""""html":(.*?)isFullHouse""",response.body.decode())
        RECORDS = re.findall("""room_unfold(.*?)class='clicked hidden""",BLOCK)
        for RECORD in RECORDS:
            # 房型名称
            RoomName = extract_re(r"""RoomName\\":\\"(.*?)\\""",RECORD)
            item["ROOM_TYPE"] = RoomName
            RECORDS2 = re.findall(r"""data-hotelInvoice(.*?class=\\"hotel_room_last\\">.*?<\\/div>)""",RECORD)
            for RECORD2 in RECORDS2:
                itemValue = copy.deepcopy(item)
                # 产品名称
                itemValue["PRODUCT_TYPE"] = extract_re(r"""(room_type_name\\".*?background-image:url\(|room_type_name\\".*?)([^>"]*?)(<br\\/>[^']|\)\\"><|\\/span>|<\\/[es])""",RECORD2,group_num=2)
                # 预定方式
                pay_type = extract_re(r"""payment_txt\\".*?>(.*?)<""",RECORD2)
                map_pay_type = classify({"0": "(在线付)", "2": "(担保)", "1": "(到店付)"}, pay_type)
                itemValue["PAYMENT_TYPE"] = map_pay_type if map_pay_type else "null"
                # 代理
                daili = extract_re(r"""data-role=\\"title\\">(.*?)<\\/span>""", RECORD2)
                itemValue["IS_NOT_AGENT"] = daili if daili else "true"
                # 预订状态
                pay_status = extract_re(r"""btns_base22_main\\">(.*?)<""", RECORD2)
                itemValue["AVAILABLE_ROOM_SITUATION"] = classify({"可预订": "(预订)","满房": "(订完)"}, pay_status)
                # 早餐
                BREAKFAST = extract_re(r"""col4'>(.*?)<""", RECORD2)
                itemValue["BREAKFAST"] = BREAKFAST if BREAKFAST else "null"
                # 原价
                itemValue["ORIGINAL_PRICE"] = extract_re(r"""data-price='(\d+)'""", RECORD2)
                # 套餐价格
                taocan_price = extract_re(r"""rt_origin_price\\"><dfn>&yen;<\\/dfn>(.*?)<""", RECORD2)
                itemValue["DISCOUNT_PRICE"] = taocan_price if taocan_price else "0"
                # 返减
                fanjian = extract_re(r"""span>返现(.*?)<""", RECORD2)
                itemValue["DISCOUNT"] = fanjian if fanjian else "0"
                print(itemValue)
                yield itemValue