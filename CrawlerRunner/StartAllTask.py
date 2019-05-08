#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 17:24
# @Author : yingchao.wang
# @describe :

import datetime

from CrawlerRunner import cf      # 配置文件
from CrawlerSystemUntils.CrawlerUntils import get_current_ip
from scrapy.utils.project import get_project_settings
from scrapy.log import logger
from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler
import time
# from scrapy.crawler import CrawlerProcess
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer

set_ =set()
def CreateTask(settings,*args,**kwargs):
    # print(crawler_process.crawlers)
    mysql_client = SQLServer.from_settings(settings,cf.get("MYSQL_SERVER","type"),db=cf.get("MYSQL_SERVER","db"))
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'Task';"
    column_name_list = [x[0] for x in mysql_client.select(sql)]      # 查询Task表中的所有列名
    sql = "SELECT {} FROM `Task` WHERE NextRunTime<NOW() AND `STATUS`='NEW';".format(",".join(column_name_list))
    site_info_dict_list = []
    for site_info in mysql_client.select(sql):    # 查询所有当前要触发的任务，并转换格式
        item ={}
        for i,x in enumerate(column_name_list):
            item[x] = site_info[i]
        site_info_dict_list.append(item)

    for site_info in site_info_dict_list:
        if site_info["SpiderName"] not in set_:
            if get_current_ip() == settings.get("MASTER_HOST", ""):
                time.sleep(5)
                sql = "UPDATE Task SET NextRunTime=DATE_ADD(NextRunTime,interval IntervalTime MINUTE) WHERE id = {id}".format(id=site_info["ID"])
                mysql_client.execute(sql)
            else:
                set_.add(site_info["SpiderName"])
            site_info["cf"] = cf
            site_info["CHECK_POINT"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            site_info["set_"] = set_
            print(site_info)
            settings.set("CONCURRENT_REQUESTS", site_info.get("CONCURRENT_REQUESTS", 16), priority="project")
            # crawler_process.crawl(site_info["SpiderName"], **site_info)
    mysql_client.close()



if __name__ == '__main__':
    settings = get_project_settings()
    # crawler_process = CrawlerProcess(settings)
    Scheduler = TwistedScheduler()
    # Scheduler.add_job(func=CreateTask, args=(crawler_process,"BaiDu"), trigger='interval', seconds=2, id='BaiDu_task')
    # Scheduler.add_job(func=CreateTask, args=(settings,), trigger='interval', seconds=5, id='Test')
    # Scheduler.add_job(CreateTask, 'date', run_date=datetime.datetime.now()+datetime.timedelta(seconds=2),args=(settings,), id='Test')
    Scheduler.add_job(func=CreateTask, trigger='interval', seconds=2, args=(settings,), id='Test')
    Scheduler._logger = logger
    Scheduler.start()
    reactor.run()
