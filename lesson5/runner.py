from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hh_spider import HhSpiderSpider
from jobparser.spiders.sj_spider import SjSpiderSpider

if __name__== '__main__':
    crawler_setings=Settings()
    crawler_setings.setmodule(settings)
    process=CrawlerProcess(settings=crawler_setings)
    process.crawl(HhSpiderSpider, vacancy='повар')
    process.crawl(SjSpiderSpider, vacancy1='повар')
    process.start()