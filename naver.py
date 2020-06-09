# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from selenium import webdriver
import constants
from time import sleep
from utils import copy_input


class NaverSpider(Spider):
    name = 'naver'
    allowed_domains = ['naver.com']

    def start_requests(self):
        # Must install chrome webdriver
        # https://chromedriver.chromium.org/downloads
        # self.driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)
        '''
        파이어 폭스로 하면 네이버 자동로그인이 된다... 파이어폭스 설치 및 드라이버가 선결조건
        '''
        self.driver = webdriver.Firefox(
            executable_path=constants.GECKO_DRIVER_PATH)
        self.driver.get(
            'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        sleep(1)

        copy_input(self.driver, '//*[@id="id"]', constants.NAVER_ID)
        copy_input(self.driver, '//*[@id="pw"]', constants.NAVER_PW)

        self.driver.find_element_by_id('log.login').click()
        sleep(2)

        self.driver.get(
            f'https://blog.naver.com/{constants.NAVER_ID}/postwrite')

        scr = self.driver.find_element_by_tag_name('script')
        print(scr, '@@@' * 10)

        # yield Request(url=f'https://blog.naver.com/{constants.NAVER_ID}/postwrite', callback=self.parse, cookies=self.driver.get_cookies())

        # yield Request(url=f'https://platform.editor.naver.com/api/blogpc001/v1/photo-uploader/session-key?userId={constants.NAVER_ID}', callback=self.parse, cookies=self.driver.get_cookies())
        yield Request(url='https://platform.editor.naver.com/api/blogpc001/v1/service_config', callback=self.parse, cookies=self.driver.get_cookies())

    def parse(self, response):
        print(response.body)
        pass

    def close(self):
        self.driver.quit()
