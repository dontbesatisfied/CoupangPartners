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
        # image = Image.open(
        #     '/Users/ian/workspace/my/CoupangPartners/1111.png')
        # print(image)
        # yield FormRequest(url=f'https://blog.upphoto.naver.com/{self.session_key}/simpleUpload/{random.randint(100000000, 999999999)}?userId={constants.NAVER_ID}&extractExif=true&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=', method='POST', formdata={
        #     'image': image
        # }, callback=self.get_image_url)
        yield FormRequest(url="https://blog.naver.com/RabbitWrite.nhn", method="POST", headers={
            'referer': f'https://blog.naver.com/{constants.NAVER_ID}/postwrite',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }, formdata={
            "blogId": constants.NAVER_ID,
            "documentModel": {
                "document": {
                    "version": "2.4.0",
                    "theme": "default",
                    "language": "ko-KR",
                    "components": [
                        {
                            "id": "SE-af884225-142e-4844-bd08-bbe05e6898a6",
                            "layout": "default",
                            "title": [
                                {
                                    "id": "SE-6eb3072c-b193-42d0-8408-fa76faad3f92",
                                    "nodes": [
                                        {
                                            "id": "SE-f997710d-3fa8-4593-8a25-51d725044b77",
                                            "value": "제목 입력",
                                            "@ctype": "textNode"
                                        }
                                    ],
                                    "@ctype": "paragraph"
                                }
                            ],
                            "align": "left",
                            "@ctype": "documentTitle"
                        },
                        {
                            "id": "SE-3e6ee39d-0bdb-45d7-b9f0-092207f36c91",
                            "layout": "default",
                            "value": [
                                {
                                    "id": "SE-922c2d9e-e358-42cd-ac68-8172a126a3a0",
                                    "nodes": [
                                        {
                                            "id": "SE-4d520fa4-74c5-40f9-b2ce-6d49ed7e80e1",
                                            "value": "테스트 삼다수 ->",
                                            "@ctype": "textNode"
                                        }
                                    ],
                                    "@ctype": "paragraph"
                                },
                                {
                                    "id": "SE-2d315809-217d-4456-8b6a-5af8d7967da8",
                                    "nodes": [
                                        {
                                            "id": "SE-290b3703-f9e2-46a0-88e7-807e7ff1d3e6",
                                            "value": "테스트 삼다수2",
                                            "style": {
                                                "fontSizeCode": "fs24",
                                                "bold": True,
                                                "@ctype": "nodeStyle"
                                            },
                                            "@ctype": "textNode"
                                        }
                                    ],
                                    "@ctype": "paragraph"
                                }
                            ],
                            "@ctype": "text"
                        },
                        {
                            "id": "SE-f1ceff1d-3c7a-4f13-a646-0a497a6bae74",
                            "layout": "default",
                            "src": "https://blogfiles.pstatic.net/MjAyMDA2MTFfMTU5/MDAxNTkxODA3MTc2NzI4.7H0crByi1PVfJyfMgJ4pdi62BdZaIFFKAP4a9eKEQaQg.rfivzXsU9wj_iWOTtCXlrhted0uydTCnHDiPWOpXF5kg.JPEG.zxcvzxcv93/1572793928637.jpg?type=w1",
                            "internalResource": True,
                            "represent": True,
                            "path": "/MjAyMDA2MTFfMTU5/MDAxNTkxODA3MTc2NzI4.7H0crByi1PVfJyfMgJ4pdi62BdZaIFFKAP4a9eKEQaQg.rfivzXsU9wj_iWOTtCXlrhted0uydTCnHDiPWOpXF5kg.JPEG.zxcvzxcv93/1572793928637.jpg",
                            "domain": "https://blogfiles.pstatic.net",
                            "fileSize": 344776,
                            "width": 693,
                            "widthPercentage": 0,
                            "height": 489,
                            "originalWidth": 1300,
                            "originalHeight": 919,
                            "fileName": "1572793928637.jpg",
                            "caption": None,
                            "format": "normal",
                            "displayFormat": "normal",
                            "contentMode": "fit",
                            "origin": {
                                "srcFrom": "local",
                                "@ctype": "imageOrigin"
                            },
                            "@ctype": "image"
                        },
                        {
                            "id": "SE-be2627c8-b663-4e98-9c5b-1933f3d4d079",
                            "layout": "default",
                            "value": [
                                {
                                    "id": "SE-b1f13c43-c012-4457-9ca3-60d616b0a3f8",
                                    "nodes": [
                                        {
                                            "id": "SE-a139c260-7e5f-4eb5-b88c-55e27aebf1f2",
                                            "value": "",
                                            "style": {
                                                "fontSizeCode": "fs24",
                                                "bold": True,
                                                "@ctype": "nodeStyle"
                                            },
                                            "@ctype": "textNode"
                                        }
                                    ],
                                    "@ctype": "paragraph"
                                }
                            ],
                            "@ctype": "text"
                        }
                    ]
                },
                "documentId": ""
            },
            "populationParams": {
                "configuration": {
                    "openType": 2,
                    "commentYn": True,
                    "sympathyYn": False,
                    "searchYn": True,
                    "scrapType": 2,
                    "outSideAllowYn": True,
                    "cclYn": False
                },
                "editorSource": "L9Lb8aLgQSlvHoW/j+ORoA==",
                "populationMeta": {
                    "mrBlogTalkCode": None,
                    "bookThemeInfoPk": None,
                    "greenReviewBannerYn": False,
                    "moviePanelParticipation": False,
                    "postLocationJson": None,
                    "postLocationSupportYn": False,
                    "categoryId": 1,
                    "directorySeq": 0,
                    "autoByCategoryYn": False,
                    "continueSaved": False,
                    "noticePostYn": False,
                    "tags": "#첫글",
                    "postWriteTimeType": "now",
                }
            }
        }, callback=self.upload)

    def upload(self, response):
        print(response.body)

    def get_image_url(self, response):
        print(response.body)
        pass

    def close(self):
        self.driver.quit()
