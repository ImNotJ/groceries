import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class Aldi2Spider(scrapy.Spider):
    name = 'aldi2'

    def __init__(self, *args, **kwargs):
        super(Aldi2Spider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        # First request to the specific link
        initial_url = 'https://new.aldi.us/products/bakery-bread/k/6'
        yield scrapy.Request(url=initial_url, callback=self.parse, meta={'page': 1, 'total_pages': 6, 'initial': True})

    def parse(self, response):
        self.driver.get(response.url)

        # Allow JavaScript to load contents
        self.driver.implicitly_wait(10)

        sel = Selector(text=self.driver.page_source)

        products = sel.css('a.base-link.product-tile__content.product-tile__link')
        logging.info(f"Found {len(products)} products")

        for product in products:
            item = GroceryPriceItem()
            item['store'] = 'Aldi'
            
            # Extract item name
            item_name = product.css('div.product-tile__name p::text').get()
            item['item_name'] = item_name.strip() if item_name else 'N/A'
            
            logging.info(f"Found product name: {item_name}")

            # Extract original price
            original_price = product.css('span.base-price__regular span:first-child::text').get()
            item['price'] = original_price.strip('$') if original_price else 'N/A'

            # Extract price per unit
            price_per_unit = product.css('div.product-detail::text').get()
            item['price_per_unit'] = price_per_unit.strip('()').strip() if price_per_unit else 'N/A'

            # Default sale price to 'N/A' since no sale indicator is given
            item['sale_price'] = 'N/A'

            item['date'] = datetime.now().strftime('%Y-%m-%d')

            logging.info(f"Scraped item: {item}")
            yield item

        # Close the current browser window
        self.driver.quit()

        # Handle pagination if there are more pages to scrape
        current_page = response.meta['page']
        total_pages = response.meta['total_pages']
        initial = response.meta.get('initial', False)
        next_page = current_page + 1

        # Check if there are more pages to scrape
        if initial or next_page <= total_pages:
            # # Introduce a delay before making the next request
            # time.sleep(300)
            
            # Reinitialize the driver
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

            # Construct the next page URL
            base_url = 'https://new.aldi.us/products/bakery-bread/k/6?page={page}'
            next_url = base_url.format(page=next_page)

            # Make a new request for the next page
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': next_page, 'total_pages': total_pages})

    def closed(self, reason):
        self.driver.quit()

