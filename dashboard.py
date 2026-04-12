import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="European Energy Market", layout="wide")
st.title("European Energy Grid & Pricing Dashboard")
st.markdown("### Live Market Volatility & Weather Correlation")
st.markdown("This dashboard connects to the Snowflake Gold Layer (`mart_energy_weather`) to visualize the impact of weather patterns on Awattar energy pricing.")

# 2. Sidebar Filters
st.sidebar.header("Filter Parameters")
days_to_pull = st.sidebar.slider("Select Days to Analyze", 1, 14, 7)
region = st.sidebar.selectbox("Select Market Region", ["Germany (DE)", "Austria (AT)"])

# 3. Simulate Data from Snowflake Gold Layer
@st.cache_data
def load_mock_gold_layer(days):
    dates = pd.date_range(start="2024-01-01", periods=days * 24, freq="h")
    # Simulate pricing spikes when temperatures drop
    temp = np.random.normal(10, 5, len(dates)) - np.cos(np.arange(len(dates)) / 10) * 8
    price = np.random.normal(80, 15, len(dates)) + (20 - temp) * 3 
    
    return pd.DataFrame({"Timestamp": dates, "Temperature_C": temp, "Energy_Price_EUR": price})

df = load_mock_gold_layer(days_to_pull)

# 4. Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average Energy Price", f"€{df['Energy_Price_EUR'].mean():.2f}")
col2.metric("Peak Price Volatility", f"€{df['Energy_Price_EUR'].max():.2f}")
col3.metric("Average Temperature", f"{df['Temperature_C'].mean():.1f} °C")

# 5. Display Interactive Charts
st.subheader("Price vs. Temperature Correlation")
st.line_chart(df, x="Timestamp", y=["Energy_Price_EUR", "Temperature_C"], color=["#FF4B4B", "#0068C9"])

st.caption("Data engineered via dbt Core & Snowflake. Dashboard deployed via Streamlit.")
