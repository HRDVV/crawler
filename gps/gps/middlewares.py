# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.http import HtmlResponse


class GpsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GpsDownloaderMiddleware(object):

    def __init__(self):

        self.ua = UserAgent(path="useragent.json")
        super(GpsDownloaderMiddleware, self).__init__()

    def process_request(self, request, spider):
        # 代理ip, 免费的不好用
        # def get_ip():
        #     with Db() as db:
        #         sql = "SELECT ip from `proxy` ORDER BY RAND() LIMIT 0,1"
        #         ip = db.operator(sql, False)[0]

        if spider.name == 'gpsspg':
            key = request.meta.get('key')
            type_item = request.meta.get('type_item')
            spider.browser.get(request.url)
            # time.sleep(1.5)
            spider.browser.find_element_by_id('sm_' + str(type_item)).click()
            spider.browser.find_element_by_id("s_t").send_keys(key)
            spider.browser.find_element_by_id("s_btn").click()
            frame = spider.browser.find_element_by_id('map_f_' + str((type_item + 1) if type_item != 3 else 5))
            spider.browser.switch_to.frame(frame)
            time.sleep(3)
            page_source = spider.browser.page_source
            # print(self.ua.random)
            # 设置随机请求头
            request.headers.setdefault('User-Agent', self.ua.random)
            return HtmlResponse(body=page_source, url=spider.browser.current_url, encoding='utf8', request=request)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
