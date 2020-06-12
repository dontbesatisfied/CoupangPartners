# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoupangItem(scrapy.Item):
    # define the fields for your item here like:
    productId = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    salesPrice = scrapy.Field()
    originPrice = scrapy.Field()
    shortUrl = scrapy.Field()
    contents = scrapy.Field()
