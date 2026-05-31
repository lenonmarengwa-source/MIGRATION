# Zimbabwe Bayesian Migration Risk Model

Advanced hierarchical Bayesian spatio-temporal model with CAR spatial correlation for predicting internal migration risk in Zimbabwe under climate, economic, and policy scenarios.

## Features
- CAR (Conditional Autoregressive) spatial effects
- Province → District hierarchy
- Explicit missing data handling
- Multiple counterfactual interventions (irrigation, education, conflict, economy)
- Posterior predictive checks
- Interactive Streamlit dashboard
- Full uncertainty quantification

## How to Run
1. `pip install -r requirements.txt`
2. Place your data files (`zimbabwe_district_data.csv` and shapefile)
3. `python zimbabwe_migration_model.py`
4. `streamlit run app.py`

## Model Innovation
Combines small-area estimation, spatio-temporal dynamics, and policy counterfactuals — currently rare in Zimbabwe-focused literature.