import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from grocery_prices.items import GroceryPriceItem
from datetime import datetime
import logging

class AldiSpider(scrapy.Spider):
    name = 'aldi'

    def __init__(self, start_url=None, total_pages=1, *args, **kwargs):
        super(AldiSpider, self).__init__(*args, **kwargs)
        self.start_url = start_url
        self.total_pages = int(total_pages)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        if not self.start_url:
            logging.error("No start URL provided.")
            return

        # First request to the specific link
        yield scrapy.Request(url=self.start_url, callback=self.parse, meta={'page': 1, 'total_pages': self.total_pages, 'initial': True})

    def parse(self, response):
        self.driver.get(response.url)

        # Press Escape key to close any potential menu
        try:
            body = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            body.send_keys(Keys.ESCAPE)
            logging.info("Pressed Escape to close any potential menu.")
        except Exception as e:
            logging.info("No menu to close or failed to press Escape.")

        # Additional fixed delay to ensure all content is loaded
        time.sleep(2)

        # Scroll down incrementally to load all items
        scroll_pause_time = 2  # Time to wait for the page to load after each scroll
        increment = 500  # Number of pixels to scroll down each time
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script(f"window.scrollBy(0, {increment});")
            time.sleep(scroll_pause_time)  # Wait for new items to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Allow JavaScript to load content
        self.driver.implicitly_wait(10)

        sel = Selector(text=self.driver.page_source)

        # Correct selector for the product tiles
        products = sel.css('div.product-tile')
        logging.info(f"Found {len(products)} products")

        for product in products:
            item = GroceryPriceItem()
            item['store'] = 'Aldi'
            
            # Extract item name
            item_name = product.css('div.product-tile__name p::text').get()
            item['item_name'] = item_name.strip() if item_name else 'N/A'
            
            logging.info(f"Found product name: {item_name}")

            # Extract original price
            original_price = product.css('span.base-price__regular span::text').get()
            item['price'] = original_price.strip('$') if original_price else 'N/A'

            # Extract price per unit
            price_per_unit = product.css('div.product-tile__unit-of-measurement p::text').get()
            item['price_per_unit'] = price_per_unit.strip() if price_per_unit else 'N/A'

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

            # Navigate to the next page using the existing WebDriver instance
            self.driver.get(next_url)

            # Make a new request for the next page
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'page': next_page, 'total_pages': total_pages})

    def closed(self, reason):
        self.driver.quit()