import streamlit as st
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# Function to read and concatenate all CSV files in the folder
def load_data(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    df_list = []
    for file in all_files:
        df = pd.read_csv(file)
        # Extract date from filename assuming format cleaned_prices-YYYY-MM-DD.csv
        date_str = os.path.basename(file).split('-')[1:]
        date_str = '-'.join(date_str).split('.')[0]
        df['date'] = pd.to_datetime(date_str)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

# Load data
data_folder = './data/cleaned_prices/'
df = load_data(data_folder)

# Streamlit app
st.title('Historical Prices Dashboard')

# Sidebar for selections
st.sidebar.title('Filter Options')

# Date selection
start_date = st.sidebar.date_input('Start Date:', df['date'].min())
end_date = st.sidebar.date_input('End Date:', df['date'].max())

# Category selection
categories = st.sidebar.multiselect('Select Category:', ['All'] + list(df['category'].unique()))

# Filter alt names based on selected categories
if 'All' in categories or not categories:
    filtered_alt_names = df['alt_name'].unique()
else:
    filtered_alt_names = df[df['category'].isin(categories)]['alt_name'].unique()

# Alt name selection
alt_names = st.sidebar.multiselect('Select Grocery Item:', filtered_alt_names)

# Filter data based on selections
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
if 'All' not in categories and categories:
    filtered_df = filtered_df[filtered_df['category'].isin(categories)]
if alt_names:
    filtered_df = filtered_df[filtered_df['alt_name'].isin(alt_names)]

# Plotting
fig, ax = plt.subplots()
for alt_name in alt_names:
    item_df = filtered_df[filtered_df['alt_name'] == alt_name]
    ax.plot(item_df['date'], item_df['price'], marker='o', label=alt_name)

ax.set_title('Price Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Price in Dollars')
ax.set_ylim(bottom=0)  # Start y-axis at 0
plt.xticks(rotation=45)
ax.legend(title='Grocery Item')
st.pyplot(fig)