# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义新闻大类的标题和链接
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    # 小类的标题和链接
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    # 小类的存储的路径
    subFileName = scrapy.Field()

    # 新闻详情链接
    sonUrls = scrapy.Field()

    # 标题和内容
    head = scrapy.Field()
    content = scrapy.Field()






























