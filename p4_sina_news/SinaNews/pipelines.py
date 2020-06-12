# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def process_item(self, item, spider):
        sonUrl = item['sonUrls']
        # ent.sina.com.cn_s_h_2019-06-21_doc-ihytcerk8383549
        filename = sonUrl[7:-6].replace('/', '_')
        file_name = filename + '.txt'
        with open(item['subFileName'] + '/' + file_name, 'w', encoding='utf8') as f:
            f.write(item['content'])
        return item
