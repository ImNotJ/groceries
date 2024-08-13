import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class AldiSpider(scrapy.Spider):
    name = 'aldi'

    def __init__(self, *args, **kwargs):
        super(AldiSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        # First request to the specific link
        initial_url = 'https://new.aldi.us/products/fresh-produce/fresh-fruit/k/89'
        yield scrapy.Request(url=initial_url, callback=self.parse, meta={'page': 1, 'total_pages': 1, 'initial': True})

    def parse(self, response):
        self.driver.get(response.url)
        
        # Allow JavaScript to load content
        self.driver.implicitly_wait(10) 

        sel = Selector(text=self.driver.page_source)

        products = sel.css('div.sans-serif')
        logging.info(f"Found {len(products)} products")

        for product in products:
            item = GroceryPriceItem()
            item['store'] = 'Aldi'
            item_name = product.css('span[data-automation-id="product-title"]::text').get()
            item['item_name'] = item_name.strip() if item_name else 'N/A'
            
            logging.info(f"Found product name: {item_name}")

            # Check for sale price
            sale_price_whole = product.css('div[data-automation-id="product-price"] span.f3::text').get()
            if sale_price_whole and sale_price_whole.strip().lower() == 'now':
                sale_price = product.css('div[data-automation-id="product-price"] span.w_iUH7::text').get()
                item['sale_price'] = sale_price.strip('current price Now $') if sale_price else 'N/A'
                original_price = product.css('div[data-automation-id="product-price"] div.gray.strike::text').get()
                item['price'] = original_price.strip('$') if original_price else 'N/A'
                price_per_unit = product.css('div[data-automation-id="product-price"] div.gray:nth-of-type(2)::text').get()                
                item['price_per_unit'] = price_per_unit.strip() if price_per_unit else 'N/A'
            else:
                item['sale_price'] = 'N/A'
                original_price = product.css('div[data-automation-id="product-price"] span.w_iUH7::text').get()
                item['price'] = original_price.strip('current price $') if original_price else 'N/A'
                price_per_unit = product.css('div[data-automation-id="product-price"] div.gray::text').get()
                item['price_per_unit'] = price_per_unit.strip() if price_per_unit else 'N/A'

            item['date'] = datetime.now().strftime('%Y-%m-%d')
            logging.info(f"Scraped item: {item}")
            yield item

        # Close the current browser window
        self.driver.quit()

        # Get the current page number and total pages from meta
        current_page = response.meta['page']
        total_pages = response.meta['total_pages']
        initial = response.meta.get('initial', False)

        # Increment the page number
        next_page = current_page + 1

        # # Check if there are more pages to scrape
        # if initial or next_page <= total_pages:
        #     # Introduce a delay before making the next request
        #     time.sleep(300)
            
        #     # Reinitialize the driver
        #     self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            
        #     # Construct the next page URL
        #     base_url = 'https://www.walmart.com/browse/food/great-value-food/976759_7128585_9834661?page={page}&affinityOverride=default'
        #     next_url = base_url.format(page=next_page)
            
        #     # Make a new request for the next page
        #     yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': next_page, 'total_pages': total_pages})

    def closed(self, reason):
        self.driver.quit()