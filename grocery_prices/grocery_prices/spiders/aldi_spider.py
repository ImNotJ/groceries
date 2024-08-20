import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class AldiSpider(scrapy.Spider):
    name = 'aldi'

    def __init__(self, start_url=None, total_pages=1, *args, **kwargs):
        super(AldiSpider, self).__init__(*args, **kwargs)
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.start_url = start_url
        self.total_pages = int(total_pages)
        # Initialize the driver in the constructor, keeping it for the entire session
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def start_requests(self):
        if not self.start_url:
            logging.error("No start URL provided.")
            return

        # First request to the specific link
        yield scrapy.Request(url=self.start_url, callback=self.parse, meta={'page': 1, 'total_pages': self.total_pages})

    def parse(self, response):
        # Reuse the same driver instance
        try:
            self.driver.get(response.url)
            # Allow JavaScript to load content
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

            # Handle pagination if there are more pages to scrape
            current_page = response.meta['page']
            total_pages = response.meta['total_pages']
            next_page = current_page + 1

            # Check if there are more pages to scrape
            if next_page <= total_pages:
                # Construct the next page URL
                base_url = self.start_url.split('?')[0] + '?page={page}'
                next_url = base_url.format(page=next_page)

                # Make a new request for the next page
                yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': next_page, 'total_pages': total_pages})

        finally:
            # Ensure the driver is closed after the spider finishes
            self.driver.quit()

    def closed(self, reason):
        # Ensure the driver quits if the spider is closed unexpectedly
        if self.driver:
            self.driver.quit()
