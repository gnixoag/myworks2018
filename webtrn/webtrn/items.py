# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebtrnItem(scrapy.Item):
    # define the fields for your item here like:
    kechen_name = scrapy.Field()
    file_urls=scrapy.Field()
    files=scrapy.Field()
    #pdf_url=scrapy.Field()

