import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Indian EV Dashboard", page_icon="⚡", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("indian_ev_market_2001_2024.csv")

df = load_data()

# Sidebar - Navigation & Theme
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["📊 Overview", "📈 Trends", "📍 Insights", "✉️ Feedback"])

theme = st.sidebar.selectbox("🎨 Theme", ["Dark", "Light"])
plotly_theme = "plotly_dark" if theme == "Dark" else "plotly_white"

# Title
st.markdown(
    f"""
    <style>
    .title {{
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: {"white" if theme == "Dark" else "#000000"};
    }}
    .subtitle {{
        text-align: center;
        color: #888;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='title'>⚡ Indian Electric Vehicle Market Dashboard (2001 - 2024) 🚗⚡</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Tracking the rise of EVs across India using interactive insights</div>", unsafe_allow_html=True)

# Page Routing
if page == "📊 Overview":
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("2024 EV Sales", f"{df[df['Year'] == 2024]['Total_EV_Sales'].values[0]:,}")
    col2.metric("Market Penetration (2024)", f"{df[df['Year'] == 2024]['EV_Market_Penetration_%'].values[0]}%")
    col3.metric("2W Sales in 2024", f"{df[df['Year'] == 2024]['EV_2W_Sales'].values[0]:,}")

    st.subheader("📌 Government Policies Timeline")
    st.dataframe(df[['Year', 'Govt_Policy']][df['Govt_Policy'] != "None"].reset_index(drop=True))

elif page == "📈 Trends":
    # EV type filter
    st.subheader("🔧 Filter by EV Type")
    ev_types = ["EV_2W_Sales", "EV_3W_Sales", "EV_4W_Sales", "EV_Bus_Sales"]
    selected_types = st.multiselect("Select EV Types", ev_types, default=ev_types)

    # Line chart
    st.subheader("📈 EV Sales Over Time by Segment")
    if selected_types:
        fig_line = px.line(df, x="Year", y=selected_types,
                           labels={"value": "Sales", "variable": "EV Type"},
                           title="EV Segment-wise Sales (2001-2024)",
                           template=plotly_theme)
        st.plotly_chart(fig_line, use_container_width=True)

    # Donut chart for 2024 sales
    st.subheader("🍩 EV Sales Breakdown (2024)")
    donut_df = df[df["Year"] == 2024][ev_types].melt(var_name="EV Type", value_name="Sales")
    fig_donut = px.pie(donut_df, names="EV Type", values="Sales", hole=0.4,
                       title="EV Sales Share by Segment (2024)",
                       template=plotly_theme)
    st.plotly_chart(fig_donut, use_container_width=True)

    # Area chart
    st.subheader("🚀 Total EV Sales Growth")
    fig_area = px.area(df, x="Year", y="Total_EV_Sales",
                       title="Total EV Sales in India (2001-2024)",
                       labels={"Total_EV_Sales": "Total Sales"},
                       template=plotly_theme)
    st.plotly_chart(fig_area, use_container_width=True)

    # Market Penetration
    st.subheader("📉 EV Market Penetration Over Years")
    fig_bar = px.bar(df, x="Year", y="EV_Market_Penetration_%",
                     title="EV Market Share % (2001-2024)",
                     labels={"EV_Market_Penetration_%": "Market Share (%)"},
                     template=plotly_theme)
    st.plotly_chart(fig_bar, use_container_width=True)

elif page == "📍 Insights":
    st.subheader("💡 Key Insights")
    st.markdown("""
    - 🚀 **2-Wheelers dominate** EV adoption in India.
    - 🔋 **Sharp rise after 2018**, thanks to better policy and awareness.
    - 🏙️ **Urban areas** lead the EV market, while rural EV adoption is slowly increasing.
    - 📈 **Market Penetration reached its peak** in 2024.
    - ⚙️ Government initiatives (like FAME II) **boosted growth significantly**.
    """)

elif page == "✉️ Feedback":
    st.subheader("📬 We'd love your feedback!")

    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        comment = st.text_area("Your Comments")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success(f"✅ Thanks {name}! Your feedback has been recorded.")

# Footer
st.markdown("---")
st.markdown("👤 Made with ❤️ by **Kashish Rathore**")
