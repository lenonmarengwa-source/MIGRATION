# Quick-Start Implementation Guide

## Phase 1: Immediate Actions (This Week)

### 1. Set Up Project Structure
```bash
git clone https://github.com/lenonmarengwa-source/MIGRATION.git
cd MIGRATION

# Create directory structure
mkdir -p backend/{data_sources,models,policy_engine,alerts,reporting,api,db}
mkdir -p frontend/{web,mobile}
mkdir -p deployment/{docker,render,aws}
mkdir -p docs

# Initialize core files
touch backend/__init__.py
touch backend/requirements_extended.txt
```

### 2. Install Extended Dependencies
```bash
# backend/requirements_extended.txt
pip install -r requirements_extended.txt
```

**New Dependencies:**
```
# Data Integration
requests==2.31.0
schedule==1.2.0
pandas==2.0.0
geopandas==0.13.0

# Advanced Models
xgboost==2.0.0
lightgbm==4.0.0
tensorflow==2.13.0  # for LSTM
torch==2.0.0  # optional: for neural networks

# API & Deployment
fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.4.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0  # PostgreSQL adapter

# Bayesian & Spatial
pymc==5.8.0
arviz==0.16.0
scikit-learn==1.3.0
scipy==1.11.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.0
```

### 3. Create Data Pipeline Skeleton

**File:** `backend/data_sources/zimstat_api.py`
```python
"""
ZimStat API Integration
Connects to Zimbabwe Statistical Agency for official data
"""
import requests
from datetime import datetime, timedelta
import pandas as pd
import os

class ZimStatAPI:
    def __init__(self):
        self.base_url = os.getenv("ZIMSTAT_API_URL", "https://api.zimstat.co.zw")
        self.api_key = os.getenv("ZIMSTAT_API_KEY")
        
    def get_agricultural_yield(self, district=None, year=None):
        """Fetch agricultural yield data"""
        endpoint = f"{self.base_url}/agriculture/yield"
        params = {
            "api_key": self.api_key,
            "district": district,
            "year": year
        }
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def get_inflation_rate(self):
        """Fetch current inflation/USD exchange rate"""
        endpoint = f"{self.base_url}/economic/inflation"
        params = {"api_key": self.api_key}
        response = requests.get(endpoint, params=params)
        return response.json()
    
    def get_unemployment(self, district=None):
        """Fetch unemployment statistics"""
        endpoint = f"{self.base_url}/employment/unemployment"
        params = {
            "api_key": self.api_key,
            "district": district
        }
        response = requests.get(endpoint, params=params)
        return response.json()

if __name__ == "__main__":
    zimstat = ZimStatAPI()
    print("Testing ZimStat API connections...")
    # Tests will run once API keys are configured
```

### 4. Create FastAPI Skeleton

**File:** `backend/api/main.py`
```python
"""
FastAPI Backend for Zimbabwe Migration System
Production-ready REST API
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

app = FastAPI(
    title="Zimbabwe Migration Risk API",
    description="Advanced decision-support system for migration management",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes (will be created)
# from api.routes import risk, forecast, policy, data

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5. Create Enhanced Model Skeleton

**File:** `backend/models/bayesian_hierarchical_v2.py`
```python
"""
Enhanced Spatio-Temporal Bayesian Hierarchical Model
Includes climate projections, economic indicators, conflict layer
"""
import pymc as pm
import numpy as np
import pandas as pd
from arviz import InferenceData

class EnhancedBayesianModel:
    def __init__(self, data: pd.DataFrame, climate_data: pd.DataFrame, 
                 economic_data: pd.DataFrame, conflict_data: pd.DataFrame):
        """
        Initialize the enhanced model
        
        Args:
            data: Migration and baseline covariates
            climate_data: CMIP6 projections + SPEI indices
            economic_data: Inflation, exchange rates, unemployment
            conflict_data: ACLED events aggregated to district level
        """
        self.data = data
        self.climate_data = climate_data
        self.economic_data = economic_data
        self.conflict_data = conflict_data
        self.model = None
        self.trace = None
    
    def build_model(self):
        """Build the hierarchical model"""
        with pm.Model() as model:
            # Priors for global parameters
            global_mean = pm.Normal('global_mean', mu=10, sigma=5)
            global_sd = pm.HalfNormal('global_sd', sigma=2)
            
            # Climate effect
            climate_effect = pm.Normal('climate_effect', mu=0, sigma=1)
            
            # Economic effect
            economic_effect = pm.Normal('economic_effect', mu=0, sigma=1)
            
            # Conflict effect
            conflict_effect = pm.Normal('conflict_effect', mu=0, sigma=1)
            
            # Hierarchical effects (district-level)
            n_districts = self.data['district'].nunique()
            district_effects = pm.Normal('district_effects', 
                                        mu=global_mean, 
                                        sigma=global_sd, 
                                        shape=n_districts)
            
            # Likelihood
            mu = global_mean + district_effects + \
                climate_effect * self.climate_data['spei'] + \
                economic_effect * self.economic_data['inflation'] + \
                conflict_effect * self.conflict_data['event_count']
            
            migration_rate = pm.Normal('migration_rate', 
                                      mu=mu, 
                                      sigma=2,
                                      observed=self.data['migration_rate'])
        
        self.model = model
        return model
    
    def fit(self, draws=2000, tune=1000):
        """Fit the model using NUTS sampler"""
        with self.model:
            self.trace = pm.sample(draws=draws, tune=tune, 
                                  return_inferencedata=True,
                                  cores=4, progressbar=True)
        return self.trace
    
    def predict(self, new_data: pd.DataFrame):
        """Make predictions on new data"""
        # Implementation
        pass

if __name__ == "__main__":
    print("Enhanced Bayesian Model ready for implementation")
```

---

## Phase 2: Data Partnership Setup (Next 2 Weeks)

### 1. Contact Government Partners
**Action Items:**
- [ ] Email: Ministry of Local Government - Request dashboard access & feedback
- [ ] Email: ZimStat - Request API credentials
- [ ] Email: Meteorological Services - Request climate data feed
- [ ] Email: Reserve Bank of Zimbabwe - Request economic data
- [ ] Meeting: ACLED team - Discuss conflict data integration

### 2. Create Partnership MOU Template
**File:** `docs/PARTNERSHIP_MOU_TEMPLATE.md`
```markdown
# Memorandum of Understanding Template

## Between: [Your Organization] & [Government/Data Partner]

### 1. Objective
Support evidence-based migration policy through real-time data integration and decision support.

### 2. Data Sharing Terms
- [ ] Data provider commits to monthly/weekly updates
- [ ] API access credentials provided
- [ ] Data confidentiality agreement signed
- [ ] Quality standards established

### 3. Timeline
- [ ] Integration starts: [Date]
- [ ] First data pull: [Date]
- [ ] Testing period: [Duration]
- [ ] Production deployment: [Date]

### 4. Success Metrics
- [ ] System uptime > 99%
- [ ] API response time < 500ms
- [ ] Data accuracy validated annually
```

---

## Phase 3: Deployment Configuration (Week 3)

### 1. Docker Setup
**File:** `deployment/docker/Dockerfile.api`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements_extended.txt .
RUN pip install --no-cache-dir -r requirements_extended.txt

COPY backend/ ./backend/
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Render Deployment Config
**File:** `deployment/render_config.yaml`
```yaml
services:
  - type: web
    name: zimbabwe-migration-api
    runtime: python
    buildCommand: pip install -r backend/requirements_extended.txt
    startCommand: uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: DATABASE_URL
        scope: all
      - key: ZIMSTAT_API_KEY
        scope: all
      - key: ACLED_API_KEY
        scope: all
    
  - type: pserv
    name: zimbabwe-migration-db
    plan: starter plus
    db_name: migration_db
    user: migration_admin
```

### 3. GitHub Actions CI/CD
**File:** `.github/workflows/deploy.yml`
```yaml
name: Deploy Zimbabwe Migration System

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements_extended.txt
      - run: pytest backend/tests/
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST https://api.render.com/v1/services/deployment \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -d '{"gitBranch": "main"}'
```

---

## Priority Implementation Checklist

### ✅ IMMEDIATE (This Week)
- [ ] Fix all syntax errors (DONE ✓)
- [ ] Set up extended requirements
- [ ] Create FastAPI skeleton
- [ ] Initialize data pipeline templates
- [ ] Docker configuration

### ⚡ HIGH PRIORITY (Weeks 2-4)
- [ ] Establish ZimStat API connection
- [ ] Integrate weather data feed
- [ ] Add ACLED conflict layer
- [ ] Deploy on Render.com
- [ ] Multi-language support (English/Shona/Ndebele)

### 📊 MEDIUM PRIORITY (Weeks 5-8)
- [ ] Enhanced Bayesian model training
- [ ] Ensemble hybrid modeling
- [ ] Policy brief generator
- [ ] Early warning system
- [ ] Mobile app beta

### 🎯 LONG TERM (Weeks 9+)
- [ ] Satellite data integration
- [ ] CDR mobility analysis
- [ ] Counterfactual simulator
- [ ] WhatsApp bot
- [ ] Regional SADC integration

---

## Key Contact Information & Resources

### Zimbabwe Government
- **Ministry of Local Government:** +263 242 791811
- **ZimStat:** https://zimstat.co.zw/
- **Meteorological Services:** +263 242 737344

### International Partners
- **ACLED:** https://www.acleddata.com/
- **NASA EOSDIS:** https://eosdis.nasa.gov/
- **World Bank Open Data:** https://data.worldbank.org/
- **UNDP Zimbabwe:** https://www.zw.undp.org/

### Technical Resources
- **Render Deployment:** https://render.com/
- **PyMC Documentation:** https://www.pymc.io/
- **FastAPI Tutorial:** https://fastapi.tiangolo.com/
- **GitHub Actions:** https://github.com/features/actions

---

**Document Version:** 1.0
**Last Updated:** June 2026
