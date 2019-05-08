#!user/bin/env python3
# -*- coding: gbk -*-

import requests,json

from CrawlerSystemUntils.CrawlerUntils import cookieUntils

hotelId = "1519962"
url = "http://172.25.55.170:9002/myweb/getEleven?hotelId={}".format(hotelId)
text = requests.get(url).text
json_data = json.loads(text)
eleven = json_data["ELEVEN"]
hotelnewguid = json_data["hotelnewguid"]
cookie_str = '''hoteluuid=FLPsulDO87oZ2MnZ; fcerror=1048281711; _zQdjfing=1336fa4ea084186ad93a923a3365ac3a923a1336fa3165bb1336fa1336fa;'''


cookie = cookieUntils(cookie_str)
headers = {
    "Referer":"http://hotels.ctrip.com/hotel/{}.html?isFull=F".format(hotelId),
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
hotel_id=hotelId,eleven=eleven
)

cookie["_hotelnewguid"] = hotelnewguid

# url = "https://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=1599982&hotel=1599982&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&currentPage=9&contyped=0&callback=CASwaGVffbjQXgEzk&eleven=658c50ddf3ffcf6a070a303b70d6a975b56ee205aa43913162441aa8eb14e9b2"
# url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID={hotel_id}&hotel={hotel_id}&NewOpenCount=0&AutoExpiredCount=0&RecordCount=1253&OpenDate=2016-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=1&viewVersion=c&currentPage=1&contyped=0&callback=CASwaGVffbjQXgEzk&eleven={eleven}".format(
#     hotel_id=hotel_id,eleven=eleven
# )

text = requests.get(url,headers=headers,cookies=cookie).text
print(text)