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
        start_url = 'https://www.walmart.com/browse/976759?athcpid=7cbe8a0a-c5fe-4839-a851-edb3ec71638c&athpgid=AthenaContentPage&athznid=athenaModuleZone&athmtid=AthenaItemCarousel&athtvid=4&athena=true&page=3&affinityOverride=default'
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
                sale_price_whole = product.css('div[data-automation-id="product-price"] span.f2::text').get()
                sale_price_fraction = product.css('div[data-automation-id="product-price"] span.f6.f5-l:not([style*="margin-right:2px"])::text').get()
                item['sale_price'] = f"{sale_price_whole}.{sale_price_fraction}" if sale_price_whole and sale_price_fraction else 'N/A'
                original_price = product.css('div[data-automation-id="product-price"] div.gray.strike::text').get()
                item['price'] = original_price.strip() if original_price else 'N/A'
                price_per_unit = product.css('div[data-automation-id="product-price"] div.gray:last-of-type::text').get()
                item['price_per_unit'] = price_per_unit.strip() if price_per_unit else 'N/A'
            else:
                sale_price_whole = None
                sale_price_fraction = None
                item['sale_price'] = 'N/A'
                price_whole = product.css('div[data-automation-id="product-price"] span.f2::text').get()
                price_fraction = product.css('div[data-automation-id="product-price"] span.f6.f5-l:not([style*="margin-right:2px"])::text').get()
                item['price'] = f"{price_whole}.{price_fraction}" if price_whole and price_fraction else 'N/A'
                price_per_unit = product.css('div[data-automation-id="product-price"] div.gray::text').get()
                item['price_per_unit'] = price_per_unit.strip() if price_per_unit else 'N/A'

            

            item['date'] = datetime.now().strftime('%Y-%m-%d')
            logging.info(f"Scraped item: {item}")
            yield item

        # Follow pagination links
        next_page = sel.css('a.paginator-btn-next::attr(href)').get()
        if next_page is not None:
            logging.info(f"Following next page: {next_page}")
            yield response.follow(next_page, self.parse)
        else:
            logging.info("No next page found")

    def closed(self, reason):
        self.driver.quit()

