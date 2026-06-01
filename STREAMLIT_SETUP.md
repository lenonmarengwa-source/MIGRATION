#!/usr/bin/env python3
"""
Zimbabwe Migration Risk Management System - Streamlit Testing Guide
Complete setup for local testing and deployment
"""

# STEP 1: INSTALLATION & SETUP INSTRUCTIONS
"""
=============================================================================
INSTALLATION GUIDE
=============================================================================

1. Clone the repository:
   git clone https://github.com/lenonmarengwa-source/MIGRATION.git
   cd MIGRATION

2. Create a Python virtual environment:
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt
   
   # For enhanced features, also install:
   pip install -r backend/requirements_extended.txt

4. Create a .env file for configuration:
   cp .env.example .env
   
   # Edit .env with your settings:
   STREAMLIT_LOGGER_LEVEL=info
   DEBUG=False
   DEPLOYMENT_ENV=local

=============================================================================
RUNNING LOCALLY
=============================================================================

Option A: Run the full dashboard (recommended for testing)
   streamlit run web_system.py

Option B: Run the simple authentication app
   streamlit run app.py

Option C: Run with custom configuration
   streamlit run web_system.py --logger.level=debug

Access the app at: http://localhost:8501

Credentials:
   Username: admin
   Password: migration2026

=============================================================================
DEPLOYING TO STREAMLIT CLOUD
=============================================================================

1. Push to GitHub (already done ✓)

2. Go to https://streamlit.io/cloud

3. Click "New app" and select:
   Repository: lenonmarengwa-source/MIGRATION
   Branch: main
   Main file path: web_system.py

4. Click "Deploy!"

Your app will be live at:
   https://lenonmarengwa-source-migration.streamlit.app

=============================================================================
DEPLOYING TO RENDER (FOR API + FRONTEND)
=============================================================================

1. Create account at https://render.com

2. Connect your GitHub repository

3. Create a new "Web Service":
   - Name: zimbabwe-migration-system
   - Environment: Python 3
   - Build command: pip install -r requirements.txt
   - Start command: streamlit run web_system.py --server.port=8501

4. Add environment variables:
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_LOGGER_LEVEL=info

5. Deploy and access at: https://zimbabwe-migration-system.onrender.com

=============================================================================
TESTING CHECKLIST
=============================================================================

[ ] Installation successful
[ ] Virtual environment activated
[ ] Dependencies installed
[ ] .env file created
[ ] Streamlit runs without errors
[ ] Login page loads
[ ] Authentication works
[ ] Dashboard displays correctly
[ ] All tabs are accessible
[ ] Charts load and display data
[ ] Map renders correctly
[ ] No console errors

=============================================================================
TROUBLESHOOTING
=============================================================================

Issue: ModuleNotFoundError: No module named 'streamlit'
Fix: pip install streamlit

Issue: Port 8501 already in use
Fix: streamlit run web_system.py --server.port=8502

Issue: GeoPandas import error
Fix: conda install geopandas (if using conda)
     or: pip install geopandas

Issue: Plotly charts not rendering
Fix: pip install plotly kaleido

Issue: Authentication not working
Fix: Clear browser cache and restart app

Issue: Memory error with large datasets
Fix: Restart Streamlit and clear cache: streamlit cache clear

=============================================================================
"""

print(__doc__)
