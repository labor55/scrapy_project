# -*- coding: utf-8 -*-
import os
import scrapy
from ..items import SinanewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide']

    def parse(self, response):
        items = []
        # 所有大类的标题和链接
        parentUrls = response.xpath('//div[@id="XX_conts"]//h3/a/@href').extract()
        parentTitle = response.xpath('//div[@id="XX_conts"]//h3/a/text()').extract()

        # 所有小类的标题和链接
        subUrls = response.xpath('//div[@id="XX_conts"]//ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id="XX_conts"]//ul/li/a/text()').extract()

        for i in range(len(parentTitle)):
            # 构造大类的文件夹名字
            parentFileName = './data/' + parentTitle[i]

            if not os.path.exists(parentFileName):
                os.makedirs(parentFileName)

            # 遍历小类列表
            for j in range(len(subTitle)):
                item = SinanewsItem()
                # 保存大类的标题和链接
                item['parentUrls'] = parentUrls[i]
                item['parentTitle'] = parentTitle[i]

                flag = subUrls[j].startswith(item['parentUrls'])
                if flag:
                    subFileName = parentFileName + '/' + subTitle[j]
                    if not os.path.exists(subFileName):
                        os.makedirs(subFileName)

                    item['subTitle'] = subTitle[j]
                    item['subUrls'] = subUrls[j]
                    item['subFileName'] = subFileName

                    items.append(item)
        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1': item}, callback=self.parse2)

    def parse2(self, response):
        meta1 = response.meta['meta_1']
        # 抓取所有a标签
        sonUrls = response.xpath('//a/@href').extract()
        items = []
        for i in range(len(sonUrls)):
            flag = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta1['parentUrls'])
            if flag:
                item = SinanewsItem()
                item['parentTitle'] = meta1['parentTitle']
                item['parentUrls'] = meta1['parentUrls']
                item['subUrls'] = meta1['subUrls']
                item['subTitle'] = meta1['subTitle']
                item['subFileName'] = meta1['subFileName']
                item['sonUrls'] = sonUrls[i]
                items.append(item)
        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2': item}, callback=self.parse3)

    def parse3(self, response):
        item = response.meta['meta_2']
        head = response.xpath('//h1/text()').extract_first()
        content = response.xpath('//div[@id="artibody"]').xpath('string(.)').extract_first()
        item['head'] = head
        item['content'] = content
        yield item
