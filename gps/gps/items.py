# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GpsItem(scrapy.Item):
    poi_long = scrapy.Field()
    poi_short = scrapy.Field()
    address = scrapy.Field()
    desc = scrapy.Field()
    batch_name = scrapy.Field()
    batch_type = scrapy.Field()
    batch_no = scrapy.Field()

