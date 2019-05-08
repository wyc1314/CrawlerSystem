#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: Gaomin Wu / wugm@ruyi.ai
    Time: 2018/8/3 下午2:42
    TODO:
"""


class Model(object):
    def __init__(self, attr_values):
        for k, v in attr_values.items():
            self.__setattr__(k, v)


class Project(Model):
    def __init__(self, attr_values):
        super(Project, self).__init__(attr_values)


class Spider(Model):
    def __init__(self, attr_values):
        super(Spider, self).__init__(attr_values)


class Rule(Model):
    def __init__(self, attr_values):
        super(Rule, self).__init__(attr_values)


class Field(Model):
    def __init__(self, attr_values):
        super(Field, self).__init__(attr_values)


class Args(Model):
    def __init__(self, attr_values):
        super(Args, self).__init__(attr_values)