import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Function to read and concatenate all CSV files in the folder
def load_data(data_folder):
    # Convert to absolute path
    data_folder = os.path.abspath(data_folder)
    
    # Print the current working directory and data folder path for debugging
    print("Current working directory:", os.getcwd())
    print("Data folder path:", data_folder)
    
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"The directory {data_folder} does not exist.")
    
    df_list = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_folder, filename)
            print(f"Loading file: {file_path}")  # Debugging statement
            df = pd.read_csv(file_path)
            df_list.append(df)
    
    if not df_list:
        raise ValueError("No CSV files found in the data folder.")
    
    return pd.concat(df_list, ignore_index=True)

# Example usage
data_folder = "./grocery_prices/data/cleaned_prices/"
df = load_data(data_folder)

# Ensure 'date' column is in datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
else:
    raise KeyError("Column 'date' does not exist in the DataFrame.")

# Debugging statement to inspect DataFrame columns
print("DataFrame columns:", df.columns)

# Check if 'price_per_unit' column exists
if 'price_per_unit' in df.columns:
    df['price_per_unit'] = df['price_per_unit'].fillna(df['price'])
else:
    print("Column 'price_per_unit' does not exist in the DataFrame.")

# Create a column for the legend with alt_name and ppu_unit
df['alt_name_with_unit_legend'] = df.apply(lambda row: f"{row['alt_name']} ({row['ppu_unit']})", axis=1)

# Create a column for the legend with store name and ppu_unit
df['store_with_unit_legend'] = df.apply(
    lambda row: f"{row['store']} ({row['ppu_unit']})" if pd.notna(row['ppu_unit']) and row['ppu_unit'] != 'N/A' else row['store'], 
    axis=1
)

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
    start_date = st.sidebar.date_input('Start Date:', df['date'].min().date())
    end_date = st.sidebar.date_input('End Date:', df['date'].max().date())

    # Category selection
    categories = st.sidebar.multiselect('Select Category:', sorted(df['category'].unique()))

    # Filter alt names based on selected categories
    if categories:
        filtered_alt_names = sorted(df[df['category'].isin(categories)]['alt_name'].unique())
    else:
        filtered_alt_names = sorted(df['alt_name'].unique())

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
            filtered_df = filtered_df[filtered_df['alt_name'].isin(alt_names)]

        # Plotting with Plotly
        if not filtered_df.empty:
            if len(selected_stores) > 1:
                fig = px.line(filtered_df, x='date', y='price_per_unit', color='store_with_unit_legend', 
                              labels={'price_per_unit': 'Price per Unit', 'date': 'Date'},
                              hover_data={'price_per_unit': True, 'ppu_unit': True})
            else:
                fig = px.line(filtered_df, x='date', y='price_per_unit', color='alt_name_with_unit_legend', 
                              labels={'price_per_unit': 'Price per Unit', 'date': 'Date'},
                              hover_data={'price_per_unit': True, 'ppu_unit': True})

            # Customize hover template to show price per unit and unit
            fig.update_traces(hovertemplate='<b>%{y}</b>')

            fig.update_layout(title='Price Over Time', yaxis_title='Price (USD)', xaxis_title='Date', yaxis_range=[0, None], legend_title_text='')

            # Display the plot
            st.plotly_chart(fig)

            # Calculate inflation and CPI for each store
            st.markdown("### Inflation and CPI")
            for store in selected_stores:
                store_df = filtered_df[filtered_df['store'] == store]
                start_price = store_df[store_df['date'] == store_df['date'].min()]['price_per_unit'].mean()
                end_price = store_df[store_df['date'] == store_df['date'].max()]['price_per_unit'].mean()
                inflation = ((end_price - start_price) / start_price) * 100
                cpi = (end_price / start_price) * 100

                # Determine the color and arrow for inflation
                if inflation > 0:
                    inflation_color = "red"
                    inflation_arrow = "↑"
                else:
                    inflation_color = "green"
                    inflation_arrow = "↓"

                # Display inflation and CPI for each store with custom styling
                st.markdown(f"<h3 style='font-size:24px;'>&nbsp;&nbsp;&nbsp;&nbsp;{store}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Inflation: <span style='color:{inflation_color};'>{inflation:.2f}% {inflation_arrow}</span></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CPI: <span>{cpi:.2f}</span></p>", unsafe_allow_html=True)

            # How to use the graph and the Streamlit dashboard
            st.sidebar.markdown("### How to Use the Graph and Dashboard:")
            st.sidebar.markdown("""
            - **Select Store:** Choose one or more stores from the list to filter the data.
            - **Select Date Range:** Use the date inputs to select the start and end dates for the data you want to view.
            - **Select Category:** Choose one or more categories to filter the items displayed.
            - **Select Grocery Item:** Select multiple stores to compare one grocery item, or one store to compare multiple grocery items. 
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

            # Link to GitHub repository
            st.sidebar.markdown("### Learn More:")
            st.sidebar.markdown("[My Github Repository](https://github.com/ImNotJ/groceries)")

            
        else:
            st.write("No data available for the selected filters.")
    else:
        st.write("Please select at least one category or grocery item to display data.")