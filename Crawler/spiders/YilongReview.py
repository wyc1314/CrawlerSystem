#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/12 16:31
# @Author : yingchao.wang
# @describe : 


import scrapy,re
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer

# "siteId":"2","reviewId":"264566616","rawReviewContent":"停车和早餐从来都是锦江的亮点！这次继续超赞！"}

class YilongReview(scrapy.Spider):
    name = 'YilongReview'
    allowed_domains = ["*"]
    def __init__(self, *args, **kwargs):
        super(YilongReview, self).__init__(*args, **kwargs)
        self.site_id = kwargs.get("site_id","")
        self.cf = kwargs.get("cf","")



    def start_requests(self):
        self.mysql_client = SQLServer.from_settings(self.settings, self.cf.get("MYSQL_SERVER", "type"),"bigdata")
        sql = "SELECT BIG_DATA_HOTEL_ID,URL_CRAWL_INFO,HOTEL_URL,IS_URL_UPDATE FROM `MS_EST_WH_HOTEL_SITE_REL` WHERE `STATUS`='NORMAL' AND SITE_ID={};".format(self.site_id)
        results = self.mysql_client.select(sql)


    def parse(self, response):
        pass
