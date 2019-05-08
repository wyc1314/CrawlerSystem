#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/10 13:53
# @Author : yingchao.wang
# @describe :
import datetime,time

from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerSystemUntils.CrawlerUntils import get_current_ip
from scrapy.crawler import CrawlerProcess

from scrapy.utils.project import get_project_settings
from CrawlerRunner import cf      # 配置文件

def CreateTask(settings,*args,**kwargs):
    mysql_client = SQLServer.from_settings(settings,cf.get("MYSQL_SERVER","type"),db=cf.get("MYSQL_SERVER","db"))
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'Task';"
    column_name_list = [x[0] for x in mysql_client.select(sql)]      # 查询Task表中的所有列名
    sql = "SELECT {} FROM `Task` WHERE NextRunTime<NOW() AND `STATUS`='TEST';".format(",".join(column_name_list))
    site_info_dict_list = []
    for site_info in mysql_client.select(sql):    # 查询所有当前要触发的任务，并转换格式
        item ={}
        for i,x in enumerate(column_name_list):
            item[x] = site_info[i]
        site_info_dict_list.append(item)
    for site_info in site_info_dict_list:
        if get_current_ip() == settings.get("MASTER_HOST", ""):
            sql = "UPDATE Task SET NextRunTime=DATE_ADD(NextRunTime,interval IntervalTime MINUTE) WHERE id = {id}".format(
                id=site_info["ID"])
            mysql_client.execute(sql)
        site_info["cf"] = cf
        site_info["CHECK_POINT"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(site_info)
        settings.set("CONCURRENT_REQUESTS", site_info.get("CONCURRENT_REQUESTS", 16), priority="project")
        crawler_process.crawl(site_info["SpiderName"], **site_info)


if __name__ == '__main__':
    settings = get_project_settings()
    crawler_process = CrawlerProcess(settings)
    CreateTask(settings)
    crawler_process.start()