import pandas as pd
import numpy as np
import arviz as az
import geopandas as gpd

trace = az.from_netcdf("zimbabwe_migration_trace.nc")
data = pd.read_csv("zimbabwe_district_data.csv")
gdf = gpd.read_file("zimbabwe_districts.shp")

def simulate_counterfactual(trace, X, scenario="irrigation", strength=0.7):
    """Multiple intervention scenarios"""
    X_cf = X.copy()
    
    if scenario == "irrigation":
        X_cf[:, 0] *= strength          # Reduce drought effect
    elif scenario == "education":
        X_cf[:, 3] += 0.5 * strength    # Improve education index
    elif scenario == "conflict_reduction":
        X_cf[:, 4] *= (1 - 0.4 * strength)  # Reduce conflict
    elif scenario == "economic_boost":
        X_cf[:, 1] += 0.6 * strength    # Increase night lights
    
    # Compute counterfactual predictions
    mu_cf = (trace.posterior["mu_global"].mean() +
             trace.posterior["province_effect"].mean(dim=["chain","draw"]).values[data['province_idx']] +
             trace.posterior["phi"].mean(dim=["chain","draw"]).values[data['district_idx']] +
             trace.posterior["time_effect"].mean(dim=["chain","draw"]).values[data['year_idx']] +
             np.dot(X_cf, trace.posterior["beta"].mean(dim=["chain","draw"]).values))
    
    reduction = np.mean(y - mu_cf)
    return mu_cf, reduction

# Example scenarios
scenarios = ["irrigation", "education", "conflict_reduction", "economic_boost"]
for sc in scenarios:
    _, red = simulate_counterfactual(trace, X, sc, 0.75)
    print(f"{sc.replace('_', ' ').title()}: Avg Migration Reduction = {red:.3f}")