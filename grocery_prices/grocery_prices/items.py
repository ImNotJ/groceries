# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GroceryPricesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    store = scrapy.Field()
    item_name = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    
