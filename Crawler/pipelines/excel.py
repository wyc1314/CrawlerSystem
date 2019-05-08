#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 18:00
# @Author : yingchao.wang
# @describe : 
import xlwt,os

# path = "../.."
# resultPath = os.path.join(os.path.abspath(path), 'CrawlerResults')
# print(resultPath)
# print(os.path.exists(resultPath))

class ExcelPipeline(object):
    def __init__(self,excel_path):
        self.excel = self.write_excel(excel_path)
        self.excel.__next__()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        ProjectName = crawler.spider.name
        return cls(
            # excel_path=crawler.settings["PROJECT_CONF"][ProjectName]["excel_path"],
            excel_path = os.path.join(r"C:\Users\Yingchao.wang\Desktop\Learning\CrawlerSystem\CrawlerResults", ProjectName+".xls")
        )

    def process_item(self, item, spider):
        self.excel.send(item.values())
        return item

    def write_excel(self,path):            # path
        # 创建工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建sheet
        data_sheet = workbook.add_sheet('sheet1')
        # row0 = [u'酒店ID',"BIG_DATA_HOTEL_ID", u'酒店名称', '倒挂产品', '限定最高价',"实际标价","酒店地址","url","抓取时间","入住时间","退房时间"]
        #
        # for j, q in enumerate(row0):
        #     data_sheet.write(0, j, q)
        print(path)
        workbook.save(path)            # 第一次调用，创建文件
        index = 1
        while True:
            record = yield "ok"
            if record == "close":
                workbook.save(path)
                return
            for i,q in enumerate(record):
                data_sheet.write(index, i, str(q))
            index += 1
            workbook.save(path)