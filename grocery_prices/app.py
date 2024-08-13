import streamlit as st
import pandas as pd
import os
import glob
import plotly.express as px

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

# Replace N/A in price_per_unit with price
df['price_per_unit'] = df['price_per_unit'].fillna(df['price'])

# Append unit to alt_name
df['alt_name_with_unit'] = df.apply(lambda row: f"{row['alt_name']} (/{row['ppu_unit']})" if pd.notna(row['ppu_unit']) else row['alt_name'], axis=1)

# Streamlit app
st.title('Historical Prices Dashboard')

# Sidebar for selections
st.sidebar.title('Filter Options')

# Store selection
stores = sorted(df['store'].unique())
selected_stores = st.sidebar.multiselect('Select Store:', stores)

if not selected_stores:
    st.write("Please select a store to begin.")
else:
    # Date selection
    start_date = st.sidebar.date_input('Start Date:', df['date'].min())
    end_date = st.sidebar.date_input('End Date:', df['date'].max())

    # Category selection
    categories = st.sidebar.multiselect('Select Category:', sorted(df['category'].unique()))

    # Filter alt names based on selected categories
    if categories:
        filtered_alt_names = sorted(df[df['category'].isin(categories)]['alt_name_with_unit'].unique())
    else:
        filtered_alt_names = sorted(df['alt_name_with_unit'].unique())

    # Alt name selection
    if len(selected_stores) > 1:
        alt_names = st.sidebar.selectbox('Select Grocery Item:', filtered_alt_names)
        alt_names = [alt_names]  # Convert to list for consistency
    else:
        alt_names = st.sidebar.multiselect('Select Grocery Item:', filtered_alt_names)

    # Filter data based on selections
    if categories or alt_names:
        filtered_df = df[(df['store'].isin(selected_stores)) & 
                         (df['date'] >= pd.to_datetime(start_date)) & 
                         (df['date'] <= pd.to_datetime(end_date))]
        if categories:
            filtered_df = filtered_df[filtered_df['category'].isin(categories)]
        if alt_names:
            filtered_df = filtered_df[filtered_df['alt_name_with_unit'].isin(alt_names)]

        # Plotting with Plotly
        if not filtered_df.empty:
            if len(selected_stores) > 1:
                fig = px.line(filtered_df, x='date', y='price_per_unit', color='store', 
                              labels={'price_per_unit': 'Price per Unit', 'date': 'Date'},
                              hover_data={'price_per_unit': True, 'ppu_unit': True})
            else:
                fig = px.line(filtered_df, x='date', y='price_per_unit', color='alt_name_with_unit', 
                              labels={'price_per_unit': 'Price per Unit', 'date': 'Date'},
                              hover_data={'price_per_unit': True, 'ppu_unit': True})

            # Customize hover template to show price per unit and unit
            fig.update_traces(hovertemplate='<b>%{y}</b>')

            fig.update_layout(title='Price Over Time', yaxis_title='Price (USD)', xaxis_title='Date', yaxis_range=[0, None], legend_title_text='')

            st.plotly_chart(fig)
        else:
            st.write("No data available for the selected filters.")
    else:
        st.write("Please select at least one category or grocery item to display data.")