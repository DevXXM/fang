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
    xiaoqu_id = scrapy.Field()
    url = scrapy.Field()
    lease = scrapy.Field()
    city = scrapy.Field()


class houseItem(scrapy.Item):
    # id = scrapy.Field()
    title = scrapy.Field()  #标题
    sub = scrapy.Field()   #副标题
    follow = scrapy.Field() #关注人数
    default_img = scrapy.Field() #默认图
    img = scrapy.Field() #图片列表
    price = scrapy.Field() #总价格
    unit = scrapy.Field() #价格单位
    unit_price = scrapy.Field() #单价
    layout = scrapy.Field()  #户型
    floor = scrapy.Field() #楼层
    orientation = scrapy.Field() #方向
    renovation = scrapy.Field() #装修
    area = scrapy.Field() #面积
    years = scrapy.Field() #年代
    day7_visit = scrapy.Field() #七天看次数
    day30_visit = scrapy.Field() #30天看次数
    buy_attr = scrapy.Field() #交易属性
    basic_attr = scrapy.Field() #基本属性
    special_attr = scrapy.Field() #优势介绍
    xiaoqu_id = scrapy.Field() #小区ID
    house_id = scrapy.Field() #房屋ID