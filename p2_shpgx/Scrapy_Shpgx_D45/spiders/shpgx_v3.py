# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../..')
from Scrapy_Shpgx_D45.items import ScrapyShpgxD45Item
import json
import time

# 中国华东LNG出站价格历史价格
class ShpgxV3Spider(scrapy.Spider):
    name = 'shpgx_v3'
    allowed_domains = ['www.shpgx.com']
    # start_urls = ['https://www.shpgx.com/html/SELNGIndexHistory.html']
    url = 'https://www.shpgx.com/marketzhishu/dataList'
    page = 1
    length = 25
    params = {
        "zhishukind":"3",
        "area":"3",
        "starttime":"",
        "endtime":"",
        "start":"0",
        "length":str(length),
        "ts":None,
    }

    def start_requests(self):
        # 中国华东LNG出站价格历史数据
        self.params['wareid'] = "6"
        self.params['ts'] = str(int(time.time() * 1000))
        yield scrapy.FormRequest(url=self.url, formdata=self.params, callback=self.parse)
        
    def parse(self, response):
        # json 数据转化为字典
        res = json.loads(response.text)
        # 数据获取
        for i in res['root']:
            item = ScrapyShpgxD45Item()
            item["data_source"] = "上海石油天然气交易中心"
            item['cleaning_status'] = 0
            item['status'] = 1
            item['sign'] = '02'
            item['frequency'] = 8
            item['country'] = '中国'
            item['region'] = '华东'
            item['root_id'] = 4
            item['unit'] = '元/立方米'
            item['data_value'] = i['retailprice']
            item['create_time'] = i['strdate']
            item['data_year'] = i['strdate'].split('-')[0]
            item['data_month'] = i['strdate'].split('-')[1]
            item['data_day'] = i['strdate'].split('-')[2]
            item['indic_name'] = '中国华东LNG出站价格'
            item['parent_id'] = '4002008003'
            yield item
            self.logger.info('*{} {} {} {}*'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))
            time.sleep(0.5)

        max_page = res['totalProperty'] // self.length + 1
        self.logger.info("页数：{}/{}".format(self.page,max_page+1))
        if self.page < max_page + 1:
            self.params['ts'] = str(int(time.time() * 1000))
            self.params['start'] = str(self.page * self.length)
            yield scrapy.FormRequest(url=self.url, formdata=self.params, callback=self.parse)
            self.page += 1

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'shpgx_v3'])