import time
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import os
import subprocess

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
    # Get the current date in the desired format
    date_str = datetime.now().strftime('%Y-%m-%d')

    # Define the output file paths
    raw_output_file = f'./data/prices/prices-{date_str}.csv'
    cleaned_output_file = f'./data/cleaned_prices/cleaned_prices-{date_str}.csv'

    # Ensure the directories exist
    os.makedirs('/prices', exist_ok=True)
    os.makedirs('/cleaned_prices', exist_ok=True)

    # Run the first spider in a separate process
    p1 = multiprocessing.Process(target=run_spider, args=('walmart', raw_output_file))
    p1.start()
    p1.join()

    # Introduce a delay (e.g., 5 minutes)
    time.sleep(300)  # 300 seconds = 5 minutes

    # Run the second spider in a separate process
    p2 = multiprocessing.Process(target=run_spider, args=('walmart2', raw_output_file))
    p2.start()
    p2.join()

    # After scraping, run the cleaning script
    subprocess.run(['python', 'clean_data.py', raw_output_file, cleaned_output_file])

