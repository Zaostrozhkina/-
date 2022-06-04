# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        item['main_price'] = self.process_main_price(item['main_price'])
        item['discount_price'] = self.process_discount_price(item['discount_price'])
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_main_price(self, main_price):
        if main_price:
            main_price = int(main_price)
        else:
            main_price = 'Нет в продаже'
        return main_price

    def process_discount_price(self, discount_price):
        if discount_price:
            discount_price = int(discount_price)
        else:
            discount_price = 'Нет в продаже'
        return discount_price


