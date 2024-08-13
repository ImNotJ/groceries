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

            # Display the plot
            st.plotly_chart(fig)

            # Calculate inflation and CPI
            start_price = filtered_df[filtered_df['date'] == filtered_df['date'].min()]['price_per_unit'].mean()
            end_price = filtered_df[filtered_df['date'] == filtered_df['date'].max()]['price_per_unit'].mean()
            inflation = ((end_price - start_price) / start_price) * 100
            cpi = (end_price / start_price) * 100

            # Display inflation and CPI
            st.markdown("### Inflation and CPI")
            st.markdown(f"**Inflation:** {inflation:.2f}%")
            st.markdown(f"**CPI:** {cpi:.2f}")

            # How to use the graph and the Streamlit dashboard
            st.sidebar.markdown("### How to Use the Graph and Dashboard:")
            st.sidebar.markdown("""
            - **Select Store:** Choose one or more stores from the list to filter the data.
            - **Select Date Range:** Use the date inputs to select the start and end dates for the data you want to view.
            - **Select Category:** Choose one or more categories to filter the items displayed.
            - **Select Grocery Item:** Depending on the number of stores selected, choose a specific grocery item to view its price history.
            - **View Graph:** The graph will display the price history of the selected items over the chosen date range.
            - **Inflation and CPI:** Below the graph, you will see the calculated inflation and CPI based on the selected filters.
            """)
            
            # Display inflation and CPI
            st.sidebar.markdown("### About Inflation and CPI")
            # Description of inflation and CPI
            st.sidebar.markdown("""
            **Inflation:** The percentage increase in the price of the selected item or category over the selected date range.
            
            **CPI (Consumer Price Index):** A measure that examines the weighted average of prices of the selected item or category relative to the base period (start date).
            """)

            # Description of the data
            st.sidebar.markdown("### About the Data:")
            st.sidebar.markdown("""
            The data is sourced from the respective stores' websites in Cary, NC. The items selected for data scraping are store brand items unless no store brand item for that grocery item exists, in which case the name brand item is used. The prices listed do not include sale prices and also list price per weight or price per unit if provided on the website for standardization across stores.
            """)

            
        else:
            st.write("No data available for the selected filters.")
    else:
        st.write("Please select at least one category or grocery item to display data.")