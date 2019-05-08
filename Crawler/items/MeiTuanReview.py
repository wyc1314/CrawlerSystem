
from scrapy.item import Item, Field
# 携程酒店综合评分
class MeiTuanZongHeItem(Item):
    stream_name = "est_server_crawler_data_hotel_analysis_info"
    BIG_DATA_HOTEL_ID = Field()
    SITE_ID=Field()
    RATING_VALUE = Field()
    REVIEW_COUNT = Field()
    CHECK_POINT = Field()
    GUEST_TYPE = Field()