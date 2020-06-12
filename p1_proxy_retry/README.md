# scrapy_proxy_retry
目标： 换代理再重试

对象：自定义的中间件 （使用自带的中间件请忽略）

### 基础

scrapy默认开启'scrapy.downloadermiddlewares.retry.RetryMiddleware'中间件，其默认优先级为550

##### scrapy中间件的默认优先级

```
  'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
```

`process_request()` 每个中间件的方法将以**递增**的中间件顺序（100、200、300，...）`process_response()`每个中间件的方法将以**递减**(300,200,100)顺序被调用



#### 操作

0、把404设置为重试状态码，重试一个随便写的url（使之报404错误）

1、先关闭默认代理中间件

`'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,`

2、把自己定义的中间件开启，注意：根据响应链的调用顺序，一定要设置为**代理中间件的优先级低于重试优先级**，

```
'xxx.middlewares.AddProxyMiddlewares':543, # 低优先级
'xxx.middlewares.MyRetryMiddleware': 534, # 高优先级
```

