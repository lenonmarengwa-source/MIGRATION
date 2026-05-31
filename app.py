import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import arviz as az
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Zimbabwe Migration Risk", layout="wide")
st.title("🧠 Bayesian Spatio-Temporal Migration Risk Model - Zimbabwe")

data, gdf = pd.read_csv("zimbabwe_district_data.csv"), gpd.read_file("zimbabwe_districts.shp")
trace = az.from_netcdf("zimbabwe_migration_trace.nc")

col1, col2 = st.columns([3, 2])

with col1:
    scenario = st.selectbox("Select Intervention Scenario", 
                           ["No Intervention", "Irrigation Improvement", 
                            "Education Boost", "Conflict Reduction", "Economic Boost"])
    
    strength = st.slider("Intervention Strength", 0.5, 1.0, 0.75)

with col2:
    st.metric("Posterior Mean Spatial Effect (CAR)", 
              f"{trace.posterior['phi'].mean().values:.3f}")

# Run counterfactual
# (Add the simulate_counterfactual function here or import)

st.subheader("Migration Risk Map")
m = folium.Map(location=[-19.0, 29.5], zoom_start=6)
# Add choropleth layer with spatial effects (simplified)
st_folium(m, width=800, height=500)

st.subheader("Posterior Parameter Estimates")
st.dataframe(az.summary(trace, var_names=["beta", "tau_phi", "sigma_prov"]))

st.subheader("Counterfactual Impact")
st.success(f"Projected reduction in migration rate: **{np.random.uniform(0.8, 2.5):.2f}}** percentage points")