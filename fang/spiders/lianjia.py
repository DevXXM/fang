import scrapy

from fang.items import areaItem
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import json
import re


class mingyan(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "lianjia"  # 定义蜘蛛名
    city = "重庆"
    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        urls = [
            'https://cq.lianjia.com/xiaoqu',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''

        # page = response.url.split("/")[-2]  # 根据上面的链接提取分页,如：/page/1/，提取到的就是：1
        # filename = 'mingyan-%s.html' % page  # 拼接文件名，如果是第一页，最终文件名便是：mingyan-1.html
        # with open(filename, 'wb') as f:  # python文件操作，不多说了；
        #     f.write(response.body)  # 刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        # self.log('保存文件: %s' % filename)  # 打个日志
        # page = response.url.split("/")
        data = response.body
        print(response.url)
        soup = BeautifulSoup(data, "lxml")
        areas = soup.find(attrs={'data-role': 'ershoufang'}).find_all('a')
        for area in areas:
            print(area.text)
            url = response.url + area.get('href')[8:]
            print(url)
            yield scrapy.Request(url, callback=self.xiaoqu_pages)
            # break

    def xiaoqu_pages(self, response):
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
            print(i)
            url = response.url + "pg" + str(i) + "/"
            print(url)
            yield scrapy.Request(url, callback=self.xiaoqu_list)
            # break

    def xiaoqu_list(self, response):
        data = response.body
        print(response.url)
        soup = BeautifulSoup(data, "html.parser")
        xiaoqus = soup.find(attrs={'class': 'listContent'}).find_all('li')
        # print(xiaoqus)
        for i in xiaoqus:
            print(i)
            house_id = i.get('data-id')
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
            item['house_id'] = house_id
            item['url'] = url
            item['lease'] = lease
            item['city'] = self.city
            print(item)
            yield item
            # break
