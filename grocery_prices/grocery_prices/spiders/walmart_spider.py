import scrapy
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class WalmartSpider(scrapy.Spider):
    name = 'walmart'
    start_urls = ['https://www.walmart.com/browse/976759?athcpid=7cbe8a0a-c5fe-4839-a851-edb3ec71638c&athpgid=AthenaContentPage&athznid=athenaModuleZone&athmtid=AthenaItemCarousel&athtvid=4&athena=true']

    def parse(self, response):
        logging.info("Parsing the response")
        products = response.css('div.search-result-gridview-item-wrapper')
        logging.info(f"Found {len(products)} products")
        
        for product in products:
            item = GroceryPriceItem()
            item['store'] = 'Walmart'
            item_name = product.css('a.product-title-link span::text').get()
            item['item_name'] = item_name.strip() if item_name else 'N/A'
            price_whole = product.css('span.price-main span.visuallyhidden::text').get()
            price_fraction = product.css('span.price-main span.price-characteristic::text').get()
            item['price'] = f"{price_whole}.{price_fraction}" if price_whole and price_fraction else 'N/A'
            item['date'] = datetime.now().strftime('%Y-%m-%d')
            logging.info(f"Scraped item: {item}")
            yield item

        # Follow pagination links
        next_page = response.css('a.paginator-btn-next::attr(href)').get()
        if next_page is not None:
            logging.info(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse)