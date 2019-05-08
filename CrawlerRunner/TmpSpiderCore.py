#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from Templates.model import *
from mako.template import Template
import settings




class BaseTemplate(object):
    def __init__(self, template_name, output_name, output_dir):
        self.template = Template(filename=template_name,
                                 output_encoding="utf-8")
        self.output_filename = os.path.join(output_dir, output_name)
    def render(self, *args, **kwargs):
        with open(self.output_filename, "w+") as f:
            f.write(self.template.render(**kwargs).decode())


def generate_crawl_template(project, rule_fields, spider_output_dir,item_output_dir):

    t = BaseTemplate(template_name=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Templates","template.py.tpl"),
                     output_name=project.name + ".py", output_dir=spider_output_dir)
    t.render(**{"rule_fields": rule_fields, "project": project})

    t = BaseTemplate(template_name=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Templates", "items.py.tpl"),
                     output_name = project.name + ".py",
                     output_dir=item_output_dir)
    t.render(**{"rule_fields": rule_fields,"project": project})


def start_project(project, rule_fields, spider_output_dir=settings.OUTPUT_DIR,item_output_dir=settings.ITEM_DIR):
    generate_crawl_template(project, rule_fields, spider_output_dir,item_output_dir)


if __name__ == '__main__':
    projectDict = {'name': 'TaiHe',
               'pipelines': ['JsonWriterPipeline'],
               'download_delay': 1,
               'image_urls': 'image_srcs',
               'images': 'images',
               'spider': Spider({'name': 'TaiHe',
                                 'domain': None,
                                 'download_image': False,
                                 'custom_settings': None,
                                 'start_urls': 'http://music.taihe.com/artist'})
               }
    project = Project(projectDict)
    fields = [Field({'name': 'url', 'path': '//link', 'type': 'str'}),
              Field({'name': 'singerName', 'path': '//ul[@class="container"]//a[contains(@href,"artist")]/@title','type': 'list', 'dup_filter': True})]
    rule = Rule({'rule': 'TaiHe',
                 'fields': fields,
                 "funcName": "parse",
                 'item_name': 'TaiHe',
                 'callback_func': 'parse_item'})
    rule2 = Rule({'rule': 'TaiHe',
                  "funcName":"parse_item",
                 'fields': fields,
                 'item_name': 'TaiHe1',
                 'callback_func': 'parse_item'})
    args = Args({})


    start_project(project, [rule,rule2])
