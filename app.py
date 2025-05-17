import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Indian EV Dashboard", page_icon="⚡", layout="wide")

# Sidebar: Theme selector
theme = st.sidebar.selectbox("🎨 Select Theme", ["Dark", "Light"])
plotly_theme = "plotly_dark" if theme == "Dark" else "plotly_white"

# Custom title styling
st.markdown(
    f"""
    <style>
    .title {{
        font-size: 2.8em;
        font-weight: 900;
        text-align: center;
        color: {"white" if theme == "Dark" else "#000000"};
        margin-bottom: 0px;
    }}
    .subtitle {{
        font-size: 1.2em;
        text-align: center;
        color: #999999;
        margin-top: 0px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title section
st.markdown("<div class='title'>⚡ Indian Electric Vehicle Market Dashboard (2001 - 2024) 🚗⚡</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Tracking the rise of EVs across India using interactive insights</div>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("indian_ev_market_2001_2024.csv")

df = load_data()

# Summary metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("2024 EV Sales", f"{df[df['Year'] == 2024]['Total_EV_Sales'].values[0]:,}")
col2.metric("Market Penetration (2024)", f"{df[df['Year'] == 2024]['EV_Market_Penetration_%'].values[0]}%")
col3.metric("2W Sales in 2024", f"{df[df['Year'] == 2024]['EV_2W_Sales'].values[0]:,}")

# Line chart: EV segment sales
st.subheader("📈 EV Sales Over Time by Segment")
fig_line = px.line(df, x="Year", y=["EV_2W_Sales", "EV_3W_Sales", "EV_4W_Sales", "EV_Bus_Sales"],
                   labels={"value": "Sales", "variable": "EV Type"},
                   title="EV Segment-wise Sales (2001-2024)",
                   template=plotly_theme)
st.plotly_chart(fig_line, use_container_width=True)

# Area chart: Total sales
st.subheader("🚀 Total EV Sales Growth")
fig_area = px.area(df, x="Year", y="Total_EV_Sales",
                   title="Total EV Sales in India (2001-2024)",
                   labels={"Total_EV_Sales": "Total Sales"},
                   template=plotly_theme)
st.plotly_chart(fig_area, use_container_width=True)

# Bar chart: Market penetration
st.subheader("📉 EV Market Penetration")
fig_bar = px.bar(df, x="Year", y="EV_Market_Penetration_%",
                 title="EV Market Penetration % Over the Years",
                 labels={"EV_Market_Penetration_%": "Market Share (%)"},
                 template=plotly_theme)
st.plotly_chart(fig_bar, use_container_width=True)

# Policy table
st.subheader("📌 Government Policies Timeline")
st.dataframe(df[['Year', 'Govt_Policy']][df['Govt_Policy'] != "None"].reset_index(drop=True))

# Footer
st.markdown("---")
st.markdown("👤 Made with ❤️ by **Kashish Rathore**")
