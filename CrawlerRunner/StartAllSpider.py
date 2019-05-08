from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from apscheduler.schedulers.twisted import TwistedScheduler

from scrapy.crawler import CrawlerProcess

from Crawler.pipelines.MySQL import MysqlTwistedPipeline



def CreateTask(crawler_process,TaskName):
    projectConf = crawler_process.settings.get("PROJECT_CONF","")
    # projectConf[""]
    print(projectConf)
    opts = {}

    crawler_process.crawl(TaskName, **opts)


if __name__ == '__main__':
    settings = get_project_settings()
    Scheduler = TwistedScheduler()
    crawler_process = CrawlerProcess(settings)
    mysql_client = MysqlTwistedPipeline.create_mysql_client("")
    Scheduler.add_job(func=CreateTask, args=(crawler_process,"BaiDu"), trigger='interval', seconds=2, id='BaiDu_task')
    Scheduler.start()
    reactor.run()
