#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 17:21
# @Author : yingchao.wang
# @describe : 
import boto3,time

class KinessPipeline(object):
    def __init__(self, client):
        self.client = client

    @classmethod
    def from_settings(cls):
        client = boto3.client('kinesis',region_name='cn-north-1')
        return cls(client)

    def getShardIterator(self):
        NextShardIterator = None
        # my_stream_name = 'est_server_crawler_data_comment'

        # my_stream_name = 'est_server_crawler_data_hotel_analysis_info'
        my_stream_name = 'est_server_crawler_data_price'
        # my_stream_name = "bigdata_base_price"
        # my_stream_name = "speed-bird-log"
        # my_stream_name = ""
        # my_stream_name = "spiderTextKinesis"
        response = self.client.describe_stream(StreamName=my_stream_name)
        my_shard_id = response['StreamDescription']['Shards'][-1]['ShardId']
        print(my_shard_id)
        ShardIterator = self.client.get_shard_iterator(
            StreamName=my_stream_name,
            ShardId=my_shard_id,
            ShardIteratorType='LATEST',
        )['ShardIterator']
        while True:
            if not NextShardIterator:
                results = self.client.get_records(ShardIterator=ShardIterator,Limit=100)
            else:
                results = self.client.get_records(ShardIterator=NextShardIterator, Limit=100)
            NextShardIterator = results["NextShardIterator"]
            yield results["Records"]


client = KinessPipeline.from_settings()
xx = client.getShardIterator()

import os
f = open(os.path.dirname(__file__)+"/aa.txt","w+")
while True:
    for x in xx.__next__():
        data = x["Data"].decode("utf-8")
        print(data)
        # f.write(x["Data"].decode()+"\r\n")
    time.sleep(1)