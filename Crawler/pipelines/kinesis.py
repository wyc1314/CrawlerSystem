#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/31 20:26
# @Author : yingchao.wang
# @describe : 


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 17:21
# @Author : yingchao.wang
# @describe :
import boto3,time,json

class KinessPipeline(object):
    def __init__(self, client):
        self.client = client

    @classmethod  # 类方法，无需实例化就可以调用
    def from_crawler(cls, crawler):  # 固定写法 scrapy自动调用，用来获取settings.py中的设置
        client = boto3.client('kinesis',region_name='cn-north-1')
        return cls(client)

    def process_item(self, item, spider,streamName =None):
        if not isinstance(item,dict):
            if item.stream_name:
                stream_name = item.stream_name
                item = item._values
        else:
            if spider.KinesisQueue:
                # print(spider.KinesisQueue)
                stream_name = spider.KinesisQueue
            else:
                stream_name=streamName
        self.client.put_record(
            StreamName=stream_name,
            Data=bytes(json.dumps(item,ensure_ascii=False),encoding="utf-8"),
            PartitionKey='0',
            # ExplicitHashKey='string',
            # SequenceNumberForOrdering='string'
        )
        return item


# client =KinessPipeline.from_settings()
# xx = client.getShardIterator()
# while True:
#     for x in xx.__next__():
#         print(x["Data"].decode("utf-8"))
#     time.sleep(1)



# xx = KinessPipeline.from_crawler(crawler=None)
# item = {"reviewRatingValue":"4.44","bigDataHotelId":"1126","entireScore":"0","accommodationTime":"2019-02-28 16:02:03","userName":"31***66","rawPictures":"{\"imgUrls\":[],\"entireScore\":0,\"recommend\":0,\"remark\":\"朋友出游\",\"memberNickName\":\"31***66\",\"content\":\"性价比高，期待下一次\",\"avgScore\":5.0,\"merchantId\":\"1126\",\"imHeadImage\":null,\"imNickName\":null,\"hasReply\":false,\"anonymity\":false,\"merchandiseName\":\"传统大床房\",\"memberId\":\"239456993\",\"childrenEvaluations\":[],\"like\":0,\"display\":true,\"updateTime\":1551340923424,\"evaluationDimensionVOs\":[{\"evaluationType\":1001,\"evaluationName\":\"服务评分\",\"evaluationScore\":5},{\"evaluationType\":1002,\"evaluationName\":\"设备评分\",\"evaluationScore\":5},{\"evaluationType\":1003,\"evaluationName\":\"环境评分\",\"evaluationScore\":5},{\"evaluationType\":1004,\"evaluationName\":\"地理位置评分\",\"evaluationScore\":5}],\"parentId\":null,\"evaluationId\":\"5c77957be4b0af59f730b2c0\",\"merchandiseId\":\"228\",\"memberHeadImage\":\"http:\\/\\/images.plateno.com\\/images\\/avatar\\/14g2R7eMdU\\/320\",\"recommendCount\":0,\"createTime\":1551340923424,\"orderCode\":\"102166053253\",\"memberType\":\"1\",\"merchandiseCode\":null}","isNotReply":"true","emotionType":"1","sourceSiteId":"4","siteId":"4","reviewId":"5c77957be4b0af59f730b2c0","rawReviewContent":"性价比高，期待下一次","guestType":"4"}
# xx.process_item(item,streamName="text_kinesis")
