import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

# ========================= DATA LOADING & PREPROCESSING =========================
print("Loading data...")
data = pd.read_csv("zimbabwe_district_data.csv")
gdf = gpd.read_file("zimbabwe_districts.shp")

data = data.merge(gdf[['district_name', 'province', 'geometry']], 
                  left_on='district', right_on='district_name')

# Adjacency Matrix for CAR
def create_adjacency_matrix(gdf):
    n = len(gdf)
    W = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if gdf.geometry.iloc[i].touches(gdf.geometry.iloc[j]):
                W[i, j] = W[j, i] = 1
    return W

W = create_adjacency_matrix(gdf)
n_districts = W.shape[0]

# Indices
data = data.sort_values(['province', 'district', 'year'])
data['district_idx'] = data['district'].astype('category').cat.codes
data['province_idx'] = data['province'].astype('category').cat.codes
data['year_idx'] = data['year'] - data['year'].min()

# Handle Missing Data (Explicit Imputation in Model)
features = ['spei_drought', 'night_lights', 'ag_yield', 'education_index', 'conflict_index']
for col in features:
    if col in data.columns:
        data[col] = data[col].fillna(data[col].median())

X = data[features].values
scaler = StandardScaler()
X = scaler.fit_transform(X)

y = data['migration_rate'].values

print(f"Districts: {n_districts} | Provinces: {data['province'].nunique()} | Years: {data['year'].nunique()}")

# ========================= BAYESIAN HIERARCHICAL CAR MODEL =========================
with pm.Model() as model:
    # Global
    mu_global = pm.Normal("mu_global", 0, 2)
    sigma = pm.HalfNormal("sigma", 2)
    
    # Hierarchical Province Effect
    sigma_prov = pm.HalfNormal("sigma_prov", 1)
    province_effect = pm.Normal("province_effect", 0, sigma_prov, 
                              shape=data['province'].nunique())
    
    # CAR Spatial Effect
    tau_phi = pm.Gamma("tau_phi", 1, 1)
    phi = pm.CAR("phi", W=W, alpha=0.95, tau=tau_phi, shape=n_districts)
    
    # Temporal Effect
    sigma_time = pm.HalfNormal("sigma_time", 1)
    time_effect = pm.RandomWalk("time_effect", sigma=sigma_time, 
                              shape=data['year_idx'].max() + 1)
    
    # Fixed Effects
    beta = pm.Normal("beta", 0, 1, shape=len(features))
    
    # Linear Predictor
    mu = (mu_global +
          province_effect[data['province_idx'].values] +
          phi[data['district_idx'].values] +
          time_effect[data['year_idx'].values] +
          pm.math.dot(X, beta))
    
    # Likelihood
    obs = pm.StudentT("obs", nu=4, mu=mu, sigma=sigma, observed=y)

    # Sampling
    trace = pm.sample(draws=2000, tune=1500, target_accept=0.93, 
                     chains=2, cores=2, return_inferencedata=True)

# Save trace
az.to_netcdf(trace, "zimbabwe_migration_trace.nc")
print("Model sampling completed and saved.")

# ========================= POSTERIOR PREDICTIVE CHECKS =========================
with model:
    ppc = pm.sample_posterior_predictive(trace)

print("Posterior Predictive Check Summary:")
az.plot_ppc(ppc, num_pp_samples=100)
plt.title("Posterior Predictive Check")
plt.show()