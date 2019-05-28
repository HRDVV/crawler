# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
import codecs


class JsonExporterPipeline(object):
    # poi_long = scrapy.Field()
    # poi_short = scrapy.Field()
    # address = scrapy.Field()
    # desc = scrapy.Field()
    # batch_name = scrapy.Field()
    # batch_type = scrapy.Field()
    # batch_no = scrapy.Field()
    # field_list = ['batch_type', 'batch_no', 'batch_name', 'poi_long', 'poi_short', 'desc', 'address']

    def __init__(self):
        self.file = codecs.open('target/gps.json', 'wb')
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        # spider.compare_before_list.append(item)
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # new_compare_before_list = []
        # for item in new_compare_before_list:
        #     for item1 in spider.compare_before_list:
        #         if item["batch_no"] == item1["batch_no"]:
        #             item["poi"].append({
        #                 "map": item1["batch_name"],
        #                 "long": item1["poi_long"],
        #                 "short": item1["poi_short"],
        #                 "desc": item1["desc"]
        #             })
        #             item["distance"] = None
        #         else:
        #             new_compare_before_list.append({
        #                 "batch_no": item1["batch_no"],
        #                 "poi": [{
        #                     "map": item1["batch_name"],
        #                     "long": item1["poi_long"],
        #                     "short": item1["poi_short"],
        #                     "desc": item1["desc"]
        #                 }],
        #                 "distance": None,
        #                 "address": item1["address"]
        #             })
        #
        # for item2 in new_compare_before_list:
        #     self.exporter.export_item(item2)
        self.exporter.finish_exporting()
        self.file.close()
        spider.logger.info("=====爬虫结束=====")
