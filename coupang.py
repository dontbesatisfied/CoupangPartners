# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request, FormRequest
from utils import parse_detail_content
from items import CoupangItem
import constants
import json


class CoupangSpider(Spider):
    name = 'coupang'
    allowed_domains = ['partners.coupang.com', 'coupang.com']
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
            "categoryId": constants.COUPANG_SEARCH_CATEGORYID,
            "filter": constants.COUPANG_SEARCH_WORD,
            "deliveryTypes": [],
            "page": {"pageNumber": 0, "size": constants.COUPANG_SEARCH_COUNT}
        }), callback=self.parse_products)

    def parse_products(self, response):
        print(response.body.decode())
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
                }}), meta={'productId': i['productId'], 'itemId': i['itemId'], 'vendorItemId': i['vendorItemId'], 'title': i['title'], 'salesPrice': i['salesPrice'], 'image': i['image'], },  callback=self.parse_short_url) for i in products]

    def parse_short_url(self, response):
        _DETAIL_PAGE_URL = f"https://www.coupang.com/vp/products/{response.meta['productId']}/items/{response.meta['itemId']}/vendoritems/{response.meta['vendorItemId']}"
        print(_DETAIL_PAGE_URL)
        yield Request(url=_DETAIL_PAGE_URL, callback=self.parse_detail_info, headers={
            'User-Agent': 'PostmanRuntime/7.22.0',
        }, meta={'shortUrl': json.loads(response.body.decode())['data']['shortUrl'], 'title': response.meta['title'],
                 'image': response.meta['image'],
                 'salesPrice': response.meta['salesPrice'], })

    def parse_detail_info(self, response):
        detail_items = json.loads(response.body.decode())['details']
        contents = parse_detail_content(detail_items)

        item = CoupangItem()
        item['title'] = response.meta['title']
        item['image'] = response.meta['image']
        item['salesPrice'] = response.meta['salesPrice']
        item['shortUrl'] = response.meta['shortUrl']
        item['contents'] = contents
        return item
        # yield {
        #     'title': response.meta['title'],
        #     'image': response.meta['image'],
        #     'salesPrice': response.meta['salesPrice'],
        #     'shortUrl': response.meta['shortUrl'],
        #     'contents': contents,
        # }
