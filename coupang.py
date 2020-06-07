# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
import constants
import json

class CoupangSpider(Spider):
    name = 'coupang'
    allowed_domains = ['partners.coupang.com', 'coupang.com']
    # start_urls = ['http://partners.coupang.com/']
    start_urls = ['https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fpartners.coupang.com%2Fpostlogin%3Fs%3DpTdDpjtkcHvlTPyq2xuMHMUklbFezVrZ2_-2gFhjvikLvr_lWTl9sySXpBoQ3icEOO8dNLAB3_UpBtBQnPAi1cygYGZd-vfN1vPJonkWVG-hUz_dCDseUIOCZRD5zvkjv91J_T6Bb63cYciaOoeJiQ']

    def parse(self, response):

        _LOGIN_URL = 'https://login.coupang.com/login/loginProcess.pang'

        yield FormRequest(url=_LOGIN_URL, formdata={
            'email': constants.COUPANG_ID,
            'password': constants.COUPANG_PW
        }, callback=self.search_products)

    def search_products(self, response):
        print(response.body.decode())
        _SEARCH_ENDPOINT = "https://partners.coupang.com/api/v1/search"
        yield Request(url=_SEARCH_ENDPOINT, method='POST', body=json.dumps({
            "filter": "물",
            "deliveryTypes": [],
            "page": {"pageNumber": 0, "size": 2}
        }), callback=self.parse_products)

    def parse_products(self, response):
        products = json.loads(response.body.decode())['data']['products']
        _SHORT_URL_ENDPOINT = "https://partners.coupang.com/api/v1/banner/iframe/url"

        return [Request(url=_SHORT_URL_ENDPOINT, method="POST", body=json.dumps({'product': {
                'discountRate': None,
                'image': i['image'],
                'itemId': i['itemId'],
                'originPrice': i['originPrice'],
                'productId': i['productId'],
                'salesPrice': i['salesPrice'],
                'title': i['title'],
                'type': i['type'],
                'vendorItemId': i['vendorItemId'],
            }}), meta={'productId': i['productId'], 'itemId': i['itemId']},  callback=self.parse_short_url) for i in products]

    def parse_short_url(self, response):
        print(json.loads(response.body.decode())['data']['shortUrl'])
        _DETAIL_PAGE_URL = f"https://www.coupang.com/vp/products/{response.meta['productId']}?itemId={response.meta['itemId']}&isAddedCart="
        print(_DETAIL_PAGE_URL)
        yield Request(url=_DETAIL_PAGE_URL, callback=self.parse_detail_info, headers= {
            'User-Agent': 'PostmanRuntime/7.22.0',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Postman-Token': '1fd3873a-42b3-4ab3-9cda-3676b3611315',
            'Host': 'www.coupang.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })

    def parse_detail_info(self, response):
        print(response)


