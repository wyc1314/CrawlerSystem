#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 17:24
# @Author : yingchao.wang
# @describe :
import os,sys

# from CrawlerRunner.CrawlerServer import RunCrawlerServer
from scrapy.utils.conf import closest_scrapy_cfg
# def closest_scrapy_cfg(path='.', prevpath=None):
#     """Return the path to the closest scrapy.cfg file by traversing the current
#     directory and its parents
#     """
#     if path == prevpath:
#         return ''
#     # 获得当前目录的绝对路径
#     path = os.path.abspath(path)
#     # 获得当前目录 scrapy.cfg 的绝对路径
#     cfgfile = os.path.join(path, 'scrapy.cfg')
#     if os.path.exists(cfgfile):
#         return cfgfile
#     return closest_scrapy_cfg(os.path.dirname(path), path)

closest = closest_scrapy_cfg()

assert closest
    # TODO 获得项目的绝对目录 ,并加载到环境变量
projdir = os.path.dirname(closest)
sys.path.insert(1,projdir)


import datetime
from CrawlerRunner import cf      # 配置文件
from CrawlerSystemUntils.CrawlerUntils import get_current_ip
from scrapy.utils.project import get_project_settings
from scrapy.log import logger
from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler
from CrawlerProduct.CreateSpiderTask import createSpiderTask
from scrapy.crawler import CrawlerProcess
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer
from CrawlerRunner.CrawlerWeb import app

set_ =set()
def CreateTask(settings,*args,**kwargs):
    mysql_client = SQLServer.from_settings(settings,cf.get("MYSQL_SERVER","type"),db=cf.get("MYSQL_SERVER","db"))
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'CRAWLER_SPIDER_TASK';"
    column_name_list = [x[0] for x in mysql_client.select(sql)]      # 查询Task表中的所有列名
    sql = "SELECT {} FROM `CRAWLER_SPIDER_TASK` WHERE NextRunTime<NOW() AND `STATUS`='NEW';".format(",".join(column_name_list))
    site_info_dict_list = []
    for site_info in mysql_client.select(sql):    # 查询所有当前要触发的任务，并转换格式
        item ={}
        for i,x in enumerate(column_name_list):
            item[x] = site_info[i]
        site_info_dict_list.append(item)

    for site_info in site_info_dict_list:
        sql = "UPDATE CRAWLER_SPIDER_TASK SET NextRunTime=DATE_ADD(NextRunTime,interval IntervalTime MINUTE) WHERE id = {id}".format(id=site_info["ID"])
        mysql_client.execute(sql)
        CHECK_POINT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        createSpiderTask(site_info,settings,CHECK_POINT)
    mysql_client.close()

def runAllSpiderConsume():
    mysql_client = SQLServer.from_settings(settings, cf.get("MYSQL_SERVER", "type"), db=cf.get("MYSQL_SERVER", "db"))
    sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'CRAWLER_SPIDER_TASK';"
    column_name_list = [x[0] for x in mysql_client.select(sql)]  # 查询Task表中的所有列名
    sql = "SELECT {} FROM `CRAWLER_SPIDER_TASK` WHERE isUse=1;".format(",".join(column_name_list))
    site_info_dict_list = []
    for site_info in mysql_client.select(sql):  # 查询所有当前要触发的任务，并转换格式
        item = {}
        for i, x in enumerate(column_name_list):
            item[x] = site_info[i]
        site_info_dict_list.append(item)
    for site_info in site_info_dict_list:
        site_info["cf"] = cf
        settings.set("CONCURRENT_REQUESTS", site_info.get("CONCURRENT_REQUESTS", 16), priority="project")
        crawler_process.crawl(site_info["SpiderName"], **site_info)

if __name__ == '__main__':
    settings = get_project_settings()
    crawler_process = CrawlerProcess(settings)
    Scheduler = TwistedScheduler()
    if get_current_ip() != settings.get("MASTER_HOST", ""):
        runAllSpiderConsume()
    else:
        # RunCrawlerServer()
        Scheduler.add_job(func=CreateTask, trigger='interval', seconds=2, args=(settings,), id='Test')
    Scheduler._logger = logger
    Scheduler.start()
    # app.run(port = 8000)
    reactor.run()
