#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 20:12
# @Author : yingchao.wang
# @describe : 


import pymysql
from twisted.enterprise import adbapi
# from ScrapyTest.settings import SQL_SERVER
class MysqlServer(object):
    '''异步方式存入mysql'''
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls,settings,ServerType):
        sql_config = settings.get("MYSQL_SERVER")[ServerType]
        cp = adbapi.ConnectionPool('pymysql', **sql_config)
        return cls(cp)

    def insert(self, sql):  # pipeline默认调用的，进行数据库操作
        """使用twisted将mysql插入变成异步执行"""
        query = self.db_pool.runInteraction(self.__insert, sql)  # 调用插入的方法 Interaction(中文是交互)
        # 处理异常
        query.addErrback(self.handle_error)  # 调用异常处理方法

    @staticmethod
    def handle_error(failure):
        """处理异步插入的异常"""
        print(failure)

    def __insert(self,cursor, item):  # 执行sql语句的方法
        # cursor.execute(sql, params)
        pass

    def select(self,sql,call_back,err_back,*args,**kwargs):
        self.db_pool.runQuery(sql) \
            .addCallback(call_back,*args,**kwargs) \
            .addErrback(err_back)

# def printResult(result):
#     print(result)
# def printError(error):
#     print(error)