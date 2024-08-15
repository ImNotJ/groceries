# Grocery Prices Project

## Overview

The Grocery Prices Project is a comprehensive tool designed to track and analyze the prices of common household groceries from three major stores: Wegmans, Walmart, and Aldi. This project leverages web scraping, data cleaning, and a Streamlit app to present the data in an accessible and informative manner. The project aims to provide insights into price trends, inflation, and the Consumer Price Index (CPI) for groceries.

The app is deployed at [https://grocery-prices.streamlit.app/](https://grocery-prices.streamlit.app/) deployed using GitHub Actions with a continuous integration and deployment pipeline on the Streamlit Cloud.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Data Sources](#data-sources)
3. [Data Pipeline](#data-pipeline)
4. [Running the Project](#running-the-project)
5. [Streamlit App](#streamlit-app)
6. [Libraries Used](#libraries-used)
7. Deployment
8. Contributing

## Project Structure

```
grocery_prices/
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── scripts/
│   ├── scrape_wegmans.py
│   ├── scrape_walmart.py
│   ├── scrape_aldi.py
│   └── clean_data.py
│
├── grocery_prices/
│   ├── __init__.py
│   ├── item_mapping.py
│   └── app.py
│
├── .github/
│   └── workflows/
│       └── scrape_and_deploy.yml
│
├── requirements.txt
├── README.md
└── setup.py
```

## Data Sources

The data is scraped from the following stores:
- **Wegmans**
- **Walmart**
- **Aldi**

Approximately 100 items are tracked in each store, consisting of common household groceries from apples to frozen pizza. The data focuses on store brand products and non-organic items whenever possible for consistency. Items are tracked per unit of weight to ensure standardization across products.

## Data Pipeline

### 1. Scraping

The data is scraped using custom Python scripts located in the `scripts/` directory:
- `scrape_wegmans.py`
- `scrape_walmart.py`
- `scrape_aldi.py`

These scripts extract the latest prices for the tracked items and save the raw data in the `data/raw/` directory.

### 2. Cleaning

The raw data is cleaned using the `clean_data.py` script. This script performs several operations:
- Removes rows with missing or invalid item names.
- Cleans and standardizes item names and prices.
- Splits price per unit into separate columns.
- Filters and maps items based on the `item_mapping.py` file.

The cleaned data is saved in the `data/cleaned/` directory.

### 3. Processing

The cleaned data is further processed to calculate inflation and CPI metrics. This processed data is used by the Streamlit app to provide insights and visualizations.

### 4. Presentation

The processed data is presented using a Streamlit app (`app.py`). The app provides an interactive interface for users to explore price trends, inflation, and CPI metrics.

## Running the Project

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/grocery-prices.git
   cd grocery-prices
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Scraping Scripts

To run the scraping scripts manually:
```bash
python scripts/scrape_wegmans.py
python scripts/scrape_walmart.py
python scripts/scrape_aldi.py
```

### Running the Cleaning Script

To clean the scraped data:
```bash
python scripts/clean_data.py data/raw/ data/cleaned/
```

### Running the Streamlit App

To run the Streamlit app locally:
```bash
streamlit run grocery_prices/app.py
```

## Streamlit App

The Streamlit app provides an interactive interface to explore the grocery price data. It includes features such as:
- Viewing price trends for individual items.
- Comparing prices across different stores.
- Calculating inflation and CPI metrics.

The app is deployed at [https://grocery-prices.streamlit.app/](https://grocery-prices.streamlit.app/).

## Libraries Used

- **Pandas**: Data manipulation and analysis.
- **Requests**: HTTP requests for web scraping.
- **BeautifulSoup**: Parsing HTML for web scraping.
- **Streamlit**: Building the interactive web app.
- **re**: Regular expressions for data cleaning.
- **sys**: System-specific parameters and functions.

## Deployment

The project is deployed using Streamlit Cloud. The scraping scripts are scheduled to run automatically at 6 AM EST using GitHub Actions. The CI/CD pipeline is defined in the `.github/workflows/scrape_and_deploy.yml` file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
