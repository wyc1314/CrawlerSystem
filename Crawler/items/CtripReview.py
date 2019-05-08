#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/3/25 15:55
# @Author : yingchao.wang
# @describe : 


from scrapy.item import Item, Field


class CtripReviewItem(Item):
    pass


# 携程酒店综合评分
class CtripZongHeItem(Item):
    stream_name = "est_server_crawler_data_hotel_analysis_info"
    BIG_DATA_HOTEL_ID = Field()
    SITE_ID=Field()
    RATING_VALUE = Field()
    REVIEW_COUNT = Field()
    CHECK_POINT = Field()
    GUEST_TYPE = Field()




# CtripZongHeItem_ = CtripZongHeItem()
# CtripZongHeItem_["BIG_DATA_HOTEL_ID"] = "11"
# CtripZongHeItem_["SITE_ID"] = "2"
# CtripZongHeItem_["RATING_VALUE"] = "5"
# CtripZongHeItem_["REVIEW_COUNT"] = "30"
#
# print(CtripZongHeItem_)
# import json
# xx = json.dumps(CtripZongHeItem_._values,ensure_ascii=False)
# print(xx)