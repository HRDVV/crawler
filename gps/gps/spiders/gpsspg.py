# -*- coding: utf-8 -*-
import codecs
import json

from scrapy.xlib.pydispatch import dispatcher
from scrapy import Spider, Request, signals
from ..items import GpsItem
from selenium import webdriver
from ..utils.crypto import Codecs
from ..utils.handler import Handler
from ..utils.distance import Distance
from selenium.webdriver.chrome.options import Options
import time
import logging
import xlrd

# 无头浏览器配置
chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--headless')


class GpsspgSpider(Spider):
    name = 'gpsspg'
    type_list = (1, 2, 3)
    allowed_domains = ['gpsspg.com']

    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.address_list = set(self.data_resource("input/gps.xlsx"))
        # self.compare_before_list = []
        super(GpsspgSpider, self).__init__()
        print(self.address_list)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    """
        爬虫的起点，返回request交给scrapy的下载器
    """
    def start_requests(self):
        logging.info("开始爬虫-%s" % time.time())
        url = 'http://www.gpsspg.com/maps.htm'
        for item in self.address_list:
            for type_item in self.type_list:
                yield Request(url=url, dont_filter=True, callback=self.parse, meta={"key": item, "type_item": type_item})

    def parse(self, response):
        logging.info("=====开始解析=====")
        try:
            key = response.meta.get("key")
            type_item = response.meta.get("type_item")
            if type_item == 1:
                poi_set = response.xpath('//div[@class="BMap_bubble_content"]/text()').extract()
                if poi_set:
                    poi = poi_set[2].split("：")[1]
                    # print(poi)
            else:
                poi = response.xpath('//div[@style="width:280px;padding:0 5px;"]/span[@class="fcg"]/text()').extract_first()

            item = GpsItem()

            if poi is not None:
                poi_long = poi.split(",")[1]
                poi_short = poi.split(",")[0]
                item["poi_long"] = poi_long
                item["poi_short"] = poi_short
                item["desc"] = None
            else:
                item["poi_long"] = None
                item["poi_short"] = None
                item["desc"] = "找不到地址或爬虫失败,请排查该地址的准确性"

            item["batch_no"] = Codecs.md5(key)
            item["batch_name"] = self.get_map_type()[type_item]
            item["address"] = key
            item["batch_type"] = type_item

            logging.info("单条爬虫结束-%s" % time.time())
            logging.info("=====爬虫结果: %s" % item)
            yield item
        except Exception as e:
            logging.error(e)
            self.browser.quit()

    def spider_closed(self):
        self.browser.quit()
        resource_data = Handler.combine_data()
        for item in resource_data:
            dict_list = []
            for item_info in item["info"]:
                if item_info["long"] is not None and item_info["short"] is not None:
                    dict_list.append({
                        "long": item_info["long"],
                        "short": item_info["short"],
                        "batch_name": item_info["batch_name"]
                    })
            item["distance"] = self.get_distance(*dict_list)
        with codecs.open("target/gps-finally.json", "wb", encoding="utf8") as f:
            f.write(json.dumps(resource_data))

    @staticmethod
    def get_map_type():
        return {
            1: '百度',
            2: '腾讯',
            3: '高德'
        }

    @staticmethod
    def data_resource(filename):
        xls = xlrd.open_workbook(filename=filename)
        sheet = xls.sheet_by_index(0)
        return sheet.col_values(0)[1:]

    @staticmethod
    def get_distance(*arg):
        if len(arg) == 1:
            return None
        elif len(arg) == 2:
            return [{
                "di": Distance.di({
                    "longitude": arg[0]["long"],
                    "latitude": arg[0]["short"]
                }, {
                    "longitude": arg[1]["long"],
                    "latitude": arg[1]["short"]
                }),
                "type": arg[0]["batch_name"] + '-' + arg[1]["batch_name"]
            }]
        elif len(arg) == 3:
            return [
                {
                    "di": Distance.di({
                        "longitude": arg[0]["long"],
                        "latitude": arg[0]["short"]
                    }, {
                        "longitude": arg[1]["long"],
                        "latitude": arg[1]["short"]
                    }),
                    "type": arg[0]["batch_name"] + '-' + arg[1]["batch_name"]
                },
                {
                    "di": Distance.di({
                        "longitude": arg[0]["long"],
                        "latitude": arg[0]["short"]
                    }, {
                        "longitude": arg[2]["long"],
                        "latitude": arg[2]["short"]
                    }),
                    "type": arg[0]["batch_name"] + '-' + arg[2]["batch_name"]
                },
                {
                    "di": Distance.di({
                        "longitude": arg[1]["long"],
                        "latitude": arg[1]["short"]
                    }, {
                        "longitude": arg[2]["long"],
                        "latitude": arg[2]["short"]
                    }),
                    "type": arg[1]["batch_name"] + '-' + arg[2]["batch_name"]
                }
            ]
