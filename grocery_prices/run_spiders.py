import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider(spider_name, output_file):
    settings = get_project_settings()
    settings.set('FEEDS', {
        output_file: {
            'format': 'csv',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
            'indent': 4,
        },
    })
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()

if __name__ == "__main__":
    output_file = 'prices.csv'

    # Run the first spider
    run_spider('walmart', output_file)

    # Introduce a delay (e.g., 5 minutes)
    time.sleep(300)  # 300 seconds = 5 minutes

    # Run the second spider
    run_spider('walmart2', output_file)