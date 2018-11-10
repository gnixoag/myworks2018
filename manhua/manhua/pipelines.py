# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
import shutil
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    "Referer": "https://www.97manhua.com/",  # 加入referer 为下载的域名网站
}


class ManhuaPipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    
    def get_media_requests(self,item,info):
        jpg=item["image_url"]
        yield scrapy.Request(jpg)
            
    def item_completed(self,results,item,info):
        image_path = [x["path"] for ok, x in results if ok]

        if not os.path.exists(self.img_store+"\\"+item['path']):
            os.makedirs(self.img_store+"\\"+item['path'])
        
        shutil.move(self.img_store+"\\"+image_path[0],self.img_store+"\\"+item['path']+"\\"+item["filename"])
        