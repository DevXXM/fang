import scrapy

from fang.items import areaItem
from fang.items import houseItem
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import json
import re


class mingyan(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "lianjia"  # 定义蜘蛛名,不要动

    # 换成自己的城市
    city = "广州"
    # 换成自己城市的链接
    url = 'https://gz.lianjia.com'

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        # 定义爬取的链接
        url = self.url + '/xiaoqu'
        urls = [
            url
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        '''
        start_requests已经爬取到页面
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        '''
        data = response.body
        # print(response.url)
        soup = BeautifulSoup(data, "lxml")
        areas = soup.find(attrs={'data-role': 'ershoufang'}).find_all('a')
        for area in areas:
            # print(area.text)
            url = response.url + area.get('href')[8:]
            # print(url)
            yield scrapy.Request(url, callback=self.xiaoqu_pages)
            # break

    def xiaoqu_pages(self, response):
        data = response.body
        # print(response.url)
        soup = BeautifulSoup(data, "html.parser")
        next_page = soup.find(attrs={'class': 'page-box fr'}).find(attrs={'class': 'house-lst-page-box'}).get(
            'page-data')
        page_json = json.loads(next_page)
        current_page = page_json['curPage']
        total_page = page_json['totalPage']
        if (current_page >= total_page):
            return False
        for i in range(1, total_page + 1):
            # print(i)
            url = response.url + "pg" + str(i) + "/"
            # print(url)
            yield scrapy.Request(url, callback=self.xiaoqu_list)
            # break

    def xiaoqu_list(self, response):
        data = response.body
        # print(response.url)
        soup = BeautifulSoup(data, "html.parser")
        xiaoqus = soup.find(attrs={'class': 'listContent'}).find_all('li')
        for i in xiaoqus:
            # print(i)
            xiaoqu_id = i.get('data-id')
            url = i.find(attrs={'class': 'img'}).get('href')
            area = i.find(attrs={'class': 'district'}).text
            street = i.find(attrs={'class': 'bizcircle'}).text
            name = i.find(attrs={'class': 'title'}).find('a').text
            cover = i.find(attrs={'class': 'lj-lazy'}).get('data-original')
            price = i.find(attrs={'class': 'totalPrice'}).text
            price_num = i.find(attrs={'class': 'totalPrice'}).find('span').text
            if price_num == '暂无':
                price_num = 0
            price_desc = i.find(attrs={'class': 'priceDesc'}).text.strip()
            deal = i.find(attrs={'class': 'houseInfo'}).find(attrs={'title': re.compile(r"网签")}).text
            lease = i.find(attrs={'class': 'houseInfo'}).find(attrs={'title': re.compile(r"租房")}).text
            if i.find(attrs={'class': 'tagList'}).find('span') is None:
                tag = ""
            else:
                tag = i.find(attrs={'class': 'tagList'}).find('span').text
            item = areaItem()
            item['name'] = name
            item['area'] = area
            item['tag'] = tag
            item['cover'] = cover
            item['price'] = price
            item['price_num'] = price_num
            item['price_desc'] = price_desc
            item['deal'] = deal
            item['street'] = street
            item['xiaoqu_id'] = xiaoqu_id
            item['url'] = url
            item['lease'] = lease
            item['city'] = self.city
            # print(item)
            yield item
            ershou_url = self.url + '/ershoufang/c' + xiaoqu_id
            # print(ershou_url)
            yield scrapy.Request(ershou_url, callback=self.get_ershou_pages)
            # break

    def get_ershou_pages(self, response):
        data = response.body
        print(response.url)
        soup = BeautifulSoup(data, "html.parser")
        next_page = soup.find(attrs={'class': 'page-box fr'}).find(attrs={'class': 'house-lst-page-box'}).get(
            'page-data')
        page_json = json.loads(next_page)
        current_page = page_json['curPage']
        total_page = page_json['totalPage']
        if (current_page >= total_page):
            return False
        for i in range(1, total_page + 1):
            # print(i)
            before = response.url[0:response.url.rfind('c', 1)]
            after = response.url[response.url.rfind('c', 1):]
            url = before + "pg" + str(i) + after
            # print(url)
            yield scrapy.Request(url, callback=self.get_ershou_list)
            # break

    def get_ershou_list(self, response):
        xiaoqu_id = response.url[response.url.rfind('c', 1) + 1:-1]
        # print(xiaoqu_id)
        data = response.body
        # print(response.url)
        soup = BeautifulSoup(data, "html.parser")
        houses = soup.find(attrs={'class': 'sellListContent'}).find_all('li')
        for i in houses:
            # print(i)
            # house_id = i.find(attrs={'class': 'noresultRecommend'}).get('data-housecode')
            house_url = i.find(attrs={'class': 'noresultRecommend'}).get('href')
            # house_img = i.find(attrs={'class': 'noresultRecommend'}).find(attrs={'class': 'lj-lazy'}).get(
            #     'data-original')
            # title = i.find(attrs={'class': 'title'}).find('a').text
            yield scrapy.Request(house_url, callback=self.get_house_info, meta={'xiaoqu_id': xiaoqu_id})
            # print(house_id)
            # print(house_url)
            # print(house_img)
            # print(title)
            # break

    def get_house_info(self, response):
        xiaoqu_id = response.meta['xiaoqu_id']
        data = response.body
        print(response.url)
        house_id = response.url[response.url.rfind('/', 1) + 1:response.url.rfind('.')]
        soup = BeautifulSoup(data, "html.parser")
        title = soup.find(attrs={'class': 'title-wrapper'}).find(attrs={'class': 'main'}).get('title')
        sub = soup.find(attrs={'class': 'title-wrapper'}).find(attrs={'class': 'sub'}).get('title')
        follow = soup.find(attrs={'id': 'favCount'}).text
        default_img = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'defaultImg'}).get('src')
        img_list = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'smallpic'}).find_all('li')
        img_arr = []
        for img in img_list:
            tmp = {}
            # if img.get('data-vr') is not None:
            tmp['vr'] = img.get('data-vr')
            tmp['desc'] = img.get('data-desc')
            tmp['img'] = img.get('data-pic')
            img_arr.append(tmp)
        img = json.dumps(img_arr)
        price = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'price'}).find(attrs={'class': 'total'}).text
        unit = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'price'}).find(attrs={'class': 'unit'}).text
        unit_price = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'price'}).find(attrs={'class': 'unitPriceValue'}).text
        layout = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'room'}).find(attrs={'class': 'mainInfo'}).text
        floor = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'room'}).find(attrs={'class': 'subInfo'}).text

        orientation = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'type'}).find(attrs={'class': 'mainInfo'}).text
        renovation = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'type'}).find(attrs={'class': 'subInfo'}).text

        area = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'area'}).find(attrs={'class': 'mainInfo'}).text
        years = soup.find(attrs={'class': 'overview'}).find(attrs={'class': 'content'}).find(
            attrs={'class': 'houseInfo'}).find(attrs={'class': 'area'}).find(attrs={'class': 'subInfo'}).text

        day7_visit = soup.find(attrs={'class': 'm-content'}).find(attrs={'id': 'record'}).find(
            attrs={'class': 'count'}).text
        day30_visit = soup.find(attrs={'class': 'm-content'}).find(attrs={'id': 'record'}).find(
            attrs={'class': 'totalCount'}).find('span').text

        basic_list = soup.find(attrs={'id': 'introduction'}).find(attrs={'class': 'introContent'}).find(
            attrs={'class': 'content'}).find_all('li')

        # xiaoqu_id = soup.find(attrs={'id':'framesdk'}).get('data-resblock-id')
        basic_attr_dict = []
        for i in basic_list:
            tmp = {}
            tmp['attr'] = i.find('span').text
            tmp['value'] = i.text
            basic_attr_dict.append(tmp)

        buy_attr_list = soup.find(attrs={'id': 'introduction'}).find(attrs={'class': 'introContent'}).find(
            attrs={'class': 'transaction'}).find(
            attrs={'class': 'content'}).find_all('li')
        buy_attr_dict = []
        for i in buy_attr_list:
            tmp = {}
            tmp['attr'] = i.find('span').text
            tmp['value'] = i.text
            buy_attr_dict.append(tmp)

        special_list = soup.find(attrs={'class': 'showbasemore'}).find_all(attrs={'class': 'baseattribute'})
        special_dict = []
        for i in special_list:
            tmp = {}
            tmp['attr'] = i.find(attrs={'class': 'name'}).text
            tmp['value'] = i.find(attrs={'class': 'content'}).text.strip()
            special_dict.append(tmp)

        buy_attr = json.dumps(buy_attr_dict)
        basic_attr = json.dumps(basic_attr_dict)
        special_attr = json.dumps(special_dict)
        item = houseItem()
        item['title'] = title
        item['sub'] = sub
        item['follow'] = follow
        item['default_img'] = default_img
        item['img'] = img
        item['price'] = price
        item['unit'] = unit
        item['unit_price'] = unit_price
        item['layout'] = layout
        item['floor'] = floor
        item['orientation'] = orientation
        item['renovation'] = renovation
        item['area'] = area
        item['years'] = years
        item['day7_visit'] = day7_visit
        item['day30_visit'] = day30_visit
        item['buy_attr'] = buy_attr
        item['basic_attr'] = basic_attr
        item['special_attr'] = special_attr
        item['xiaoqu_id'] = xiaoqu_id
        item['house_id'] = house_id
        yield item
