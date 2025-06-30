import streamlit as st; import pandas as pd; st.title('SF Airbnb Explorer'); df = pd.read_csv('listings.csv'); st.map(df)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title('🏠 SF Real Estate & Airbnb Price Explorer')

@st.cache_data
def load_data():
    data = pd.read_csv('listings.csv')
    data['price'] = data['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    data.dropna(subset=['latitude', 'longitude', 'neighbourhood_cleansed', 'price'], inplace=True)
    return data

df = load_data()

st.sidebar.header("Filters")
neighborhoods = sorted(df['neighbourhood_cleansed'].unique())
selected_neighborhoods = st.sidebar.multiselect(
    'Select Neighborhoods', options=neighborhoods, default=neighborhoods
)

min_price = int(df['price'].min())
max_price = int(df['price'].max())
if max_price > 1000:
    max_price = 1000

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=min_price, max_value=max_price, value=(min_price, max_price)
)

df_filtered = df[df['neighbourhood_cleansed'].isin(selected_neighborhoods)]
df_filtered = df_filtered[
    (df_filtered['price'] >= price_range[0]) & (df_filtered['price'] <= price_range[1])
]

st.header(f"Showing {len(df_filtered)} listings")

col1, col2 = st.columns(2)
average_price = df_filtered['price'].mean()
col1.metric("Average Price", f"${average_price:,.2f}")
col2.metric("Total Listings Found", f"{len(df_filtered):,}")

st.map(df_filtered)

if st.checkbox('Show Filtered Data Table'):
    st.write(df_filtered)
    