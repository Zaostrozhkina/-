# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksparserItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    main_price = scrapy.Field()
    discount_price = scrapy.Field()
    currency = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()

