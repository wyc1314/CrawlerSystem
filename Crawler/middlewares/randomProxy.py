# coding:utf8

import json,requests



class RandomProxy(object):
    def process_request(self, request, spider):
        if request.meta.get("is_need_proxy",""):
            ip_port = json.loads(requests.get("http://10.237.1.220:8888/resource?resourceId=1").text).get("IP_PROXY", "")
            if ip_port:
                request.meta['proxy'] = "http://" + ip_port


    # def process_exception(self,request, exception, spider):















# set_ = set()
# while True:
#     ip_port = json.loads(requests.get("http://10.237.1.220:8888/resource?resourceId=1").text).get("IP_PROXY", "")
#     pri
#
#     set_.add(ip_port)
#     print(set_.__len__())