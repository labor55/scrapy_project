# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('../..')
from Scrapy_Askci_V1_07.items import ScrapyAskciV107Item
import logging
from time import sleep


logger = logging.getLogger(__name__)

class AskciSpider(scrapy.Spider):
    name = 'Askci_V1'
    allowed_domains = ['s.askci.com']
    # start_urls = {
    #     # 石油和天然气开采业
    #     'http://s.askci.com/data/economy/00002/1/':'2002',
    #     # 石油加工、炼焦和核燃料加工业
    #     'http://s.askci.com/data/economy/00020/1/':'3013',
    #     # 燃气生产和供应业
    #     'http://s.askci.com/data/economy/00039/1/':'4002',
    #     }
    start_urls = [
        'http://s.askci.com/data/economy/2156/1/',
        ]

    def start_requests(self):
        for k in self.start_urls:
            yield scrapy.Request(k,callback=self.parse)

    def parse(self, response):
        self.logger.info(response)
        pass
if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute(['scrapy', 'crawl', 'Askci_V1'])
