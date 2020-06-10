from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from coupang import CoupangSpider
from naver import NaverSpider
from selenium import webdriver
import constants
from utils import copy_input, read_file, merge_images
import os
from multiprocessing import Pool
import json
from time import sleep
from urllib.request import urlretrieve
from selenium.webdriver.common.action_chains import ActionChains

def post(craweld_txt_data):
    try:
        crawler_data = json.loads(craweld_txt_data)

        driver = webdriver.Firefox(
            executable_path=constants.GECKO_DRIVER_PATH)
        driver.implicitly_wait(20)

        driver.get(
            'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

        copy_input(driver, '//*[@id="id"]', constants.NAVER_ID)
        copy_input(driver, '//*[@id="pw"]', constants.NAVER_PW)

        driver.find_element_by_id('log.login').click()

        driver.get(
            f'https://blog.naver.com/{constants.NAVER_ID}/postwrite')

        ActionChains(driver).send_keys(f'{crawler_data["title"]}')

        # 사진 업로드 버튼 클릭
        driver.execute_script('arguments[0].click();', driver.find_element_by_xpath(
            '//button[@data-log="dot.img"]'))

        # 이미지 요청 및 다운로드
        urlretrieve(crawler_data['image'], "./images/image.png")
        # 컨텐츠 이미지 요청 및 다운로드
        for (idx, content_image) in enumerate(crawler_data['contents']):
            urlretrieve(content_image, f"./images/content_{idx}.png")
        # 다운받은 이미지 전부 하나의 사진으로 병
        merged_image_path = merge_images(os.getcwd()+'/images')
        driver.find_element_by_css_selector(
            "input[type='file']").send_keys(merged_image_path)

        # driver.quit()

    except Exception as e:
        print('Error : ', e)
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
    'middleware.CoupangDownloaderMiddleware': 1
})

# process = CrawlerProcess(settings=settings)

# process.crawl(CoupangSpider)
# process.start()

result = read_file('result.txt')
post(result[0])

# pool = Pool(1) #os.cpu_count()
# pool.map(post, result)
