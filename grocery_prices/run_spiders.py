import time
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import os
import subprocess

def run_spider(spider_name, output_file, start_url=None, total_pages=None):
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
    if start_url and total_pages:
        process.crawl(spider_name, start_url=start_url, total_pages=total_pages)
    else:
        process.crawl(spider_name)
    process.start()

if __name__ == "__main__":
    # Get the current date in the desired format
    date_str = datetime.now().strftime('%Y-%m-%d')

    # Define the output file paths
    raw_output_file = f'./data/prices/prices-{date_str}.csv'
    cleaned_output_file = f'./data/cleaned_prices/cleaned_prices-{date_str}.csv'

    # Ensure the directories exist
    os.makedirs('./data/prices', exist_ok=True)
    os.makedirs('./data/cleaned_prices', exist_ok=True)

    # # Run the first spider in a separate process
    # p1 = multiprocessing.Process(target=run_spider, args=('walmart', raw_output_file))
    # p1.start()
    # p1.join()

    # # Introduce a delay (e.g., 5 minutes)
    # time.sleep(300)  # 300 seconds = 5 minutes

    # # Run the second spider in a separate process
    # p2 = multiprocessing.Process(target=run_spider, args=('walmart2', raw_output_file))
    # p2.start()
    # p2.join()

    # # Run the Aldi spider with arbitrary start_url and total_pages
    # aldi_start_url = 'https://new.aldi.us/products/fresh-produce/k/13'
    # aldi_total_pages = 7
    # p3 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p3.start()
    # p3.join()

    # aldi_start_url = 'https://new.aldi.us/products/bakery-bread/k/6'
    # aldi_total_pages = 6
    # p4 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p4.start()
    # p4.join()

    # aldi_start_url = 'https://new.aldi.us/products/pantry-essentials/k/16'
    # aldi_total_pages = 25
    # p5 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p5.start()
    # p5.join()

    # aldi_start_url = 'https://new.aldi.us/products/fresh-meat-seafood/k/12'
    # aldi_total_pages = 7
    # p6 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p6.start()
    # p6.join()

    # aldi_start_url = 'https://new.aldi.us/products/dairy-eggs/k/10'
    # aldi_total_pages = 13
    # p7 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p7.start()
    # p7.join()

    # aldi_start_url = 'https://new.aldi.us/products/frozen-foods/k/14'
    # aldi_total_pages = 13
    # p8 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p8.start()
    # p8.join()

    # aldi_start_url = 'https://new.aldi.us/products/breakfast-cereals/k/9'
    # aldi_total_pages = 7
    # p9 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p9.start()
    # p9.join()

    # aldi_start_url = 'https://new.aldi.us/products/snacks/k/20'
    # aldi_total_pages = 19
    # p10 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p10.start()
    # p10.join()

    # aldi_start_url = 'https://new.aldi.us/products/beverages/k/7'
    # aldi_total_pages = 13
    # p11 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p11.start()
    # p11.join()

    # aldi_start_url = 'https://new.aldi.us/products/deli/k/11'
    # aldi_total_pages = 10
    # p12 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    # p12.start()
    # p12.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/283?brand_names=wegmans'
    # weg_total_pages = 31
    # p13 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p13.start()
    # p13.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/74?brand_names=wegmans'
    # weg_total_pages = 8
    # p14 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p14.start()
    # p14.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/151?brand_names=wegmans'
    # weg_total_pages = 6
    # p15 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p15.start()
    # p15.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/1?brand_names=wegmans'
    # weg_total_pages = 3
    # p16 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p16.start()
    # p16.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/215?brand_names=wegmans'
    # weg_total_pages = 9
    # p17 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p17.start()
    # p17.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/260?brand_names=wegmans'
    # weg_total_pages = 9
    # p18 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p18.start()
    # p18.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/18?brand_names=wegmans'
    # weg_total_pages = 7
    # p19 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p19.start()
    # p19.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/75?tags=usa_snap_eligible'
    # weg_total_pages = 3
    # p20 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p20.start()
    # p20.join()

    # weg_start_url = 'https://shop.wegmans.com/shop/categories/456?tags=usa_snap_eligible'
    # weg_total_pages = 5
    # p21 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    # p21.start()
    # p21.join()

    # # After scraping, run the cleaning script
    # subprocess.run(['python', 'clean_data.py', 'prices.csv', 'clean.csv'])

    # After scraping, run the cleaning script
    subprocess.run(['python', 'clean_data.py', raw_output_file, cleaned_output_file])

