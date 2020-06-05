# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
import constants
from time import sleep
import json

class CrawlerSpider(Spider):

    name = 'crawler'
    allowed_domains = ['partners.coupang.com']

    def start_requests(self):

        # Must install chrome webdriver
        # https://chromedriver.chromium.org/downloads
        _CHROME_DRIVER_PATH = '/Users/ian/Desktop/ian/chromedriver'

        self.driver = webdriver.Chrome(_CHROME_DRIVER_PATH)
        self.driver.get('https://partners.coupang.com/')
        self.driver.find_element_by_xpath('//button[@class="ant-btn btn-link"]').click()

        sleep(2)
        self.driver.find_element_by_id('login-email-input').send_keys(constants.COUPANG_ID)
        self.driver.find_element_by_id('login-password-input').send_keys(constants.COUPANG_PW)
        self.driver.find_element_by_class_name('login__button').click()

        sleep(1)

        _SEARCH_URL = "https://partners.coupang.com/api/v1/search"
        yield Request(url=_SEARCH_URL, method='POST', cookies=self.driver.get_cookies(), body=json.dumps({
            "filter": "물",
            "deliveryTypes": [],
            "page": {"pageNumber": 0, "size": 2}
        }), headers={
            'Content-Type': 'application/json',
            'charset': 'UTF-8'
        }, callback=self.parse)

    def parse(self, response):
        print(response.body)
        self.driver.quit()
        pass



