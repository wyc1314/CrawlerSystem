#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 18:05
# @Author : yingchao.wang
# @describe : 

import boto3,json
# from servers.doRedis import RedisHelper

class SQSClient(object):
    def __init__(self):
        self.client = boto3.client('sqs')
        self.LoginQueueUrl = "https://sqs.cn-north-1.amazonaws.com.cn/006685339268/review-login"
        self.ReplyQueueUrl = "https://sqs.cn-north-1.amazonaws.com.cn/006685339268/review-reply"
        # self.rds = RedisHelper()
    def delete_message(self,Messages,QueueUrl):
        for Message in Messages:
            self.client.delete_message(
                QueueUrl=QueueUrl,
                ReceiptHandle=Message["ReceiptHandle"]
            )
    def receive_message(self,QueueUrl):
        response = self.client.receive_message(
            QueueUrl=QueueUrl,
            AttributeNames=["All"],
        )
        print(response)
        Messages = response.get("Messages","")
        print(Messages)
        # if Messages:
        #     # self.delete_message(Messages,QueueUrl)
        #     for Message in Messages:
        #         for data in json.loads(Message["Body"]):
        #             if QueueUrl.endswith("login"):
        #                 del data["cookie"]
        #                 del data["nextRunTime"]
        #                 print(data)
        #                 self.rds.setLoginTask(data)
        #             elif QueueUrl.endswith("reply"):
        #                 del data["username"]
        #                 del data["password"]
        #                 print(data)
        #                 self.rds.setReplyTask(data)


client = SQSClient()
client.receive_message("https://sqs.cn-north-1.amazonaws.com.cn/006685339268/spy-ctrip")