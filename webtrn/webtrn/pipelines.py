# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
from random import choice

# from scrapy.pipeline.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline

class WebtrnPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        file_url = item['file_urls'][0]
        meta = {'filename': os.path.join("d:\\pdf",item['kechen_name'])}
        #print("%%%%%%%%%%%%%%%",file_url,"dddddddddddddddd")
        yield scrapy.Request(url=file_url, meta=meta)


    def file_path(self, request, response=None, info=None):
        """
        重命名模块
        """
        path= request.meta.get('filename','')
        #print('############\n',path,"\n************\n")
        return path

class JxspPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        a=0
        for file in item['file_urls']:
            path=choice(file)
            a=a+1
            #print("文件地址:\n",path) 
            filename= os.path.join("d:\\jxsp",item['kechen_name'],str(a)+'.flv')

            if os.path.exists(filename):
                continue
            else:
                meta = {'filename':filename}
                print("############################\n","正在下载文件到:\n",filename,\
                "地址为：\n",path\
                ,"\n###############################\n")
                yield scrapy.Request(url=path, meta=meta)


    def file_path(self, request, response=None, info=None):
        """
        重命名模块
        """
        path= request.meta.get('filename','')
        #print('############\n',path,"\n************\n")
        return path