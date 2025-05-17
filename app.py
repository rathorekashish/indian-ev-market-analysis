import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("indian_ev_market_2001_2024.csv")

df = load_data()

# Title
st.title("🇮🇳 Indian Electric Vehicle Market Dashboard (2001 - 2024)")

# Summary metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("2024 EV Sales", f"{df[df['Year']==2024]['Total_EV_Sales'].values[0]:,}")
col2.metric("Market Penetration (2024)", f"{df[df['Year']==2024]['EV_Market_Penetration_%'].values[0]}%")
col3.metric("2W Sales in 2024", f"{df[df['Year']==2024]['EV_2W_Sales'].values[0]:,}")

# Line chart: EV Sales over time
st.subheader("📈 EV Sales Over Time")
fig = px.line(df, x="Year", y=["EV_2W_Sales", "EV_3W_Sales", "EV_4W_Sales", "EV_Bus_Sales"],
              labels={"value": "Sales", "variable": "EV Type"},
              title="EV Segment-wise Sales (2001-2024)")
st.plotly_chart(fig, use_container_width=True)

# Area chart: Total EV sales
st.subheader("📊 Total EV Sales Growth")
fig_area = px.area(df, x="Year", y="Total_EV_Sales",
                   title="Total EV Sales in India (2001-2024)",
                   labels={"Total_EV_Sales": "Total Sales"})
st.plotly_chart(fig_area, use_container_width=True)

# Bar chart: Market penetration
st.subheader("📉 EV Market Penetration")
fig_bar = px.bar(df, x="Year", y="EV_Market_Penetration_%",
                 title="EV Market Penetration % Over the Years",
                 labels={"EV_Market_Penetration_%": "Market Share (%)"})
st.plotly_chart(fig_bar, use_container_width=True)

# Policy Timeline
st.subheader("📌 Government Policies Timeline")
st.dataframe(df[['Year', 'Govt_Policy']][df['Govt_Policy'] != "None"].reset_index(drop=True))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name] | Data from simulated estimates based on public reports")
