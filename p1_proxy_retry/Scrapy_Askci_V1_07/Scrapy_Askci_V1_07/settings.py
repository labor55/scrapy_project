
BOT_NAME = 'Scrapy_Askci_V1_07'

SPIDER_MODULES = ['Scrapy_Askci_V1_07.spiders']
NEWSPIDER_MODULE = 'Scrapy_Askci_V1_07.spiders'

ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100Safari/537.36'

DOWNLOAD_DELAY = 2

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Scrapy_Askci_V1_07.middlewares.AddProxyMiddlewares':543,
   'Scrapy_Askci_V1_07.middlewares.MyRetryMiddleware': 534,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Scrapy_Askci_V1_07.pipelines.MongoPipeline': 301,
}

# 正式集
MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'industry'

# 测试集
# MONGO_URI = '127.0.0.1'
# MONGO_DATABASE = 'B_07'

# 日志文件等级
LOG_LEVEL= 'INFO'

# 重试设置
RETRY_ENABLED = True                  # 默认开启失败重试，一般关闭
RETRY_TIMES = 4                      # 失败后重试次数，默认两次
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408,404]  # 重试验证码
