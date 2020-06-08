from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.settings import Settings
from coupang import CoupangSpider
from naver import NaverSpider
from scrapy.utils.log import configure_logging
from selenium import webdriver
import constants
from time import sleep
from utils import copy_input
import os
from multiprocessing import Pool


def upload(x):
    try:
        driver = webdriver.Firefox(
            executable_path=constants.GECKO_DRIVER_PATH)
        driver.get(
            'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        sleep(1)

        copy_input(driver, '//*[@id="id"]', constants.NAVER_ID)
        copy_input(driver, '//*[@id="pw"]', constants.NAVER_PW)

        driver.find_element_by_id('log.login').click()
        sleep(2)

        driver.get(f'https://blog.naver.com/{constants.NAVER_ID}/postwrite')
        sleep(2)

        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()



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

# process = CrawlerProcess(settings=settings)
#
# process.crawl(CoupangSpider)
# process.start()

pool = Pool(os.cpu_count())
pool.map(upload, range(0, 2))


# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner(settings=settings)
#
#
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(CoupangSpider)
#     yield runner.crawl(NaverSpider)
#     reactor.stop()
#
#
# crawl()
# reactor.run()
