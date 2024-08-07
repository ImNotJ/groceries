import scrapy

class GroceryPriceItem(scrapy.Item):
    store = scrapy.Field()
    item_name = scrapy.Field()
    sale_price = scrapy.Field()
    price = scrapy.Field()
    price_per_unit = scrapy.Field()
    date = scrapy.Field()