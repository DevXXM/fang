# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from fang import settings
import logging


class FangPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        print('1111111111111111111111111111111111111111111111111111111111111111111111111111111')
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        print(
            '222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

        try:
            self.cursor.execute(
                "insert into l_xiaoqu (area, name,tag,cover,price,price_num,price_desc,deal,street,house_id,url,lease,city) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update name=(name)",
                (item['area'],
                 item['name'],
                 item['tag'],
                 item['cover'],
                 item['price'],
                 item['price_num'],
                 item['price_desc'],
                 item['deal'],
                 item['street'],
                 item['house_id'],
                 item['url'],
                 item['lease'],
                 item['city']
                 ))
            self.connect.commit()
        except Exception as error:
            print(error)
            logging.log(error)
        return item

    def close_spider(self, spider):
        self.connect.close()
