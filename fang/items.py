# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class areaItem(scrapy.Item):
    # id = scrapy.Field()
    name = scrapy.Field()
    area = scrapy.Field()
    tag = scrapy.Field()
    cover = scrapy.Field()
    price = scrapy.Field()
    price_num = scrapy.Field()
    price_desc = scrapy.Field()
    deal = scrapy.Field()
    street = scrapy.Field()
    house_id = scrapy.Field()
    url = scrapy.Field()
    lease = scrapy.Field()
    city = scrapy.Field()
