import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('prices.csv')

# Display the first few rows of the dataframe
print("Original Data:")
print(df.head())

# Example cleaning operations:
# 1. Remove rows with missing item names
df = df[df['item_name'].notna() & (df['item_name'] != 'N/A')]

# 2. Remove quotation marks from item names
df['item_name'] = df['item_name'].str.replace('"', '')

# 3. Convert price columns to numeric, handling non-numeric values
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 4. Fill missing prices with 0
df['price'].fillna(0, inplace=True)

# 5. Remove any duplicate rows
df.drop_duplicates(inplace=True)

# 6. Split price_per_unit into price_per_unit and ppu_unit
def split_price_per_unit(value):
    if pd.isna(value):
        return pd.Series([None, 'N/A'])
    match = re.match(r'^\$?(\d*\.?\d+)\s*(¢?\/?\s*\w+)', value)
    if match and '/' in value:
        price_per_unit = float(match.group(1))
        ppu_unit = match.group(2).strip()
        if ppu_unit.startswith("¢/"):
            price_per_unit /= 100
            ppu_unit = ppu_unit[2:]  # Remove "¢/"
        elif ppu_unit.startswith("/"):
            ppu_unit = ppu_unit[1:]  # Remove "/"
        return pd.Series([price_per_unit, ppu_unit])
    return pd.Series([None, 'N/A'])

df[['price_per_unit', 'ppu_unit']] = df['price_per_unit'].apply(split_price_per_unit)

# Fill missing price_per_unit with 'N/A'
df['price_per_unit'].fillna('N/A', inplace=True)

# Remove the sale_price column
df.drop(columns=['sale_price'], inplace=True)

# Display the cleaned data
print("Cleaned Data:")
print(df.head())

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_prices.csv', index=False)