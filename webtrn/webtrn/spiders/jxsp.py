# -*- coding: utf-8 -*-
import scrapy
from webtrn.items import JxspItem
import json

class JxspSpider(scrapy.Spider):
    name = 'jxsp'
    allowed_domains = ['webtrn.cn']
    start_urls = ['http://ldcbs.webtrn.cn/api/open/reslib/content/search?condition.resType.code=zpzs&order._this.create_date=desc&page=1&size=250&_=1542554821523']

    def parse(self, response):
        datas = json.loads(response.body)['data']['data']
        if datas:
            for data in datas:
                #提取属性9为教学视频mp4 地址
                #把文件名信息提取通过 meta 传入下一个网址
                url="http://ldcbs.webtrn.cn/api/open/file/get?keyList="+data['attrs'][9]['value']+"&typeList=mp4"
                file_name=data['attrs'][2]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][3]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][0]['value'] + "_" \
                         +data['attrs'][5]['resTypeAttrEnum']['value'] + "_" \
                         +data['attrs'][6]['value'] + "_" \
                         +data['attrs'][4]['value'] + "_教学视频"
                #print('RRRRRRRRRRRRRRR\n',file_name,"\nKKKKKKKKKKKKKKKKK\n")
                meta = {'filename': file_name}
                yield scrapy.Request(url,callback=self.parse_mp4,meta=meta)

    def parse_mp4(self, response):
        datas = json.loads(response.body)
        #print(datas)
        if datas:
                #要保存的文件名提取
                filename=response.meta.get('filename','')
                
                #文件服务地址提取
                server_url_find="https://1-searchvideo.webtrn.cn/search_servers2?path="+datas['data'][0]
                
                #下载的分文件名提取地址
                url = "https://stream-1-aliyuncdn.webtrn.cn/"+datas['data'][0]

                #把信息通过 meta 传入下个网址，
                meta={'filename': filename,'ziwenjian_name': url}

                yield scrapy.Request(server_url_find,callback=self.parse_mp4_server,meta=meta)

    def parse_mp4_server(self, response):
        datas = json.loads(response.body)
        #print(datas)
        if datas:
                #要保存的文件名提取
                filename=response.meta.get('filename','')
                
                #子文件地址提取
                ziwenjian_name_url=response.meta.get('ziwenjian_name','')
                
                path_url=datas['path'].replace('meta.json','')

                #视频文件服务器地址路径
                path=list(map(lambda x : x + path_url ,datas['servers']))
                
                #print("&&&&&&&&&&&&&视频文件服务器地址路径:\n",path,"\n")

                #把信息通过 meta 传入下个网址，
                meta={'filename': filename,"path":path}

                yield scrapy.Request(ziwenjian_name_url,callback=self.parse_mp4_ziwenjian,meta=meta)


    def parse_mp4_ziwenjian(self, response):
        datas = json.loads(response.body)
        item=JxspItem()
        if datas:
                item['kechen_name']=response.meta.get('filename','')
                path=response.meta.get('path','')

                full_file_name=[]
                
                for i in datas['levels']['ori']['list']:
                    file=[]
                    for j in path:
                        #print('********************\n',i['filename'])
                        file.append(j+i['filename'])
                    full_file_name.append(file)
                #print('文件下载地址：\n',full_file_name,'\n\n')
                item['file_urls'] = full_file_name
                yield item


                

    