# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def clear_price(value):
    if value:
        value = value.replace(' ', '')
        try:
            value = int(value)
        except:
            return value
        return value

def clear_spec(value):
    if value:
        value = value.replace('   ', '')
        value = value.replace('\n', '')
    return value

class CastoramaparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    spec_name = scrapy.Field(input_processor=MapCompose(clear_spec))
    spec_value = scrapy.Field(input_processor=MapCompose(clear_spec))
    spec = scrapy.Field()
    _id = scrapy.Field()
