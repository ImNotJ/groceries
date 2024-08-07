import scrapy

class GroceryPriceItem(scrapy.Item):
    store = scrapy.Field()
    item_name = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()