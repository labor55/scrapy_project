# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../..')
from Scrapy_Shpgx_D45.items import ScrapyShpgxD45Item
import json
import time

class ShpgxV2Spider(scrapy.Spider):
    name = 'shpgx_v2'
    allowed_domains = ['www.shpgx.com']
    # 全国指数
    url = 'https://www.shpgx.com/marketzhishu'
    def start_requests(self):
        # 各地区价格指数，--->parse---> parse_area
        yield scrapy.Request(url=self.url+'/map', callback=self.parse)
        # 全国价格指数，---> parse_all
        yield scrapy.Request(url=self.url+'/list/3/22', callback=self.parse_all)

    # 解析区域代号，抛出每个地区的数据
    def parse(self, response):
        res_data = json.loads(response.text)
        for i in res_data:
            if i.__contains__('cd'):
                item = ScrapyShpgxD45Item()
                content_url = self.url + "/list/3/" + i['cd']
                item['region'] = i['name']
                item['indic_name'] = '中国LNG出厂价格区域指数:{}'.format(item['region'])
                temp = int(i['cd'])
                item['parent_id'] = '4002008002' + "0" * (3-len(str(temp-7))) + str(temp-7)
                self.logger.info('中国LNG出厂价格区域指数:{}, parent_id:{}'.format(item['region'],item['parent_id']))
                yield scrapy.Request(content_url, callback=self.parse_area, meta={"meta_1":item})
    def parse_area(self, response):
        res_data = json.loads(response.text)
        item = response.meta['meta_1']
        item["data_source"] = "上海石油天然气交易中心"
        item['cleaning_status'] = 0
        item['status'] = 1
        item['sign'] = '02'
        item['frequency'] = 8
        item['country'] = '中国'
        item['root_id'] = 4
        date = res_data['DATA'].split(",")
        baseprice = res_data['BASEPRICE'].split(",")
        for i in range(len(date)):
            item['data_value'] = baseprice[i]
            item['create_time'] = date[i]
            item['data_year'] = item['create_time'].split('-')[0]
            item['data_month'] = item['create_time'].split('-')[1]
            item['data_day'] = item['create_time'].split('-')[2]
            item['unit'] = "%"
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))

    def parse_all(self, response):
        item = ScrapyShpgxD45Item()
        res_data = json.loads(response.text)
        item["data_source"] = "上海石油天然气交易中心"
        item['cleaning_status'] = 0
        item['status'] = 1
        item['sign'] = '02'
        item['frequency'] = 8
        item['country'] = '中国'
        item['root_id'] = 4
        item['region'] = '中国'
        item['indic_name'] = '中国LNG出厂价格全国指数'
        item['parent_id'] = '4002008001'
        date = res_data['DATA'].split(",")
        baseprice = res_data['BASEPRICE'].split(",")
        for i in range(len(date)):
            item['data_value'] = baseprice[i]
            item['create_time'] = date[i]
            item['data_year'] = item['create_time'].split('-')[0]
            item['data_month'] = item['create_time'].split('-')[1]
            item['data_day'] = item['create_time'].split('-')[2]
            item['unit'] = "%"
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'shpgx_v2'])