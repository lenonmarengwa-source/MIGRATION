import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Zimbabwe Migration Risk", layout="wide")

st.title("🌍 Zimbabwe Bayesian Migration Risk Model")
st.markdown("**Supporting National Migration Strategy & Vision 2030**")

# Sidebar
with st.sidebar:
    st.selectbox("Language", ["English", "Shona", "Ndebele"])
    scenario = st.selectbox("Scenario", ["Baseline", "High Climate Impact", "Economic Boom", "Policy Intervention"])

# Data
data = pd.DataFrame({
    "Province": ["Harare", "Bulawayo", "Manicaland", "Masvingo", "Midlands", "Matabeleland North"],
    "Migration Risk": [0.78, 0.45, 0.71, 0.65, 0.59, 0.48],
    "Risk": ["High", "Medium", "High", "High", "Medium", "Medium"]
})

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(px.bar(data, x="Province", y="Migration Risk", color="Risk", title="Migration Risk by Province"), use_container_width=True)

with col2:
    m = folium.Map(location=[-19.0, 29.5], zoom_start=6)
    st_folium(m, width=400, height=500)

if st.button("Generate Policy Brief"):
    st.success("✅ Report Generated!")
    st.download_button("Download PDF", "Policy recommendations for Zimbabwe migration...", "Zimbabwe_Migration_Brief.pdf")
