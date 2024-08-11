import time
import multiprocessing
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

    # Run the first spider in a separate process
    p1 = multiprocessing.Process(target=run_spider, args=('walmart', output_file))
    p1.start()
    p1.join()

    # Introduce a delay (e.g., 5 minutes)
    time.sleep(300)  # 300 seconds = 5 minutes

    # Run the second spider in a separate process
    p2 = multiprocessing.Process(target=run_spider, args=('walmart2', output_file))
    p2.start()
    p2.join()