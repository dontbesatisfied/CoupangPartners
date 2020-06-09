from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from coupang import CoupangSpider
from naver import NaverSpider
from selenium import webdriver
import constants
from time import sleep
from utils import copy_input, read_file
import os
from multiprocessing import Pool
import requests
from PIL import Image
from io import BytesIO
import json


def post(craweld_txt_data):
    try:
        crawler_data = json.loads(craweld_txt_data)
        driver = webdriver.Firefox(
            executable_path=constants.GECKO_DRIVER_PATH)

        driver.get(
            'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        driver.implicitly_wait(1)

        copy_input(driver, '//*[@id="id"]', constants.NAVER_ID)
        copy_input(driver, '//*[@id="pw"]', constants.NAVER_PW)

        driver.find_element_by_id('log.login').click()
        driver.implicitly_wait(2)

        driver.get(
            f'https://blog.naver.com/{constants.NAVER_ID}?Redirect=Write')
        driver.implicitly_wait(2)

        # 블로그 작업공간이 iframe
        driver.switch_to.frame('mainFrame')
        # 클릭을 하지 않으면 input type=file이 안생김
        image_btn = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/header/div[1]/ul/li[1]/button')
        driver.execute_script('arguments[0].click();', image_btn)

        driver.find_element_by_css_selector(
            "input[type='file']").send_keys(os.getcwd()+'test.png')
        # driver.switchTo().defaultContent();
        sleep(5)

        driver.quit()
    except Exception as e:
        print('Error : ', e)
        driver.quit()


def upload_photo(cookies):
    requests.get(
        f'https://platform.editor.naver.com/api/blogpc001/v1/photo-uploader/session-key?userId={constants.NAVER_ID}',
        headers={
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7',
            'Host': 'platform.editor.naver.com',
            'Origin': 'https://blog.naver.com',
            'Referer': f'https://blog.naver.com/{constants.NAVER_ID}/postwrite',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        })
    pass


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
    'middleware.CoupangDownloaderMiddleware': 1
})

# process = CrawlerProcess(settings=settings)

# process.crawl(CoupangSpider)
# process.start()

result = read_file('results.txt')
post(result[0])

# res = requests.get(json.loads(result[0])['image'], headers={
#                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})
# img = Image.open(BytesIO(res.content))
# print(img)

# pool = Pool(1) #os.cpu_count()
# pool.map(post, result)
