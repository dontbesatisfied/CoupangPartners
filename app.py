from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from coupang import CoupangSpider
from naver import NaverSpider
from selenium import webdriver
import constants
from utils import copy_input, read_file
import os
from multiprocessing import Pool
import json
from time import sleep
from urllib.request import urlretrieve


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


        # 이미지 요청 및 다운로드
        urlretrieve(crawler_data['image'], "image.png")
        driver.find_element_by_css_selector(
            "input[type='file']").send_keys(os.getcwd()+'/image.png')

        # for (idx, content_image) in enumerate(crawler_data['contents']):
        #     # 컨텐츠 이미지 요청 및 다운로드
        #     urlretrieve(content_image, f"{idx}.png")
        #     driver.find_element_by_css_selector(
        #         "input[type='file']").send_keys(os.getcwd() + f'/{idx}.png')

        # image_elements = driver.find_elements_by_class_name('se-image-resource')
        # for image_element in image_elements:
        #     alt = image_element.get_attribute('alt')
        #      #.find_element_by_xpath('..').click()
        #     driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(f'//img[@alt="{alt}"]').find_element_by_xpath('..'))
        #     # print(alt, driver.find_element_by_class_name('se-object-arrangement-fit'))
        #     # driver.execute_script("arguments[0].setAttribute('width', '693')", image_element)



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
#
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
