#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/25 10:34
# @Author : yingchao.wang
# @describe :

import copy
import json
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from CrawlerSystemUntils.CrawlerUntils import extract_re, classify


class MeiTuanReviewSpider(RedisSpider):
    name = 'MeiTuanReview'
    allowed_domains = ["*"]
    redis_key = 'MeiTuanReviewSpider:start_urls'

    def __init__(self, *args, **kwargs):
        super(MeiTuanReviewSpider, self).__init__(*args, **kwargs)
        self.__class__.KinesisQueue = kwargs.get("KinesisQueue","")
        self.__class__.download_delay = kwargs.get("DOWNLOAD_DELAY", 1.5)
        self.site_id = kwargs["site_id"]
        self.cf = kwargs["cf"]
        self.next_page_num = json.loads(kwargs.get("GlobalParams", "")).get("page", 1)

    def parse(self, response):
        item = response.meta["item"]
        meiTuanZongHeItem = response.meta.get("meiTuanZongHeItem",{})
        html = response.body_as_unicode()
        meiTuanZongHeItem["RATING_VALUE"] = extract_re("""class="score-color">(.*?)</em>""", html)
        meiTuanZongHeItem["REVIEW_COUNT"] = extract_re("""住客点评\((.*?)\)""", html)
        meiTuanZongHeItem["GUEST_TYPE"] = "null"
        yield meiTuanZongHeItem
        for page in range(1, int(self.next_page_num) + 1):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            }
            url = 'http://api.hotel.meituan.com/group/v1/poi/comment/{hotel_id}?sortType=default&noempty=1&withpic=0&filter=all&limit=10&offset={offset}'.format(hotel_id=item["meiTuan_hotel_id"], offset=str((page-1)*10))
            yield Request(url, headers=headers,callback=self.get_review, meta={"item": copy.deepcopy(item), "is_need_proxy": True},dont_filter=True)

    def get_review(self, response):
        res = json.loads(response.body_as_unicode())
        feedbacks = res['data']['feedback']
        for feedback in feedbacks:
            REVIEW_ID = feedback.get("id", "")
            REPLY_REVIEW_TIME = feedback.get('replytime', '')
            REVIEW_RATING_VALUE = feedback.get('score', '')
            ACCOMMODATION_TIME = feedback.get('feedbacktime', '')
            USER_AVATAR = feedback.get('avatar', '')
            REPLY_REVIEW_CONTENT = feedback.get('bizreply', '')
            RAW_REVIEW_CONTENT = feedback.get('comment', '')
            USER_NAME = feedback.get('username', '')
            RAW_PICTURES = ''
            USER_ID = feedback.get('userid', '')
            item = copy.deepcopy(response.meta["item"])
            item['replyReviewTime'] = REPLY_REVIEW_TIME
            item["userName"] = USER_NAME
            item["reviewRatingValue"] = REVIEW_RATING_VALUE
            item["accommodationTime"] = ACCOMMODATION_TIME + " 00:00:00"
            item["replyReviewContent"] = REPLY_REVIEW_CONTENT
            item["reviewId"] = REVIEW_ID
            item["userAvatar"] = USER_AVATAR if USER_AVATAR else ""
            item["isNotReply"] = 'false' if REPLY_REVIEW_CONTENT else 'true'
            item["rawReviewContent"] = RAW_REVIEW_CONTENT
            item["rawPictures"] = RAW_PICTURES if RAW_PICTURES else ""
            item['userId'] = USER_ID
            item["userLocation"] = ""
            item["emotionType"] = classify({"0": "(1|2)", "2": "(3)","1": "(4|5)"}, REVIEW_RATING_VALUE)
            item["sourceSiteId"] = item.get("siteId","6")
            yield item


"""
{"bigDataHotelId":"BIG_DATA_HOTEL_ID","siteId":"SITE_ID","userName":"USER_NAME","userAvatar":"USER_AVATAR","userLocation":"USER_LOCATION",
"reviewId":"REVIEW_ID","rawPictures":"RAW_PICTURES","accommodationTime":"ACCOMMODATION_TIME","replyReviewName":"REPLY_REVIEW_NAME",
"replyReviewTime":"REPLY_REVIEW_TIME","replyReviewContent":"REPLY_REVIEW_CONTENT","reviewRatingValue":"REVIEW_RATING_VALUE",
"isNotReply":"IS_NOT_REPLY","emotionType":"EMOTION_TYPE","rawReviewTitle":"REVIEW_TITLE","rawReviewContent":"RAW_REVIEW_CONTENT","sourceSiteId":"SITE_ID","userId":"USER_ID"}


[{"field":"RECORD.IS_NOT_REPLY","convert_type":"EMPTY2TEXT","convert_rule":"true"},
{"field":"RECORD.USER_AVATAR","convert_type":"TEXT","convert_rule":"w.h:-:100.100"},
{"field":"RECORD.REVIEW_PICTURE","convert_type":"TEXT","convert_rule":"w.h:-:200.150"}]


[{"field":"RECORD.REVIEW_RATING_VALUE","classified_field":"RECORD.EMOTION_TYPE","classifications":[
{"classification_name":"0","classification_rule":"(1|2)"},
{"classification_name":"2","classification_rule":"(3)"},
{"classification_name":"1","classification_rule":"(4|5)"}]}]
"""
