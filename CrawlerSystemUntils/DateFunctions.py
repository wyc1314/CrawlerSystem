#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 21:47
# @Author : yingchao.wang
# @describe : 


import datetime,time
def getEveryDay(num,*args):
    '''
        :param num: 间隔的天数
        :param args:年、月、日
        :return 获取一段日期内的所有日期
    '''
    time_list = []
    if args:
        newTime = datetime.datetime(year=args[0],month=args[1],day=args[2])
    else:
        newTime = datetime.datetime.now()
    for i in range(num):
        check_in = newTime + datetime.timedelta(days=i)
        time_list.append(check_in.strftime("%Y-%m-%d"))
    return time_list


def getEveryDayTuple(num,*args):
    '''
        :param num: 间隔的天数
        :param args:年、月、日
        :return 获取一段日期内的所有日期
    '''
    time_list = []
    if args:
        newTime = datetime.datetime(year=args[0],month=args[1],day=args[2])
    else:
        newTime = datetime.datetime.now()
    for i in range(num):
        check_in = newTime + datetime.timedelta(days=i)
        check_out = newTime + datetime.timedelta(days=i+1)
        time_list.append((check_in.strftime("%Y-%m-%d"),check_out.strftime("%Y-%m-%d")))
    # TUDO
    time_list.reverse()
    return time_list

def getEveryDayFormatTuple(num,*args):
    '''
        :param num: 间隔的天数
        :param args:年、月、日
        :return 获取一段日期内的所有日期
    '''
    time_list = []
    if args:
        newTime = datetime.datetime(year=args[0],month=args[1],day=args[2])
    else:
        newTime = datetime.datetime.now()
    for i in range(num):
        check_in = newTime + datetime.timedelta(days=i)
        check_out = newTime + datetime.timedelta(days=i+1)
        time_list.append(
            (
                int(check_in.timestamp()*1000),int(check_out.timestamp()*1000)
            )
        )
    return time_list


def getEveryDayFormatMapTuple(num,*args):
    '''
        :param num: 间隔的天数
        :param args:年、月、日
        :return 获取一段日期内的所有日期
    '''
    time_list = []
    if args:
        newTime = datetime.datetime(year=args[0],month=args[1],day=args[2])
    else:
        newTime = datetime.datetime.now()
    for i in range(num):
        check_in = newTime + datetime.timedelta(days=i)
        check_out = newTime + datetime.timedelta(days=i+1)
        time_list.append(
            (
                (int(check_in.timestamp()*1000),check_in.strftime("%Y-%m-%d")),(int(check_out.timestamp()*1000),check_out.strftime("%Y-%m-%d"))
            )
        )
    return time_list





