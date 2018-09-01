# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    titles = scrapy.Field()
    prices = scrapy.Field()
    unitprices = scrapy.Field()
    housenames = scrapy.Field()
    houseinfos = scrapy.Field()
