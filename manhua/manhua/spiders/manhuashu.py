# -*- coding: utf-8 -*-
import re
import scrapy
from manhua.items import ManhuaItem
import sys
import os
import urllib

class ManhuashuSpider(scrapy.Spider):
    name = 'manhuashu'
    #allowed_domains = ['97manhua.com']
    start_urls = [
        #'https://www.97manhua.com/manhua/42823/'
        #"https://www.97manhua.com/manhua/60763/"
        "https://www.97manhua.com/manhua/19542/"
        ]

    def parse(self, response):
        neirong=response.xpath('//*[@id="view-list-1"]/span/a')
        for url in neirong:
            urladr="https://www.97manhua.com"+url.xpath('@href').extract()[0]
            yield scrapy.Request(urladr,callback=self.parse_tu)

    def parse_tu(self,response):
        neirong=response.xpath('/html/body/script[2]/text()').extract()[0]
        pattern=re.compile(r'http:.*jpg-smh\.middle')
        urljpg = pattern.findall(neirong)[0]
        re1=re.compile(r'","')
        jpg=re1.split(urljpg)
        for url in jpg:
#            
            item = ManhuaItem()
            
            item["path"]=os.path.join("ok",url.split('/')[-2])
            item["filename"] = url.split('/')[-1].split("-")[0]
            item["image_url"] = url
            
            yield item 