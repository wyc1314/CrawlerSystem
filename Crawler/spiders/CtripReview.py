#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/25 10:34
# @Author : yingchao.wang
# @describe :
import copy
import json

import re
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from Crawler.items.CtripReview import CtripZongHeItem
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerSystemUntils.CrawlerUntils import classify, cookieUntils, extract_re, get_current_ip
from CrawlerSystemUntils.getCtripEleven import getElevenURL



class CtripReviewSpider(RedisSpider):
    name = 'CtripReview'
    allowed_domains = ['hotels.ctrip.com',"*"]
    cookie_str = '''hoteluuid=FLPsulDO87oZ2MnZ; fcerror=1048281711; _zQdjfing=1336fa4ea084186ad93a923a3365ac3a923a1336fa3165bb1336fa1336fa;'''
    ELEVEN_CONCURRENT_REQUESTS = 8
    redis_key = 'CtripReviewSpider:start_urls'
    num = 0

    def __init__(self, *args, **kwargs):
        super(CtripReviewSpider, self).__init__(*args, **kwargs)
        self.__class__.KinesisQueue = kwargs.get("KinesisQueue","")
        self.__class__.download_delay = kwargs.get("DOWNLOAD_DELAY", 1.5)
        self.site_id = kwargs["site_id"]
        self.cf = kwargs["cf"]
        self.next_page_num = json.loads(kwargs.get("GlobalParams","")).get("page",1)


    def parse(self, response):
        item = response.meta.get("item", "")
        ctripZongHeItem = response.meta.get("ctripZongHeItem","")
        eleven_dict = json.loads(response.body.decode())
        print(eleven_dict)
        eleven = eleven_dict.get("ELEVEN","")
        hotelnewguid = eleven_dict.get("hotelnewguid","")
        if eleven:
            headers = {
                "Referer": "http://hotels.ctrip.com/hotel/{}.html?isFull=F".format(item["ctrip_hotel_id"]),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
                "Host": "hotels.ctrip.com",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
            }
            url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID={hotel_id}&" \
                  "hotel={hotel_id}&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&" \
                  "card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c" \
                  "&currentPage=1&contyped=0&callback=CASwaGVffbjQXgEzk&eleven={eleven}".format(
                hotel_id=item["ctrip_hotel_id"], eleven=eleven)
            cookie = cookieUntils(self.__class__.cookie_str)
            cookie["_hotelnewguid"] = hotelnewguid
            yield Request(
                url=url,
                headers=headers,
                cookies=cookie,
                callback=self.get_home_review,priority=10+self.__class__.num,
                meta={"item":copy.deepcopy(item),"eleven":eleven,"ctripZongHeItem":ctripZongHeItem,"is_need_proxy":True})
        else:
            print("meiyou eleven")

    def get_home_review(self,response):
        eleven = response.meta["eleven"]
        html = response.body_as_unicode()
        if response.meta.get("page",1) ==1:
            item = response.meta["item"]
            ctripZongHeItem = response.meta["ctripZongHeItem"]
            ctripZongHeItem["RATING_VALUE"] = extract_re("<span class='score'><span class='n'>(.*?)</span>", html)
            ctripZongHeItem["REVIEW_COUNT"] = extract_re("<span id='All_Comment' >全部\((\d+)\)", html)
            ctripZongHeItem["GUEST_TYPE"] = "null"
            print(ctripZongHeItem)
            yield ctripZongHeItem
            for page in range(2, int(self.next_page_num) + 1):
                url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID={hotel_id}&hotel={hotel_id}" \
                      "&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&card=-1&property=-1&userType=-1&" \
                      "productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&currentPage={page}&contyped=0&" \
                      "callback=CASwaGVffbjQXgEzk&eleven={eleven}".format(hotel_id=item["ctrip_hotel_id"], page=page,
                                                                          eleven=eleven)
                yield Request(url, headers=response.request.headers, cookies=response.request.cookies, callback=self.get_home_review, priority=20+self.__class__.num,
                                     meta={"item": copy.deepcopy(item), "page": page, "eleven": eleven,"is_need_proxy":True},
                                     )
        RECORDS = re.findall("class='comment_block J_asyncCmt'(.*?)</div></div></div>",html,re.DOTALL)
        for RECORD in RECORDS:
            item = response.meta["item"]
            USER_NAME = extract_re("class='name'><span>(.*?)</span>", RECORD)
            REVIEW_RATING_VALUE = extract_re("<span class='n'>([0-9]\d*\.?\d*)</span>分", RECORD)
            ACCOMMODATION_TIME = extract_re("class='time'>发表于(.*?)</span>", RECORD)
            RAW_REVIEW_CONTENT = extract_re("class='J_commentDetail'>(.*?)</div>", RECORD)
            REVIEW_ID = extract_re("data-cid='(.*?)'", RECORD)
            USER_AVATAR = extract_re("class='head'.*?img src='(.*?)'", RECORD)
            IS_NOT_REPLY = extract_re("class='htl_reply'.*?class='text.*?>(.*?)</p>",
                                           RECORD) if "false" else "true"  # 1 有回复内容，0没有
            REPLY_REVIEW_CONTENT = extract_re("class='htl_reply'.*?class='text.*?>(.*?)</p>", RECORD)
            RAW_PICTURES = extract_re("class='comment_pic'(.*?)class='comment_bar'", RECORD)
            sourceSiteId = classify({"7": "(艺龙网用户)", "1": "(去哪儿网用户)", "2": "(.+)"}, USER_NAME)
            item["userName"] = USER_NAME
            item["reviewRatingValue"] = REVIEW_RATING_VALUE
            item["accommodationTime"] = ACCOMMODATION_TIME + " 00:00:00"
            item["replyReviewContent"] = REPLY_REVIEW_CONTENT
            item["reviewId"] = REVIEW_ID
            item["userAvatar"] = USER_AVATAR
            item["isNotReply"] = "false" if IS_NOT_REPLY else "true"
            item["rawReviewContent"] = RAW_REVIEW_CONTENT
            item["RAW_PICTURES"] = RAW_PICTURES
            EMOTION_TYPE = classify(
                {"0": "(1\\.|2\\.|3\\.0|3\\.1|3\\.2|3\\.3|3\\.4)", "2": "(3\\.5|3\\.6|3\\.7|3\\.8|3\\.9)",
                 "1": "(^4$|5|4\\.)"}, REVIEW_RATING_VALUE)
            item["emotionType"] = EMOTION_TYPE
            item["sourceSiteId"] = sourceSiteId
            print(item)
            yield item