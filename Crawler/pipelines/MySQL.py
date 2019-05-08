import pymysql
from twisted.enterprise import adbapi
# from ScrapyTest.settings import SQL_SERVER
class MysqlTwistedPipeline(object):
    '''异步方式存入mysql'''
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod # 类方法，无需实例化就可以调用
    def from_crawler(cls,crawler): # 固定写法 scrapy自动调用，用来获取settings.py中的设置
        ProjectName = crawler.spider.name
        SQLServerType = crawler.settings["PROJECT_CONF"][ProjectName]["SQLServer"]
        dbparms = dict(
            host=crawler.settings["SQL_SERVER"][SQLServerType]["host"],
            user=crawler.settings["SQL_SERVER"][SQLServerType]["user"],
            passwd=crawler.settings["SQL_SERVER"][SQLServerType]["passwd"],
            db=crawler.settings["SQL_SERVER"][SQLServerType]["db"],
            port=crawler.settings["SQL_SERVER"][SQLServerType]["port"],
            charset=crawler.settings["SQL_SERVER"][SQLServerType]["charset"],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 链接池 , **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        db_pool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(db_pool)

    def process_item(self, item, spider):  # pipeline默认调用的，进行数据库操作
        """使用twisted将mysql插入变成异步执行"""
        query = self.db_pool.runInteraction(self.__insert, item)  # 调用插入的方法 Interaction(中文是交互)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)  # 调用异常处理方法
        return item

    @staticmethod
    def handle_error(failure, item, spider):
        """处理异步插入的异常"""
        print(failure)

    @staticmethod
    def __insert(cursor, item):  # 执行sql语句的方法
        # cursor.execute(sql, params)
        pass




# client = MysqlTwistedPipeline.Text()
# sql = "SELECT * FROM `MS_EST_WH_HOTEL_INFO` WHERE BIG_DATA_HOTEL_ID='4646'"
# client.select(sql,printResult,printError)
#
# from twisted.internet import reactor
# reactor.callLater(5, reactor.stop)
# reactor.run()