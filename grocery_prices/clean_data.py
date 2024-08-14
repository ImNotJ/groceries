import pandas as pd
import re
import sys
from item_mapping import item_mapping

def clean_data(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Display the first few rows of the dataframe
    print("Original Data:")
    print(df.head())

    # Example cleaning operations:
    # 1. Remove rows with missing item names
    df = df[df['item_name'].notna() & (df['item_name'] != 'N/A')]

    # 2. Remove quotation marks from item names
    # df['item_name'] = df['item_name'].str.replace('"', '') 

    # 3. Trim " /ea" from the end of the price for Wegmans
    df.loc[df['store'] == 'Wegmans', 'price'] = df.loc[df['store'] == 'Wegmans', 'price'].str.replace(' /ea', '')

    # 4. Convert price columns to numeric, handling non-numeric values
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 5. Fill missing prices with 0
    df['price'].fillna(0, inplace=True)

    # 6. Remove any duplicate rows
    df.drop_duplicates(inplace=True)

    # 7. Clean item names for Aldi: replace multiple spaces with a single space
    df.loc[df['store'] == 'Aldi', 'item_name'] = df.loc[df['store'] == 'Aldi', 'item_name'].str.replace(r'\s+', ' ', regex=True)

    # 8. Split price_per_unit into price_per_unit and ppu_unit for Walmart
    def split_price_per_unit_walmart(value):
        if pd.isna(value):
            return pd.Series([None, 'N/A'])
        match = re.match(r'^\$?(\d*\.?\d+)\s*(¢?\/?\s*\w+)', value)
        if match and '/' in value:
            price_per_unit = float(match.group(1))
            ppu_unit = match.group(2).strip()
            if ppu_unit.startswith("¢/"):
                price_per_unit /= 100
                price_per_unit = round(price_per_unit, 3)
                ppu_unit = ppu_unit[2:]  # Remove "¢/"
                if ppu_unit.startswith("fl"):
                    ppu_unit = "fl oz"
            elif ppu_unit.startswith("/"):
                ppu_unit = ppu_unit[1:]  # Remove "/"
            return pd.Series([price_per_unit, ppu_unit])
        return pd.Series([None, 'N/A'])

    # 9. Split price_per_unit into price_per_unit and ppu_unit for Aldi
    def split_price_per_unit_aldi(value, price):
        if pd.isna(value):
            return pd.Series([None, 'N/A'])
        match = re.match(r'avg\.\s*(\d*\.?\d+)\s*(\w+)', value)
        if match:
            quantity = float(match.group(1))
            unit = match.group(2).strip()
            price_per_unit = round(price / quantity, 3)
            if unit.startswith("fl"):
                unit = "fl oz"
            return pd.Series([price_per_unit, unit])
        match = re.match(r'(\d*\.?\d+)\s*(\w+)', value)
        if match:
            quantity = float(match.group(1))
            unit = match.group(2).strip()
            price_per_unit = round(price / quantity, 3)
            if unit.startswith("fl"):
                unit = "fl oz"
            return pd.Series([price_per_unit, unit])
        return pd.Series([price, 'N/A'])

    # 10. Split price_per_unit into price_per_unit and ppu_unit for Wegmans
    def split_price_per_unit_wegmans(value):
        if pd.isna(value):
            return pd.Series([None, 'N/A'])
        match = re.search(r'\$(\d*\.?\d+)\s*\/?\s*(\w+)', value)
        if match:
            price_per_unit = float(match.group(1))
            ppu_unit = match.group(2).strip()
            if ppu_unit.startswith("fl"):
                ppu_unit = "fl oz"
            return pd.Series([price_per_unit, ppu_unit])
        return pd.Series([None, 'N/A'])

    # Apply the appropriate function based on the store name
    df[['price_per_unit', 'ppu_unit']] = df.apply(
        lambda row: split_price_per_unit_walmart(row['price_per_unit']) if row['store'] == 'Walmart' else (
            split_price_per_unit_aldi(row['price_per_unit'], row['price']) if row['store'] == 'Aldi' else split_price_per_unit_wegmans(row['price_per_unit'])
        ),
        axis=1
    )

    # Fill missing price_per_unit with 'N/A'
    df['price_per_unit'].fillna('N/A', inplace=True)

    # Keep only the item with the highest price for each item_name
    df = df.loc[df.groupby('item_name')['price'].idxmax()]

    # Remove the sale_price column
    df.drop(columns=['sale_price'], inplace=True)

    # Filter the DataFrame to keep only the specified items
    filtered_items = list(item_mapping.keys())
    df_filtered = df[df['item_name'].isin(filtered_items)]

    # Add alt_name and category columns
    df_filtered['alt_name'] = df_filtered['item_name'].map(lambda x: item_mapping[x]['alt_name'])
    df_filtered['category'] = df_filtered['item_name'].map(lambda x: item_mapping[x]['category'])

    # Display the cleaned and filtered data
    print("Filtered and Cleaned Data:")
    print(df_filtered.head())

    # Save the cleaned and filtered data to a new CSV file
    df_filtered.to_csv(output_file, index=False) 

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    clean_data(input_file, output_file)