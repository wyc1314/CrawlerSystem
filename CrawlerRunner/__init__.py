#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/24 20:19
# @Author : yingchao.wang
# @describe : 

import os
from configparser import ConfigParser
cf = ConfigParser()
cf.read(os.path.dirname(__file__)+"/config.ini")

# print(os.path.dirname(__file__)+"/config.ini")

# xx = cf.get("MYSQL_SERVER","type")
# print(xx)
# print(type(xx))