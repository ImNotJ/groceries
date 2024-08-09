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

# 2. Convert price columns to numeric, handling non-numeric values
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['sale_price'] = pd.to_numeric(df['sale_price'], errors='coerce')

# 3. Fill missing prices with 0
df['price'].fillna(0, inplace=True)
df['sale_price'].fillna(0, inplace=True)

# 4. Remove any duplicate rows
df.drop_duplicates(inplace=True)

# 5. Split price_per_unit into price_per_unit and ppu_unit
def split_price_per_unit(value):
    if pd.isna(value):
        return pd.Series([None, 'N/A'])
    match = re.match(r'^\$?(\d*\.?\d+)\s*(¢?\/?\s*\w+)', value)
    if match and '/' in value:
        price_per_unit = float(match.group(1))
        ppu_unit = match.group(2).strip()
        return pd.Series([price_per_unit, ppu_unit])
    return pd.Series([None, 'N/A'])

df[['price_per_unit', 'ppu_unit']] = df['price_per_unit'].apply(split_price_per_unit)

# Fill missing price_per_unit with 'N/A'
df['price_per_unit'].fillna('N/A', inplace=True)

# Display the cleaned data
print("Cleaned Data:")
print(df.head())

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_prices.csv', index=False)