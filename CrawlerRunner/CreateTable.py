from CrawlerRunner import cf
from scrapy.utils.project import get_project_settings
from CrawlerSystemConnector.CrawlerSystem_MySQ.MySqlClient import SQLServer

# 任务表
CreateTaskSQL = """
CREATE TABLE `Task` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `IntervalTime` int(11) NOT NULL DEFAULT '60' COMMENT '分钟',
  `NextRunTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `STATUS` enum('NEW','FROZEN','FINISH','DOING')  DEFAULT 'FROZEN',
  `stage_tree_root_ids` varchar(50)  DEFAULT NULL,
  `global_downloader_params` text ,
  `max_retry_times` int(11) NOT NULL DEFAULT '3',
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
"""
# 配置表
CreateSettingsSql = """
CREATE TABLE `Settings` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TaskId` int(11) ,
  `Key` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Value` text COLLATE utf8mb4_unicode_ci,
  `ValueType` enum('str','int','dict','list','bool','float','NoneType') DEFAULT 'str',
  `STATUS` enum('Develop','Test','Pre-production','Produce')  DEFAULT 'Develop' COMMENT '环境模式',
  `IsUse` TINYINT(1) DEFAULT 1 COMMENT '是否被使用',
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# 规则树
CreateStageTreeSql = """
CREATE TABLE `stage_tree` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `parent_id` int(11) DEFAULT 0,
  `root_id` int(11) NOT NULL,
  `stage_type` enum('NEXT_PAGE','PIPELINE','NORMAL') NOT NULL DEFAULT 'NORMAL' COMMENT '阶段类型',                                                       
  `extract_type` enum('DOMTREE','JSON','JSOUP','XPATH','AUTOMATIC','REGEX') NOT NULL DEFAULT 'REGEX' COMMENT '抽取类型',
  `max_next_page_num` int(11) DEFAULT '100',
  `extract_rule_tree_root_id` int(11) DEFAULT '0',
  `downloader_params` text,
  `IsUse` TINYINT(1) DEFAULT 1 COMMENT '是否被使用',
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30722 DEFAULT CHARSET=utf8;"""


CreateXieChengTableSql = """
CREATE TABLE `stage_tree` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `cityName` varchar(255) DEFAULT NULL,
  `brand` varchar(255) DEFAULT NULL,
  `cityNamePY` varchar(255) DEFAULT NULL,
  `checkIn` varchar(255) DEFAULT NULL,                                                       
  `checkOut` varchar(255) DEFAULT NULL,
  `hotelAmount` varchar(255) DEFAULT NULL,
  `hotelId` varchar(255) DEFAULT NULL,
  `fullname` text,
  `price` varchar(255) DEFAULT NULL,
  `sorceInfo` text,
  `info` text,
  `CREATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UPDATE_TIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30722 DEFAULT CHARSET=utf8;"""

CreateExtractRuleTree = """

"""

if __name__ == '__main__':
    settings = get_project_settings()
    client = SQLServer.from_settings(settings,cf.get("MYSQL_SERVER","type"))
    # client.do_execute(CreateTaskSQL)
    # client.do_execute(CreateSettingsSql)
    client.do_execute(CreateXieChengTableSql)