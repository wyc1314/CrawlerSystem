#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/4/2 16:58
# @Author : yingchao.wang
# @describe :
import xlrd


# def mapDict():


def readFile(filenames,itemList,sheetName=None):
    '''
    :param filenames: 文件绝对路径
    :param item: 定义item
    :param sheet_name: 要读取的表sheet_name,默认读取全部表
    :return: json类型的数据
    '''
    filenames = filenames.replace("~$","")
    excel = xlrd.open_workbook(filenames)
    sheet_name_list = excel.sheet_names()
    for sheet_name in sheet_name_list:
        key_list = []
        if sheet_name and sheet_name==sheetName:
            table = excel.sheet_by_name(sheet_name)
            for index in range(table.nrows):
                if index==0:
                    key_list = table.row_values(index)
                else:
                    item = {}
                    for i,x in enumerate(table.row_values(index)):

                        item[key_list[i]]  = x
                    itemList.append(item)
    return itemList

itemList = []
# eachFile(r".\酒店各房型最高价汇总",item)
# readFile(r"./Louvre Hotel.xlsx",itemList,sheetName='39家')

