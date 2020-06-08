from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler import CrawlerSpider
from coupang import CoupangSpider

settings = Settings()
settings.set('ROBOTSTXT_OBEY', False)

settings.set('DEFAULT_REQUEST_HEADERS', {
    'Content-Type': 'application/json',
    'charset': 'UTF-8',
    'Accept': '*/*'
})
settings.set('USER_AGENT', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
settings.set('COOKIES_DEBUG', True)
settings.set('COOKIES_ENABLED', True)
settings.set('DOWNLOAD_TIMEOUT', 30)
# 분당 50회의 요청을 넘어가면 24시간 제한
# 3회 위반시 계정정지
# settings.set('DOWNLOAD_DELAY', 1.3)
settings.set('ITEM_PIPELINES',
             {
                 'pipelines.CrawlerPipeline': 300,
             }
             )
settings.set('DOWNLOADER_MIDDLEWARES', {
    # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':
    'middleware.CoupangDownloaderMiddleware': 1
})
process = CrawlerProcess(settings=settings)
process.crawl(CoupangSpider)
process.start()

