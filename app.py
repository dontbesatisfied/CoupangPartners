from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler import CrawlerSpider

settings = Settings()
settings.set('ROBOTSTXT_OBEY', False)
settings.set('DEFAULT_REQUEST_HEADERS', {
    'Content-Type': 'application/json',
    'charset': 'UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
})
settings.set('DOWNLOAD_TIMEOUT', 30)
settings.set('ITEM_PIPELINES',
             {
                 'pipelines.CrawlerPipeline': 300,
             }
             )
process = CrawlerProcess(settings=settings)
process.crawl(CrawlerSpider)
process.start()
