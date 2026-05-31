# Synthetic Data Generator

import pandas as pd
import numpy as np
np.random.seed(42)
provinces = ['Harare', 'Bulawayo', 'Mashonaland East', 'Mashonaland West', 'Matabeleland North', 'Matabeleland South']
data = []
for p in provinces:
    for d in range(1, 11):
        data.append({
            'province': p,
            'district': f'District_{d}',
            'migration_risk': round(np.random.beta(2, 5), 3),
            'population': int(np.random.randint(20000, 600000)),
            'climate_stress': round(np.random.uniform(0.1, 0.9), 2),
            'economic_index': round(np.random.uniform(0.3, 0.8), 2),
            'year': 2025
        })
df = pd.DataFrame(data)
df.to_csv('synthetic_migration_data.csv', index=False)
print('✅ Synthetic data created successfully!')