#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/2/14 9:53
# @Author : yingchao.wang
# @describe : 



# {"headers":{},"url":"http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=@REGEX_COLUMNS1@&hotel=@REGEX_COLUMNS1@&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&currentPage=1&contyped=0&callback=CASwaGVffbjQXgEzk&eleven=@ELEVEN@","httpHost":"@IP_PROXY@"}

import requests
headers = {
    "Referer":"http://hotels.ctrip.com/hotel/{}.html?isFull=F".format("1564946"),
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=1564946&hotel=1564946&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&currentPage=1&contyped=0&callback=CASwaGVffbjQXgEzk&eleven=a4d3dba70cefd70a99f0661319d93c302482253865f49ae1c0cb471d2750e675"
# url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=1496646&hotel=1496646&NewOpenCount=0&AutoExpiredCount=0&RecordCount=14590&OpenDate=2017-06-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&contyped=0&eleven=4e591154078de88bfe04e129cb96204c4f127f690d533bcddcf30abac1afd2cc&callback=CASGDaKJMBzjSkSIu&_=1550109413011"
text = requests.get(url=url,headers=headers).text
print(text)