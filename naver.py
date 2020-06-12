# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from selenium import webdriver
import constants
from time import sleep
from utils import copy_input
import re
import json
import random
from PIL import Image
import os


class NaverSpider(Spider):
    name = 'naver'
    allowed_domains = ['naver.com']
    token = None
    session_key = None

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

        # self.driver.get(
        #     f'https://blog.naver.com/{constants.NAVER_ID}/postwrite')

        yield Request(url=f'https://blog.naver.com/{constants.NAVER_ID}/postwrite', cookies=self.driver.get_cookies(), callback=self.get_token)

    def get_token(self, response):
        finder = re.compile(r'token: "(.*?)"')
        self.token = finder.findall(response.body.decode())[0]

        yield Request(url=f'https://platform.editor.naver.com/api/blogpc001/v1/photo-uploader/session-key?userId={constants.NAVER_ID}', headers={'SE-Authorization': self.token}, callback=self.get_session_key)

    def get_session_key(self, response):

        self.session_key = json.loads(response.body.decode())['sessionKey']
        # image = Image.open(os.getcwd() + '/1111.png')

        yield FormRequest(url=f'https://blog.upphoto.naver.com/{self.session_key}/simpleUpload/{random.randint(100000000, 999999999)}?userId={constants.NAVER_ID}&extractExif=true&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=', method='POST', formdata={
            'image': open(os.getcwd() + '/1111.png', 'rb').read()
        }, callback=self.get_image_url)

    def upload(self, response):
        print(response.body)

    def get_image_url(self, response):
        print(response.body)
        pass

    def close(self):
        self.driver.quit()
