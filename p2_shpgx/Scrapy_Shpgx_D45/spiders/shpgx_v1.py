# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../..')
from Scrapy_Shpgx_D45.items import ScrapyShpgxD45Item
import json
import time
import requests

class ShpgxV1Spider(scrapy.Spider):
    '''
        管道天然气数据和液化天然气数据
    '''
    name = 'shpgx_v1'
    allowed_domains = ['www.shpgx.com']
    url = 'https://www.shpgx.com/marketstock/dataList'
    page = 1
    length = 25
    # "wareid":"3" 为液化天然气数据，6 为管道天然气数据
    params = {
        "wareid":"6",
        "cd":"",
        "starttime":"",
        "endtime":"",
        "start":"0",
        "length":str(length),
        "ts":None,
    }

    def start_requests(self):
        # 管道天然气
        self.params['wareid'] = "6"
        self.params['ts'] = str(int(time.time() * 1000))
        yield scrapy.FormRequest(url=self.url, formdata=self.params, callback=self.parse)
        # 液化天然气
        self.params['wareid'] = '3'
        yield scrapy.FormRequest(self.url, formdata=self.params, callback=self.parse)

    def parse(self, response):
        # json 数据转化为字典
        res = json.loads(response.text)
        # 数据获取
        for i in res['root']:
            # 公共部分
            item = ScrapyShpgxD45Item()
            item["data_source"] = "上海石油天然气交易中心"
            item['cleaning_status'] = 0
            item['status'] = 1
            item['sign'] = '02'
            item['frequency'] = 8
            item['country'] = '中国'
            item['region'] = i['jsd']
            item['root_id'] = 4
            # 挂牌价
            item['unit'] = i['priceunit']
            item['indic_name'] = i['warekind'] + '挂牌价'
            item['data_value'] = i['basename']
            item['create_time'] = i['orderdate']
            item['data_year'] = i['orderdate'].split('-')[0]
            item['data_month'] = i['orderdate'].split('-')[1]
            item['data_day'] = i['orderdate'].split('-')[2]
            if i['warekind'] == 'PNG':
                item['parent_id'] = '4002006001'
            elif i['warekind'] == 'LNG':
                # item['parent_id'] = '4002007001'
                item['indic_name'] = i['warekind'] + '挂牌价' + item['region']
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))
            # 挂牌量
            item['unit'] = i['countunit']
            item['data_value'] = i['basenum']
            item['indic_name'] = i['warekind'] + '挂牌量'
            if i['warekind'] == 'PNG':
                item['parent_id'] = '4002006002'
            elif i['warekind'] == 'LNG':
                item['indic_name'] = i['warekind'] + '挂牌量' + item['region']
                # item['parent_id'] = '4002007002'
            yield item
            self.logger.info('*{} {} {} {}*'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))

            # 成交价
            item['data_value'] = i['contprice']
            item['unit'] = i['priceunit']
            item['indic_name'] = i['warekind'] + '成交价'
            item['create_time'] = i['enddate']
            item['data_year'] = i['enddate'].split('-')[0]
            item['data_month'] = i['enddate'].split('-')[1]
            item['data_day'] = i['enddate'].split('-')[2]
            if i['warekind'] == 'PNG':
                item['parent_id'] = '4002006003'
            elif i['warekind'] == 'LNG':
                # item['parent_id'] = '4002007003'
                item['indic_name'] = i['warekind'] + '成交价' + item['region']
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))
            # 成交量
            item['unit'] = i['countunit']
            item['data_value'] = i['dealnum']
            if i['warekind'] == 'PNG':
                item['indic_name'] = i['warekind'] + '成交量'
                item['parent_id'] = '4002006004'
            elif i['warekind'] == 'LNG':
                item['indic_name'] = i['warekind'] + '成交量' + item['region']
                # item['parent_id'] = '4002007004'
            yield item
            self.logger.info('****{} {} {} {}****'.format(item['create_time'],item['indic_name'],item['data_value'],item['unit']))
            time.sleep(1)

        max_page = res['totalProperty'] // self.length + 1
        self.logger.info("页面{}/{}".format(self.page,max_page))
        if self.page < max_page + 1:
            self.params['ts'] = str(int(time.time() * 1000))
            self.params['start'] = str(self.page * self.length)
            yield scrapy.FormRequest(url=self.url, formdata=self.params, callback=self.parse)
            self.page += 1

    def pid_api(self,data_list,**kwargs):
        arr = []
        p_data = {'data':json.dumps(arr.append(data_list))}
        url = "http://localhost:5020/get"
        p_res = requests.post(url, data=p_data)
        pid = json.loads(p_res.text)['res']
        return pid

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'shpgx_v1'])