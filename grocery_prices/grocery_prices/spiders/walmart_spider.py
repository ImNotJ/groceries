import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class WalmartSpider(scrapy.Spider):
    name = 'walmart'

    def __init__(self, *args, **kwargs):
        super(WalmartSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        start_url = 'https://www.walmart.com/browse/976759?page=4&affinityOverride=default'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        
        # Allow JavaScript to load content
        self.driver.implicitly_wait(10)

        sel = Selector(text=self.driver.page_source)

        products = sel.css('div.sans-serif')
        logging.info(f"Found {len(products)} products")

        for product in products:
            item = GroceryPriceItem()
            item['store'] = 'Walmart'
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
                price_per_unit = product.css('div[data-automation-id="product-price"] div.gray:last-of-type::text').get()
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

        # Follow pagination links
        next_page = sel.css('a[data-testid="NextPage"]::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            logging.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            logging.info("No next page found")

    def closed(self, reason):
        self.driver.quit()