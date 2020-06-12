# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
from ..items import UserItem
import json
import re


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 开始用户
    start_user = 'excited-vczh'

    # 用户信息
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    # 用户关注列表
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # 粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)

    # 获取用户信息
    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query, offset=0, limit=20), callback=self.parse_follows)
        yield Request(self.followers_url.format(user=result.get('url_token'), include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)

    # 关注列表
    def parse_follows(self, response):
        results = json.loads(response.text)
        # 获取用户当前页面的关注列表
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        else:
            print('用户不存在')

        # 关注列表下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            # 将next_page修正为可用的url
            p = re.compile('com/(.*?)')
            next_page = re.sub(p, 'com/api/v4/', next_page)
            yield Request(next_page, callback=self.parse_follows)
        else:
            print('关注列表未找到')

    # 粉丝列表
    def parse_followers(self, response):
        results = json.loads(response.text)
        # 获取用户当前页面的关注列表
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        # 关注列表下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            # 将next_page修正为可用的url
            p = re.compile('com/(.*?)')
            next_page = re.sub(p, 'com/api/v4/', next_page)
            yield Request(next_page, callback=self.parse_followers)
        else:
            print('粉丝列表未找到')
