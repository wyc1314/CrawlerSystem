
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/4/16 17:54
# @Author : yingchao.wang
# @describe :
import os
from scrapy.utils.conf import closest_scrapy_cfg

# from scrapy.utils.project import get_project_settings
# settings = get_project_settings()
# import os
# print(os.environ)

closest = closest_scrapy_cfg()
# closest = ""
assert closest
    # 获得项目的绝对目录
projdir = os.path.dirname(closest)
print(projdir)



print(os.path.join(projdir,"Crawler\spiders"))
#
# print(settings.copy_to_dict())
