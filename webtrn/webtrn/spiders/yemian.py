# -*- coding: utf-8 -*-
import scrapy
from webtrn.items import WebtrnItem
import json

class YemianSpider(scrapy.Spider):
    name = 'yemian'
    allowed_domains = ['webtrn.cn']
    start_urls = ['http://ldcbs.webtrn.cn/api/open/reslib/content/search?condition.resType.code=zpzs&order._this.create_date=desc&page=1&size=250&_=1542554821523']

    def parse(self, response):
        datas = json.loads(response.body)['data']['data']
        if datas:
            for data in datas:
                url="http://idocv.webtrn.cn/content/"+data['attrs'][8]['value']+".json"
                file_name=data['attrs'][2]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][3]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][0]['value'] + "_" \
                         +data['attrs'][5]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][6]['value'] + "_" \
                         +data['attrs'][4]['value']+'.pdf'
                #print('RRRRRRRRRRRRRRR\n',file_name,"\nKKKKKKKKKKKKKKKKK\n")
                meta = {'filename': file_name}
                yield scrapy.Request(url,callback=self.parse_pdf,meta=meta)



    def parse_pdf(self, response):
        datas = json.loads(response.body)
        #print(datas)
        item=WebtrnItem()
        if datas:
                item['kechen_name']=response.meta.get('filename','')
                #print('yyyyyyyyyyyyyy\n',item['kechen_name'],"\n55555555555555555\n")
                item['file_urls']=[datas['srcUrl']]
                yield(item)