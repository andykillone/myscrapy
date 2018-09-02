# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MyspiderPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient()
        db = client["soufangdb"]
        self.table = db["soufangtable1"]

    def process_item(self, item, spider):

        self.table.insert(dict(item))
        return item
