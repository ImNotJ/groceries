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
            price_per_unit = round(price_per_unit, 3)
            ppu_unit = ppu_unit[2:]  # Remove "¢/"
            if ppu_unit.startswith("fl"):
                ppu_unit = "fl oz"
        elif ppu_unit.startswith("/"):
            ppu_unit = ppu_unit[1:]  # Remove "/"
        return pd.Series([price_per_unit, ppu_unit])
    return pd.Series([None, 'N/A'])

df[['price_per_unit', 'ppu_unit']] = df['price_per_unit'].apply(split_price_per_unit)

# Fill missing price_per_unit with 'N/A'
df['price_per_unit'].fillna('N/A', inplace=True)

# Remove the sale_price column
df.drop(columns=['sale_price'], inplace=True)

# Define the mapping for alt names and categories
item_mapping = {
    # Fresh Produce
    "Fresh Pink Lady Apple, Each": {"alt_name": "Apples", "category": "Fresh Produce"},
    "Fresh Banana Fruit, Each": {"alt_name": "Bananas", "category": "Fresh Produce"},
    "Fresh Strawberries, 1 lb Container": {"alt_name": "Strawberries", "category": "Fresh Produce"},
    "Fresh Hass Avocados, Each": {"alt_name": "Avocados", "category": "Fresh Produce"},
    "Fresh Color Bell Peppers, 3 Count": {"alt_name": "Bell Peppers", "category": "Fresh Produce"},
    "Fresh Whole Carrots, 1 lb Bag": {"alt_name": "Carrots", "category": "Fresh Produce"},
    "Fresh Broccoli Crowns, Each": {"alt_name": "Broccoli", "category": "Fresh Produce"},
    "Garlic Bulb Fresh Whole, Each": {"alt_name": "Garlic", "category": "Fresh Produce"},
    "Fresh Lemon, Each": {"alt_name": "Lemon", "category": "Fresh Produce"},
    "Fresh Lime, Each": {"alt_name": "Lime", "category": "Fresh Produce"},
    "Fresh Whole Yellow Onion, Each": {"alt_name": "Onion", "category": "Fresh Produce"},
    "Fresh Italian Parsley Bunch, Each": {"alt_name": "Parsley", "category": "Fresh Produce"},
    "Fresh Cilantro, Bunch": {"alt_name": "Cilantro", "category": "Fresh Produce"},
    "Fresh Organic Basil, 0.5 oz Clamshell": {"alt_name": "Basil", "category": "Fresh Produce"},
    "Russet Baking Potatoes Whole Fresh, Each": {"alt_name": "Potatoes", "category": "Fresh Produce"},
    "Marketside Fresh Spinach, 10 oz Bag, Fresh": {"alt_name": "Spinach", "category": "Fresh Produce"},
    "Fresh Slicing Tomato, Each": {"alt_name": "Tomatoes", "category": "Fresh Produce"},

    # Grains
    "Great Value Plain Bread Crumbs, 15 oz": {"alt_name": "Breadcrumbs", "category": "Grains"},
    "Great Value Penne Pasta, 16 oz Box, (Shelf Stable)": {"alt_name": "Pasta", "category": "Grains"},
    "Great Value Organic Tri-Color Quinoa, 16 oz": {"alt_name": "Quinoa", "category": "Grains"},
    "Great Value Long Grain Enriched Rice, 32 oz": {"alt_name": "Rice", "category": "Grains"},
    "Great Value White Sandwich Bread, 20 oz": {"alt_name": "Sandwich Bread", "category": "Grains"},
    "Great Value Medium Soft Taco Flour Tortillas, 16 oz, 10 Count": {"alt_name": "Tortillas", "category": "Grains"},

    # Meat/Protein
    "Great Value All Natural Boneless Skinless Chicken Breasts, 3 lb (Frozen)": {"alt_name": "Chicken", "category": "Meat/Protein"},
    "Great Value, Large White Eggs, 12 Count": {"alt_name": "Eggs", "category": "Meat/Protein"},
    "Great Value Roast Beef Lunchmeat, 7oz Plastic Tub, 10 G of Protein per 2 oz (56g) Serving": {"alt_name": "Beef", "category": "Meat/Protein"},
    "Great Value Thin Sliced Oven Roasted Turkey Breast Family Pack, 16 oz Plastic Tub, 9 Grams of Protein per 2 oz Serving": {"alt_name": "Turkey", "category": "Meat/Protein"},
    "Great Value Thin Sliced Black Forest Ham Lunchmeat, Family Pack, 1lb, Resealable Plastic Tub, 10 G of Protein per 2oz Serving": {"alt_name": "Ham", "category": "Meat/Protein"},

    # Dairy
    "Great Value Sweet Cream Unsalted Butter Sticks, 4 Count,16 oz": {"alt_name": "Butter", "category": "Dairy"},
    "Great Value Deli Style Sliced Non-Smoked Provolone Cheese, 8 oz, 12 Count": {"alt_name": "Sliced Cheese", "category": "Dairy"},
    "Great Value Finely Shredded Low-Moisture Part-Skim Mozzarella Cheese, 8 oz Bag": {"alt_name": "Shredded Cheese", "category": "Dairy"},
    "Great Value Mozzarella String Cheese Sticks, 12 oz Bag, 12 Count (Refrigerated)": {"alt_name": "String Cheese", "category": "Dairy"},
    "Great Value Milk 2% Reduced Fat Gallon Plastic Jug": {"alt_name": "Milk", "category": "Dairy"},
    "Great Value Original Sour Cream, 16 oz Tub": {"alt_name": "Sour Cream", "category": "Dairy"},
    "Great Value Greek Plain Nonfat Yogurt, 32 oz Tub": {"alt_name": "Greek Yogurt", "category": "Dairy"},

    # Baking Goods
    "Great Value Double Acting Baking Powder, 8.1 oz": {"alt_name": "Baking Powder", "category": "Baking Goods"},
    "Great Value Baking Soda, 1 Lb": {"alt_name": "Baking Soda", "category": "Baking Goods"},
    "Great Value Pure Granulated Sugar, 4 lb": {"alt_name": "Granulated Sugar", "category": "Baking Goods"},
    "Great Value Light Brown Sugar, 32 oz": {"alt_name": "Brown Sugar", "category": "Baking Goods"},
    "Great Value All-Purpose Enriched Flour, 5LB Bag": {"alt_name": "Flour", "category": "Baking Goods"},
    "Great Value Honey, 12 oz Plastic Bear": {"alt_name": "Honey", "category": "Baking Goods"},
    "Great Value Pure Vanilla Extract, 1 fl oz (Ambient, Plastic Container)": {"alt_name": "Vanilla Extract", "category": "Baking Goods"},
    "Great Value Active Dry Yeast, 0.25 oz, 3 Count": {"alt_name": "Dry Yeast", "category": "Baking Goods"},
    "Great Value Milk Chocolate Chips, 11.5 oz": {"alt_name": "Chocolate Chips", "category": "Baking Goods"},
    "Great Value Baking Unsweetened Cocoa Powder, 8 oz Tub": {"alt_name": "Cocoa Powder", "category": "Baking Goods"},
    "Great Value Confectioners Powdered Sugar, 32 oz": {"alt_name": "Powdered Sugar", "category": "Baking Goods"},

    # Frozen Goods
    "Great Value Frozen Whole Berry Medley, 16 oz": {"alt_name": "Frozen Fruit and Berries", "category": "Frozen Goods"},
    "Great Value Frozen Mixed Vegetables, 12 oz Steamable Bag": {"alt_name": "Frozen Veggies", "category": "Frozen Goods"},
    "Great Value Buttermilk Waffles, 24 Count": {"alt_name": "Waffle", "category": "Frozen Goods"},
    "Great Value Rising Crust Pepperoni Pizza, Marinara Sauce, 28.25 oz (Frozen)": {"alt_name": "Pizza", "category": "Frozen Goods"},
    "Great Value Traditional Pie Crusts, 9\", 2 Count (Frozen)": {"alt_name": "Pie Crust", "category": "Frozen Goods"},
    "Great Value Ready to Bake Regular Chocolate Chip Cookie Dough, 16.5 oz": {"alt_name": "Cookie Dough", "category": "Frozen Goods"},
    "Great Value Fully Cooked Chicken Nuggets 32oz Frozen": {"alt_name": "Chicken Nuggets", "category": "Frozen Goods"},

    # Sauces/Canned Goods
    "Great Value Meat-Based Chicken Broth, 32 oz Carton, Ready-to-Serve, Shelf-Stable/Ambient, Gluten-Free": {"alt_name": "Chicken Stock", "category": "Sauces/Canned Goods"},
    "Great Value Thick and Chunky Salsa Mild, 16 oz": {"alt_name": "Salsa", "category": "Sauces/Canned Goods"},
    "Great Value Diced Tomatoes in Tomato Juice, 14.5 oz Can": {"alt_name": "Diced Tomatoes", "category": "Sauces/Canned Goods"},
    "Great Value Concord Grape Jelly, 30 oz": {"alt_name": "Jelly", "category": "Sauces/Canned Goods"},
    "Great Value Creamy Peanut Butter, 16 oz": {"alt_name": "Peanut Butter", "category": "Sauces/Canned Goods"},
    "Great Value Traditional Pasta Sauce, 24 oz": {"alt_name": "Pasta Sauce", "category": "Sauces/Canned Goods"},
    "Great Value Alfredo Pasta Sauce, 16 Oz": {"alt_name": "Alfredo Sauce", "category": "Sauces/Canned Goods"},
    "Great Value, No Salt Added, Canned Black Beans, 15 oz Can": {"alt_name": "Black Beans", "category": "Sauces/Canned Goods"},
    "Great Value Tomato Condensed Soup, 10.75 oz": {"alt_name": "Soups", "category": "Sauces/Canned Goods"},
    "Great Value Chunk Light Tuna in Water, 5 oz, 4 Count": {"alt_name": "Tuna", "category": "Sauces/Canned Goods"},
    "Great Value Canned Medium Diced Green Chiles, 4 Oz": {"alt_name": "Green Chiles", "category": "Sauces/Canned Goods"},
    "Great Value Golden Sweet Whole Kernel Corn, Canned Corn, 15 oz Can": {"alt_name": "Green Chiles", "category": "Sauces/Canned Goods"},

    # Condiments/Spices
    "Great Value Ground Black Pepper, 3 oz": {"alt_name": "Black Pepper", "category": "Condiments/Spices"},
    "Great Value Chili Powder, 3 oz": {"alt_name": "Chili Powder", "category": "Condiments/Spices"},
    "Great Value Kosher Ground Cinnamon, 2.5 oz": {"alt_name": "Cinnamon", "category": "Condiments/Spices"},
    "Great Value Crushed Red Pepper, 1.75 oz": {"alt_name": "Red Pepper", "category": "Condiments/Spices"},
    "Great Value Ground Cumin, 2.5 oz": {"alt_name": "Cumin", "category": "Condiments/Spices"},
    "Great Value Garlic Powder, 3.4 oz": {"alt_name": "Garlic Powder", "category": "Condiments/Spices"},
    "Great Value Tomato Ketchup, 32 oz": {"alt_name": "Ketchup", "category": "Condiments/Spices"},
    "Great Value Yellow Mustard, 20 oz": {"alt_name": "Mustard", "category": "Condiments/Spices"},
    "Great Value Mayonnaise, 30 fl oz": {"alt_name": "Mayonnaise", "category": "Condiments/Spices"},
    "Great Value Ground Nutmeg, 1.5 oz": {"alt_name": "Nutmeg", "category": "Condiments/Spices"},
    "Great Value Paprika, 2.5 oz": {"alt_name": "Paprika", "category": "Condiments/Spices"},
    "Great Value Coarse Sea Salt, 17.6 oz": {"alt_name": "Sea Salt", "category": "Condiments/Spices"},
    "Morton Salt Coarse Kosher Salt – for Cooking, Grilling, Brining, & Salt Rimming, 16 oz": {"alt_name": "Kosher Salt", "category": "Condiments/Spices"},
    "Great Value Savory Steak Sauce, 10 oz": {"alt_name": "Steak Sauce", "category": "Condiments/Spices"},
    "Great Value Louisiana Hot Sauce, 12 fl oz": {"alt_name": "Hot Sauce", "category": "Condiments/Spices"},
    "Great Value Classic Ranch Salad Dressing & Dip, 16 fl oz": {"alt_name": "Ranch", "category": "Condiments/Spices"},
    "Great Value Traditional Italian Salad Dressing & Marinade, 16 fl oz": {"alt_name": "Salad Dressing", "category": "Condiments/Spices"},

    # Oils/Vinegars
    "Great Value Apple Cider Vinegar, 32 fl oz": {"alt_name": "Apple Cider Vinegar", "category": "Oils/Vinegars"},
    "Great Value Balsamic Vinegar of Modena, 8.45 fl oz": {"alt_name": "Balsamic Vinegar", "category": "Oils/Vinegars"},
    "Great Value Organic Unrefined Virgin Coconut Oil, 14 fl oz": {"alt_name": "Coconut Oil", "category": "Oils/Vinegars"},
    "Great Value 100% Extra Virgin Olive Oil, 25.5 fl oz": {"alt_name": "Olive Oil", "category": "Oils/Vinegars"},
    "Great Value Vegetable Oil, 48 fl oz": {"alt_name": "Vegetable Oil", "category": "Oils/Vinegars"},
    "Great Value Red Wine Vinegar, 12.7 fl oz": {"alt_name": "Red Wine Vinegar", "category": "Oils/Vinegars"},
    "Great Value Distilled White Vinegar, 32 fl oz": {"alt_name": "White Vinegar", "category": "Oils/Vinegars"},
    "Great Value White Wine Vinegar, 12.7 fl oz": {"alt_name": "White Wine Vinegar", "category": "Oils/Vinegars"},

    # Snacks
    "Great Value Saltine Crackers, 16 oz, 4 Count": {"alt_name": "Crackers", "category": "Snacks"},
    "Great Value Deluxe Mixed Nuts, 30 oz": {"alt_name": "Nuts", "category": "Snacks"},
    "Great Value Whole Grain Quick Rolled Oats": {"alt_name": "Quick Oats", "category": "Snacks"},
    "Great Value Extra Butter Flavored Microwave Popcorn, 2.55 oz, 12 Count": {"alt_name": "Popcorn", "category": "Snacks"},
    "Great Value Restaurant Style White Corn Tortilla Chips, 13 oz": {"alt_name": "Tortilla Chips", "category": "Snacks"},
    "Great Value Cinnamon Crunch Breakfast Cereal, 20.25 oz": {"alt_name": "Cereal", "category": "Snacks"},
    "Great Value Patties Shredded Seasoned Poatato Hash Brown": {"alt_name": "Hash Browns", "category": "Snacks"},

    # Beverages
    "Great Value 100% Apple Juice, 96 fl oz": {"alt_name": "Apple Juice", "category": "Beverages"},
    "Great Value 100% Pasteurized Orange Juice with No Pulp, 52 fl oz": {"alt_name": "Orange Juice", "category": "Beverages"},
    "Great Value Black Tea Bags, 8 oz, 100 Count": {"alt_name": "Tea Bags", "category": "Beverages"},
    "Great Value Classic Roast Ground Naturally Caffeinated Coffee, 40.3 oz Cannister": {"alt_name": "Coffee", "category": "Beverages"}
}


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
df_filtered.to_csv('cleaned_prices.csv', index=False)
