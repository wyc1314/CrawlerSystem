"""
    Author: YingChao Wang
    Time: 2018/8/3 下午2:24
    TODO:
"""

# -*- coding: utf-8 -*-


from Crawler.items.${project.spider.name} import *
import scrapy

_META_VERSION = 'v1.0'


class ${project.name.capitalize()}Spider(scrapy.Spider):
    name = "${project.spider.name}"
    meta_version = _META_VERSION
    % if project.spider.domain:
    allowed_domains = ${project.domain.split(",")}
    % endif
    start_urls = ${project.spider.start_urls.split(",")}
    % if project.spider.custom_settings:
    custom_settings = project.spider.custom_settings
    % endif

    def __init__(self, *args, **kwargs):
        super(${project.name.capitalize()}Spider, self).__init__(*args, **kwargs)

    % for rule_field in rule_fields:
    % if rule_field.callback_func:
    ## def ${rule_field.callback_func}(self, response):
    def ${rule_field.funcName}(self, response):
        item = ${rule_field.item_name}Item()
        % for field in rule_field.fields:
        % if field.name == "url":
        field = response.url
        % else:
        field = self.get_${field.name}(response)
        % endif
        % if field:
        item['${field.name}'] = field
        % endif
        % endfor
        yield item

    % endif
    % endfor

    % for field in rule_field.fields:
    % if field.name != "url":
    % if project.spider.download_image and field.name == "image_urls":
    def get_${field.name}(self, response):
        ${field.name} = response.xpath('${field.path}').extract()
        return ${field.name} if ${field.name} else []
    % else:
    def get_${field.name}(self, response):
        ${field.name} = response.xpath('${field.path}').extract()
        % if field.type != 'str':
        % if field.dup_filter is True:
        return list(set(${field.name}))
        % else:
        return ${field.name}
        % endif
        % else:
        return ''.join(${field.name}).strip()
        % endif
    % endif
    % endif
    % endfor