import time
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
import os
import subprocess

# Define the repository path
repo_path = r'C:\Users\Administrator\groceries\grocery_prices'
os.chdir(repo_path)

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

    # Run the Aldi spider with arbitrary start_url and total_pages
    aldi_start_url = 'https://new.aldi.us/products/fresh-produce/k/13'
    aldi_total_pages = 7
    p3 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p3.start()
    p3.join()

    aldi_start_url = 'https://new.aldi.us/products/bakery-bread/k/6'
    aldi_total_pages = 6
    p4 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p4.start()
    p4.join()

    aldi_start_url = 'https://new.aldi.us/products/pantry-essentials/k/16'
    aldi_total_pages = 25
    p5 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p5.start()
    p5.join()

    aldi_start_url = 'https://new.aldi.us/products/fresh-meat-seafood/k/12'
    aldi_total_pages = 7
    p6 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p6.start()
    p6.join()

    aldi_start_url = 'https://new.aldi.us/products/dairy-eggs/k/10'
    aldi_total_pages = 13
    p7 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p7.start()
    p7.join()

    aldi_start_url = 'https://new.aldi.us/products/frozen-foods/k/14'
    aldi_total_pages = 13
    p8 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p8.start()
    p8.join()

    aldi_start_url = 'https://new.aldi.us/products/breakfast-cereals/k/9'
    aldi_total_pages = 7
    p9 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p9.start()
    p9.join()

    aldi_start_url = 'https://new.aldi.us/products/snacks/k/20'
    aldi_total_pages = 19
    p10 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p10.start()
    p10.join()

    aldi_start_url = 'https://new.aldi.us/products/beverages/k/7'
    aldi_total_pages = 13
    p11 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p11.start()
    p11.join()

    aldi_start_url = 'https://new.aldi.us/products/deli/k/11'
    aldi_total_pages = 10
    p12 = multiprocessing.Process(target=run_spider, args=('aldi', raw_output_file, aldi_start_url, aldi_total_pages))
    p12.start()
    p12.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/283?brand_names=wegmans'
    weg_total_pages = 31
    p13 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p13.start()
    p13.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/74?brand_names=wegmans'
    weg_total_pages = 8
    p14 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p14.start()
    p14.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/151?brand_names=wegmans'
    weg_total_pages = 6
    p15 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p15.start()
    p15.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/1?brand_names=wegmans'
    weg_total_pages = 3
    p16 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p16.start()
    p16.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/215?brand_names=wegmans'
    weg_total_pages = 9
    p17 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p17.start()
    p17.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/260?brand_names=wegmans'
    weg_total_pages = 9
    p18 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p18.start()
    p18.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/18?brand_names=wegmans'
    weg_total_pages = 7
    p19 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p19.start()
    p19.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/75?tags=usa_snap_eligible'
    weg_total_pages = 3
    p20 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p20.start()
    p20.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/456?tags=usa_snap_eligible'
    weg_total_pages = 5
    p21 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p21.start()
    p21.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/283?brand_names=wegmans'
    weg_total_pages = 31
    p22 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p22.start()
    p22.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/74?brand_names=wegmans'
    weg_total_pages = 8
    p23 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p23.start()
    p23.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/151?brand_names=wegmans'
    weg_total_pages = 6
    p24 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p24.start()
    p24.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/1?brand_names=wegmans'
    weg_total_pages = 3
    p25 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p25.start()
    p25.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/215?brand_names=wegmans'
    weg_total_pages = 9
    p26 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p26.start()
    p26.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/260?brand_names=wegmans'
    weg_total_pages = 9
    p27 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p27.start()
    p27.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/18?brand_names=wegmans'
    weg_total_pages = 7
    p28 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p28.start()
    p28.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/75?tags=usa_snap_eligible'
    weg_total_pages = 3
    p29 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p29.start()
    p29.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/456?tags=usa_snap_eligible'
    weg_total_pages = 5
    p30 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p30.start()
    p30.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/283?brand_names=wegmans'
    weg_total_pages = 31
    p31 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p31.start()
    p31.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/74?brand_names=wegmans'
    weg_total_pages = 8
    p32 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p32.start()
    p32.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/151?brand_names=wegmans'
    weg_total_pages = 6
    p33 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p33.start()
    p33.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/1?brand_names=wegmans'
    weg_total_pages = 3
    p34 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p34.start()
    p34.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/215?brand_names=wegmans'
    weg_total_pages = 9
    p35 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p35.start()
    p35.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/260?brand_names=wegmans'
    weg_total_pages = 9
    p36 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p36.start()
    p36.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/18?brand_names=wegmans'
    weg_total_pages = 7
    p37 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p37.start()
    p37.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/75?tags=usa_snap_eligible'
    weg_total_pages = 3
    p38 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p38.start()
    p38.join()

    weg_start_url = 'https://shop.wegmans.com/shop/categories/456?tags=usa_snap_eligible'
    weg_total_pages = 5
    p39 = multiprocessing.Process(target=run_spider, args=('wegmans', raw_output_file, weg_start_url, weg_total_pages))
    p39.start()
    p39.join()

    # # After scraping, run the cleaning script
    # subprocess.run(['python', 'clean_data.py', 'prices.csv', 'clean.csv'])

    # After scraping, run the cleaning script
    subprocess.run(['python', 'clean_data.py', raw_output_file, cleaned_output_file])

