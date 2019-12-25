# -*- coding: utf-8 -*-
import scrapy
from hot_search.items import HotSearchItem
from bs4 import BeautifulSoup
import json
import os
import time
class HotsearchSpider(scrapy.Spider):
    name = 'hotsearch'
    # allowed_domains = ['tophub.fun/main/home/hot']
    start_urls = ['https://tophub.fun/']

    def parse(self, response):
    
        node_list=response.xpath("//div[@class='article-component']")
        for node in node_list:
            item=HotSearchItem()
            name=node.xpath("./div[1]/a/text()").extract()
            link=node.xpath("./div[1]/a/@href").extract()
            heat=node.xpath(".//span[@class='source-title type']/text()").extract()
            item['name']=name[0]
            item['link']=link[0]
            yield item
    

        url="https://www.tophub.fun:8888/GetAllInfoGzip?id=2&page=0"
        for i in range (2,5):
            a="span[{}]".format(i)
            id=response.xpath("//div[@class='site-box']//"+a+"/@data-siteid").extract()[0]
            id=(int(id)%10000)
            url="https://www.tophub.fun:8888/GetAllInfoGzip?id={}&page=0".format(id)
            print('*'*30)
            print(url)
            yield scrapy.Request( url,callback=self.parse_page)

    def parse_page(self, response):
        result=json.loads(response.text)['Data']
        for node in result:
            item=HotSearchItem()
            name=node['Title']
            link=node['Url']
            item['name']=name
            item['link']=link
          
            yield item
            
      