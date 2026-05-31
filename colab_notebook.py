"""
Google Colab Setup Notebook
Run this in Google Colab to fetch data, train model, and launch dashboard
"""

# ============================================================================
# CELL 1: Clone Repository & Install Dependencies
# ============================================================================

!git clone https://github.com/clairelenon62-beep/system.git
%cd system
!pip install -r requirements.txt -q

print("✓ Repository cloned and dependencies installed!")

# ============================================================================
# CELL 2: Fetch Data from Real Sources
# ============================================================================

!python fetch_data.py

print("\n✓ Data fetching complete!")

# ============================================================================
# CELL 3: Run Bayesian Migration Model
# ============================================================================

!python zimbabwe_migration_model.py 2>&1 | head -100

print("\n✓ Model training complete!")

# ============================================================================
# CELL 4: Verify Data & Explore Results
# ============================================================================

import pandas as pd
import numpy as np
import geopandas as gpd
import arviz as az
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("zimbabwe_district_data.csv")
gdf = gpd.read_file("zimbabwe_districts.shp")
trace = az.from_netcdf("zimbabwe_migration_trace.nc")

print("=" * 70)
print("DATA SUMMARY")
print("=" * 70)
print(f"\nDataset shape: {data.shape}")
print(f"Columns: {list(data.columns)}")
print(f"\nDistricts: {data['district'].nunique()}")
print(f"Years: {data['year'].min()}-{data['year'].max()}")
print(f"Provinces: {data['province'].nunique()}")

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)
print(data[['migration_rate', 'spei_drought', 'night_lights', 'ag_yield', 'education_index', 'conflict_index']].describe())

print("\n" + "=" * 70)
print("BAYESIAN MODEL - POSTERIOR SUMMARY")
print("=" * 70)
print(az.summary(trace, var_names=["beta", "mu_global", "sigma"]))

print("\n" + "=" * 70)
print("TOP 10 DISTRICTS BY AVERAGE MIGRATION RATE")
print("=" * 70)
top_migration = data.groupby('district')['migration_rate'].mean().sort_values(ascending=False).head(10)
print(top_migration)

# ============================================================================
# CELL 5: Visualize Results
# ============================================================================

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Migration Rate Distribution
axes[0, 0].hist(data['migration_rate'], bins=30, color='steelblue', edgecolor='black')
axes[0, 0].set_title('Migration Rate Distribution', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Migration Rate (%)')
axes[0, 0].set_ylabel('Frequency')

# Drought vs Migration
axes[0, 1].scatter(data['spei_drought'], data['migration_rate'], alpha=0.5, s=20)
axes[0, 1].set_title('Drought (SPEI) vs Migration Rate', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('SPEI Drought Index')
axes[0, 1].set_ylabel('Migration Rate (%)')

# Nighttime Lights vs Migration
axes[0, 2].scatter(data['night_lights'], data['migration_rate'], alpha=0.5, s=20, color='orange')
axes[0, 2].set_title('Nighttime Lights vs Migration Rate', fontsize=12, fontweight='bold')
axes[0, 2].set_xlabel('Night Lights (NOAA VIIRS)')
axes[0, 2].set_ylabel('Migration Rate (%)')

# Ag Yield vs Migration
axes[1, 0].scatter(data['ag_yield'], data['migration_rate'], alpha=0.5, s=20, color='green')
axes[1, 0].set_title('Agricultural Yield vs Migration Rate', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Ag Yield (kg/ha)')
axes[1, 0].set_ylabel('Migration Rate (%)')

# Education vs Migration
axes[1, 1].scatter(data['education_index'], data['migration_rate'], alpha=0.5, s=20, color='purple')
axes[1, 1].set_title('Education Index vs Migration Rate', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Education Index')
axes[1, 1].set_ylabel('Migration Rate (%)')

# Conflict vs Migration
axes[1, 2].scatter(data['conflict_index'], data['migration_rate'], alpha=0.5, s=20, color='red')
axes[1, 2].set_title('Conflict Index vs Migration Rate', fontsize=12, fontweight='bold')
axes[1, 2].set_xlabel('Conflict Events')
axes[1, 2].set_ylabel('Migration Rate (%)')

plt.tight_layout()
plt.savefig('migration_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Visualization saved as migration_analysis.png")

# ============================================================================
# CELL 6: Posterior Predictive Checks
# ============================================================================

az.plot_trace(trace, var_names=['beta', 'mu_global', 'sigma'])
plt.tight_layout()
plt.savefig('posterior_trace.png', dpi=150, bbox_inches='tight')
plt.show()

print("✓ Posterior trace plots saved as posterior_trace.png")

# ============================================================================
# CELL 7: Model Interpretation
# ============================================================================

print("\n" + "=" * 70)
print("MODEL INTERPRETATION")
print("=" * 70)

beta_summary = az.summary(trace, var_names=["beta"])
print("\nFEATURE EFFECTS (Beta Coefficients):")
print("Interpretation: positive = increases migration, negative = decreases migration")
print(beta_summary)

print("\n" + "=" * 70)
print("KEY FINDINGS")
print("=" * 70)

features = ['spei_drought', 'night_lights', 'ag_yield', 'education_index', 'conflict_index']
beta_values = trace.posterior["beta"].mean(dim=["chain", "draw"]).values

for i, feature in enumerate(features):
    effect = "↑ INCREASES" if beta_values[i] > 0 else "↓ DECREASES"
    magnitude = abs(beta_values[i])
    print(f"\n{feature.upper()}: {effect} migration ({magnitude:.3f} units per std)")

print("\n" + "=" * 70)
print("✓ ANALYSIS COMPLETE!")
print("=" * 70)
print("\nNext steps:")
print("1. Download the generated plots and data")
print("2. Review model diagnostics and posterior predictive checks")
print("3. Use the model for counterfactual policy simulations")
print("4. Deploy dashboard with: streamlit run app.py")
