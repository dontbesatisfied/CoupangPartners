# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json
import logging


class CrawlerSpider(Spider):

    name = 'crawler'
    allowed_domains = ['partners.coupang.com', 'coupang.com', 'google.com']
    constants = {
        'CHROME_DRIVER_PATH': "/Users/ian/workspace/my/chromedriver",
        'COUPANG_ID': "benotsatisfied@gmail.com",
        'COUPANG_PW': "Tmdghks93!"

    }

    def start_requests(self):

        try:
            # Must install chrome webdriver
            # https://chromedriver.chromium.org/downloads
            self.driver = webdriver.Chrome(
                self.constants['CHROME_DRIVER_PATH'])
            self.driver.get('https://partners.coupang.com/')
            self.driver.find_element_by_xpath(
                '//button[@class="ant-btn btn-link"]').click()

            # 로그인
            sleep(2)
            self.driver.find_element_by_id(
                'login-email-input').send_keys(self.constants['COUPANG_ID'])
            self.driver.find_element_by_id(
                'login-password-input').send_keys(self.constants['COUPANG_PW'])
            self.driver.find_element_by_class_name('login__button').click()

            # 상품검색
            sleep(1)
            _SEARCH_URL = "https://partners.coupang.com/api/v1/search"
            yield Request(url=_SEARCH_URL, method='POST', cookies=self.driver.get_cookies(), body=json.dumps({
                "filter": "물",
                "deliveryTypes": [],
                "page": {"pageNumber": 0, "size": 2}
            }), callback=self.parse_products, meta={'cookie': self.driver.get_cookies()})
        except Exception as error:
            logging.error(error)

    def parse_products(self, response):
        try:
            products = json.loads(response.body.decode())['data']['products']
            for i in products:
                detail_page_url = "https://www.coupang.com/vp/products/{productId}?itemId={itemId}".format(
                    productId=i['productId'], itemId=i['itemId'])
                '''
                왜 Request를 날리면 pending이 나지??
                '''
                yield Request(url=detail_page_url, callback=self.parse_detail_info)
                # self.driver.get(detail_page_url)
                # sleep(1)
                # detail_page = Selector(text=self.driver.page_source)
                # detail_items = detail_page.xpath(
                #     '//div[@class="detail-item"]').extract()
                # # image = i['image'],
                # # originPrice = i['originPrice'],
                # # salesPrice = i['salesPrice'],
                # # title = i['title']

                # print(detail_items, "!@#!@#!@!#!@#!@#!#!@#!#!@!@#@!#")

                yield Request(url="https://partners.coupang.com/api/v1/banner/iframe/url", method="POST", body=json.dumps({'product': {
                    'discountRate': None,
                    'image': i['image'],
                    'itemId': i['itemId'],
                    'originPrice': i['originPrice'],
                    'productId': i['productId'],
                    'salesPrice': i['salesPrice'],
                    'title': i['title'],
                    'type': i['type'],
                    'vendorItemId': i['vendorItemId'],
                }}), cookies=response.meta['cookie'], callback=self.parse_url)

        except Exception as error:
            logging.error(error)

    def parse_url(self, response):
        try:
            yield {'shortUrl': json.loads(response.body.decode())['data']['shortUrl']}
        except Exception as error:
            logging.error(error)

    def parse_detail_info(self, response):
        # pass
        print(response)
        # yield {
        #     'image': response.xpath('//img[@class="prod-image__detail"]/@src').extract_first()
        # }

    def close(self):
        self.driver.quit()
        print('CLOSE')
