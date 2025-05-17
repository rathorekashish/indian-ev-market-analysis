import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# Page config
st.set_page_config(page_title="Indian EV Dashboard", page_icon="⚡", layout="wide")

# Load Lottie animation from URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_car = load_lottieurl("https://lottie.host/3a3ff95e-e148-48cb-9d93-4a91e16f65cd/vZwYqv7iGj.json")

# Custom CSS styles
st.markdown(
    """
    <style>
    .title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #31333f;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.1em;
        text-align: center;
        color: #5c5e66;
        margin-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and animation
st.markdown("<div class='title'>⚡ Indian Electric Vehicle Market Dashboard (2001 - 2024)</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Tracking the rise of EVs across India using interactive insights</div>", unsafe_allow_html=True)
st_lottie(lottie_car, height=200, speed=1, loop=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("indian_ev_market_2001_2024.csv")

df = load_data()

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
              title="EV Segment-wise Sales (2001-2024)",
              template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Area chart: Total EV sales
st.subheader("📊 Total EV Sales Growth")
fig_area = px.area(df, x="Year", y="Total_EV_Sales",
                   title="Total EV Sales in India (2001-2024)",
                   labels={"Total_EV_Sales": "Total Sales"},
                   template="plotly_dark")
st.plotly_chart(fig_area, use_container_width=True)

# Bar chart: Market penetration
st.subheader("📉 EV Market Penetration")
fig_bar = px.bar(df, x="Year", y="EV_Market_Penetration_%",
                 title="EV Market Penetration % Over the Years",
                 labels={"EV_Market_Penetration_%": "Market Share (%)"},
                 template="plotly_dark")
st.plotly_chart(fig_bar, use_container_width=True)

# Policy Timeline
st.subheader("📌 Government Policies Timeline")
st.dataframe(df[['Year', 'Govt_Policy']][df['Govt_Policy'] != "None"].reset_index(drop=True))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by **Kashish Rathore**")


