# -*- coding: utf-8 -*-
import scrapy
from webtrn.items import WebtrnItem
import json

class YemianSpider(scrapy.Spider):
    name = 'yemian'
    allowed_domains = ['webtrn.cn']
    start_urls = ['http://ldcbs.webtrn.cn/api/open/reslib/content/search?condition.resType.code=zpzs&order._this.create_date=desc&page=1&size=215&_=1542554821523']

    def parse(self, response):
        datas = json.loads(response.body)['data']['data']
        if datas:
            for data in datas:
                url="http://idocv.webtrn.cn/content/"+data['attrs'][8]['value']+".json"
                yield scrapy.Request(url,callback=self.parse_pdf)



    def parse_pdf(self, response):
        datas = json.loads(response.body)
        #print(datas)
        item=WebtrnItem()
        if datas:
                item['kechen_name']=datas['name']
                item['file_urls']=[datas['srcUrl']]
                yield(item)