import pymysql,json
import pymysql.cursors

class SQLServer(object):
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

    @classmethod
    def from_settings(cls,settings,ServerType,db=None):
        sql_config = settings.get("MYSQL_SERVER")[ServerType]
        if db:
            sql_config["db"] = db
        conn = pymysql.connect(**sql_config)
        return cls(conn)

    def close(self):
        self.conn.close()

    def select(self, sql):
        self.cur.execute(sql)
        results = self.cur.fetchall()

        return results

    def insert(self, sql, params=None):
        if params:
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql)
        self.conn.commit()

    def execute(self,sql):
        self.cur.execute(sql)
        self.conn.commit()

# from scrapy.utils.project import get_project_settings
# from CrawlerRunner import cf
# settings = get_project_settings()
#
# print(cf.get("MYSQL_SERVER","type"))
#
# mysql_client = SQLServer.from_settings(settings, cf.get("MYSQL_SERVER", "type"),"bigdata")
# sql = "SELECT BIG_DATA_HOTEL_ID,SITE_ID,URL_CRAWL_INFO FROM `MS_EST_WH_HOTEL_SITE_REL` WHERE `STATUS`='NORMAL' AND SITE_ID=2;"
# results = mysql_client.select(sql)
# print(1111)
# print(results)