# -*- coding: utf-8 -*-

BOT_NAME = 'Scrapy_Shpgx_D45'

SPIDER_MODULES = ['Scrapy_Shpgx_D45.spiders']
NEWSPIDER_MODULE = 'Scrapy_Shpgx_D45.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100Safari/537.36',

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES = {
   'Scrapy_Shpgx_D45.middlewares.AddProxyMiddlewares': 543,
   'Scrapy_Shpgx_D45.middlewares.MyRetryMiddleware': 534,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

ITEM_PIPELINES = {
   'Scrapy_Shpgx_D45.pipelines.MongoPipeline': 300,
}

# 正式集
MONGO_URI = 'localhost'
MONGO_DATABASE = 'D45'

# 日志文件等级
LOG_LEVEL= 'INFO'

# 重试设置
RETRY_TIMES = 4                      # 失败后重试次数，默认两次
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408,404]  # 重试验证码

