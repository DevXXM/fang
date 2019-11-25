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
        class_name = item.__class__.__name__
        if class_name == 'areaItem':
            try:
                self.cursor.execute(
                    "insert into l_xiaoqu (area, name,tag,cover,price,price_num,price_desc,deal,street,xiaoqu_id,url,lease,city) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update name=(name)",
                    (item['area'],
                     item['name'],
                     item['tag'],
                     item['cover'],
                     item['price'],
                     item['price_num'],
                     item['price_desc'],
                     item['deal'],
                     item['street'],
                     item['xiaoqu_id'],
                     item['url'],
                     item['lease'],
                     item['city']
                     ))
                self.connect.commit()
            except Exception as error:
                print(error)
                logging.log(error)
        else:
            try:
                self.cursor.execute(
                    "insert into l_house (title, sub,follow,default_img,img,price,unit,unit_price,layout,floor,orientation,renovation,area,years,day7_visit,day30_visit,buy_attr,basic_attr,special_attr,xiaoqu_id,house_id) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update title=(title)",
                    (item['title'],
                     item['sub'],
                     item['follow'],
                     item['default_img'],
                     item['img'],
                     item['price'],
                     item['unit'],
                     item['unit_price'],
                     item['layout'],
                     item['floor'],
                     item['orientation'],
                     item['renovation'],
                     item['area'],
                     item['years'],
                     item['day7_visit'],
                     item['day30_visit'],
                     item['buy_attr'],
                     item['basic_attr'],
                     item['special_attr'],
                     item['xiaoqu_id'],
                     item['house_id']
                     ))
                self.connect.commit()
            except Exception as error:
                print(error)
                logging.log(error)
        return item

    def close_spider(self, spider):
        self.connect.close()
