from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler import CrawlerSpider

settings = Settings()
settings.set('ROBOTSTXT_OBEY', False)

process = CrawlerProcess(settings=settings)
process.crawl(CrawlerSpider)
process.start()
