# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../..')
from Scrapy_Shpgx_D45.items import ScrapyShpgxD45Item
import json
import time


class ShpgxV4Spider(scrapy.Spider):
    name = 'shpgx_v4'
    allowed_domains = ['www.shpgx.com']
    url = 'https://www.shpgx.com/marketzhishu/list2'
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        js = json.loads(response.text)
        item = ScrapyShpgxD45Item()
        item['region'] = '中国'
        item["data_source"] = "上海石油天然气交易中心"
        item['cleaning_status'] = 0
        item['status'] = 1
        item['sign'] = '02'
        item['frequency'] = 8
        item['country'] = '中国'
        item['unit'] = '元/立方米'
        item['root_id'] = 2

        # 0号柴油价格和日期
        BASEPRICE_petrol = js['BASEPRICE_petrol'].split(",")
        DATA_petrol = js['DATA_petrol'].split(",")
        for i in range(len(DATA_petrol)):
            item['data_value'] = BASEPRICE_petrol[i]
            item['create_time'] = DATA_petrol[i]
            item['data_year'] = item['create_time'].split('-')[0]
            item['data_month'] = item['create_time'].split('-')[1]
            item['data_day'] = item['create_time'].split('-')[2]
            item['parent_id'] = '4002008004'
            item['indic_name'] = '中国LNG综合进口到岸价格'
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))

        yield item

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'Shpgx_V5'])
