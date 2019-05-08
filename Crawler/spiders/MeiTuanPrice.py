#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 21:43
# @Author : yingchao.wang
# @describe :
import copy

import scrapy,json
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerSystemUntils.DateFunctions import  getEveryDayFormatMapTuple
from CrawlerSystemUntils.CrawlerUntils import classify, extract_re, get_current_ip
from scrapy_redis.spiders import RedisSpider


set_ = set()
class MeiTuanPriceSpider(RedisSpider):
    name = 'MeiTuanPrice'
    allowed_domains = ["*"]
    redis_key = 'MeiTuanPriceSpider:start_urls'

    def __init__(self, *args, **kwargs):
        super(MeiTuanPriceSpider, self).__init__(*args, **kwargs)
        self.site_id = kwargs["site_id"]
        self.__class__.KinesisQueue = kwargs.get("KinesisQueue","")
        self.cf = kwargs["cf"]
        self.CHECK_POINT = kwargs["CHECK_POINT"]
        self.__class__.download_delay = kwargs.get("DOWNLOAD_DELAY",1.5)
        self.dateTime = json.loads(kwargs.get("GlobalParams", "")).get("dateTime", 3)


    def start_requests(self):
        if get_current_ip() == self.settings.get("MASTER_HOST", ""):
            self.mysql_client = SQLServer.from_settings(self.settings, self.cf.get("MYSQL_SERVER", "type"),self.cf.get("MYSQL_SERVER", "db"))
            sql = "SELECT BIG_DATA_HOTEL_ID,SITE_ID,URL_CRAWL_INFO FROM `MS_EST_WH_HOTEL_SITE_REL` WHERE `STATUS`='NORMAL' AND SITE_ID={site_id};".format(site_id=self.site_id)
            results = self.mysql_client.select(sql)
            for result in results:
                item = {
                    "hotel_id": extract_re("REGEX_COLUMNS1\":\"(.*?)\"", result[2]),
                    "BIG_DATA_HOTEL_ID": result[0],
                    "SITE_ID": str(result[1]),
                    "CHECK_POINT": self.CHECK_POINT
                }
                dateTime_list = getEveryDayFormatMapTuple(self.dateTime)
                for check_in_info, check_out_info in dateTime_list:
                    itemValue = copy.deepcopy(item)
                    itemValue["CHECKIN_DATE"] = check_in_info[1]
                    itemValue["CHECKOUT_DATE"] = check_out_info[1]
                    url = "http://meituan-549257379.cn-north-1.elb.amazonaws.com.cn:80/get_meituan_price"
                    formdata = {"url_str":"https://ihotel.meituan.com/productapi/v2/prepayList?type=1&utm_medium=PC&version_name=7.3.0&poiId={hotel_id}&start={check_in}&end={check_out}".format(hotel_id=item["hotel_id"],check_in=check_in_info[0],check_out=check_out_info[0])}
                    yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.get_meituan_url,meta={"item":itemValue})
        else:
            print("美团消费者！")

    def get_meituan_url(self,response):
        response_dict = json.loads(response.body_as_unicode())
        url = response_dict.get("url","")
        item = response.meta.get("item",{})
        header = {
            "Referer": "http://hotel.meituan.com/{hotel_id}/".format(hotel_id=item.get("hotel_id","")),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }
        yield scrapy.Request(url=url,headers=header,callback=self.get_meituran_price,priority=10000,dont_filter=True,meta={"item":item},is_need_proxy=True)

    def get_meituran_price(self,response):
        response_dict = json.loads(response.body_as_unicode())
        for RECORD in response_dict.get("mergeList",{}).get("data",{}):
            item = response.meta.get("item")
            set_.add(item["BIG_DATA_HOTEL_ID"])
            print(set_.__len__())
            item["ROOM_TYPE"] = RECORD.get("roomCellName","")
            for RECORD2 in RECORD.get("aggregateGoods",[]):
                itemValue = copy.deepcopy(item)
                # 产品名称
                PRODUCT_TYPE = RECORD2.get("aggregateGoodName","")
                itemValue["PRODUCT_TYPE"] = PRODUCT_TYPE if PRODUCT_TYPE else "null"
                # 预订状态
                pay_status = RECORD2["prepayGood"]["goodsStatus"]
                itemValue["AVAILABLE_ROOM_SITUATION"] = classify({"满房": "(0)", "可预订": "(1)"}, str(pay_status))
                # 早餐
                itemValue["BREAKFAST"] = RECORD2["prepayGood"].get("breakfast","null")
                # 原价
                ORIGINAL_PRICE = RECORD2["prepayGood"]["averagePrice"]
                itemValue["ORIGINAL_PRICE"] = ORIGINAL_PRICE if ORIGINAL_PRICE else ""
                # 代理
                daili = RECORD2["prepayGood"].get("tagName", "")
                itemValue["IS_NOT_AGENT"] = daili if daili else "true"
                # 预定方式
                pay_type = RECORD2.get("prepayGood",{}).get("reserveTips","0")
                itemValue["PAYMENT_TYPE"] = classify({"0": "(在线付)"}, pay_type)
                # 均价（已减）
                itemValue["DISCOUNT_PRICE"] = ORIGINAL_PRICE if ORIGINAL_PRICE else ""
                # 返减
                itemValue["DISCOUNT"] = "0"
                # print(itemValue)
                yield itemValue








        # print(response.body_as_unicode())
        # BLOCK1 = extract_re("""data"(.*?)"giftGoodsIcon""",response.body_as_unicode())
        # RECORDS = re.findall("""\"roomId"(.*?)"unfoldProductCount\"""",BLOCK1)
        # for RECORD in RECORDS:
        #     item = response.meta.get("item")
        #     item["ROOM_TYPE"] = extract_re("""\"roomCellName":"(.*?)\"""", RECORD)
        #     for RECORD2 in re.findall("""aggregateGoodName(.*?)"dealGood":\{.*?\},"selectItemIds\"""",RECORD):
        #         print(RECORD2)
        #         # 产品名称
        #         itemValue = copy.deepcopy(item)
        #         itemValue["PRODUCT_TYPE"] = extract_re("""\"roomName": "(.*?)\"""",RECORD2)
        #         # 代理
        #         daili = extract_re("""\"tagName": "(.*?)\"""", RECORD2)
        #         itemValue["IS_NOT_AGENT"] = daili if daili else "true"
        #         # 早餐
        #         BREAKFAST = extract_re("""\"breakfast": "(.*?)\"""", RECORD2)
        #         itemValue["BREAKFAST"] = BREAKFAST if BREAKFAST else "null"
        #         # 均价（已减）
        #         DISCOUNT_PRICE = extract_re("""lowestOriginalPrice":(.*?),""", RECORD2)
        #         itemValue["DISCOUNT_PRICE"] = DISCOUNT_PRICE if DISCOUNT_PRICE else "0"
        #         # 原价
        #         itemValue["ORIGINAL_PRICE"] = extract_re("""\"originalPrice":(.*?),\"""", RECORD2)
        #         # 返减
        #         DISCOUNT = extract_re("""riceExtInfo":.*?减(.*?)\"""",RECORD2)
        #         itemValue["DISCOUNT"] = DISCOUNT if DISCOUNT else "null"
        #         # 预定方式
        #         pay_type = extract_re("""\"reserveTips":"(.*?)\"""", RECORD2)
        #         map_pay_type = classify({"0": "(在线付)"}, pay_type)
        #         itemValue["PAYMENT_TYPE"] = map_pay_type if map_pay_type else "null"
        #         # # 预订状态
        #         pay_status = extract_re("""\"goodsStatus":(.*?),""", RECORD2)
        #         itemValue["AVAILABLE_ROOM_SITUATION"] = classify({"可预订": "(1)", "满房": "(0)"}, pay_status)
        #         print(itemValue)






