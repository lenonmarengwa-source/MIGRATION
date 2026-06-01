# TROUBLESHOOTING GUIDE

## ❗️ Installation Error: "installer returned a non-zero exit code"

This error occurs when pip can't install one or more dependencies. Here are the solutions:

---

## Solution 1: Use Minimal Requirements (Fastest ⚡)

```bash
pip install -r requirements-minimal.txt
```

Then run:
```bash
streamlit run web_system.py
```

**Includes:** Streamlit, Pandas, Plotly, Folium, Maps, etc.  
**Missing:** Advanced ML libraries (added in Phase 2)

---

## Solution 2: Install Step-by-Step

If minimal fails, install one package at a time to find the culprit:

```bash
pip install streamlit
pip install pandas
pip install plotly
pip install folium
pip install streamlit-folium
pip install scipy
pip install scikit-learn
```

If GeoPandas fails (common issue on Windows):
```bash
# Option A: Use conda instead
conda install geopandas

# Option B: Skip it temporarily (maps will load without detailed shapefile)
# Comment out geopandas from requirements.txt
```

---

## Solution 3: Use Python Virtual Environment from Scratch

```bash
# 1. Remove old venv
rm -rf venv  # Mac/Linux
rmdir /s /q venv  # Windows

# 2. Create fresh venv with specific Python version
python3.11 -m venv venv

# 3. Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install minimal
pip install -r requirements-minimal.txt
```

---

## Solution 4: For Mac Users (GeoPandas Issue)

GeoPandas requires system libraries. Install via Homebrew first:

```bash
# Install system dependencies
brew install gdal geos proj

# Then create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-minimal.txt
```

---

## Solution 5: For Windows Users

Windows sometimes has issues with binary packages. Try:

```bash
# 1. Install pre-built wheels
pip install --upgrade wheel setuptools

# 2. Install minimal requirements
pip install -r requirements-minimal.txt

# 3. If still failing, use pre-built binaries
pip install --only-binary :all: geopandas
```

---

## Solution 6: Use Anaconda Instead

If pip keeps failing, use Anaconda:

```bash
# Create conda environment
conda create -n migration python=3.11

# Activate
conda activate migration

# Install from conda-forge (more stable for geospatial)
conda install streamlit pandas plotly folium geopandas -c conda-forge
```

---

## ✅ Quick Test After Installation

After successfully installing, verify with:

```bash
python -c "import streamlit; print('✓ Streamlit OK')"
python -c "import pandas; print('✓ Pandas OK')"
python -c "import plotly; print('✓ Plotly OK')"
python -c "import folium; print('✓ Folium OK')"
```

---

## 🚀 Run the App

Once installation succeeds:

```bash
streamlit run web_system.py
```

Then open: **http://localhost:8501**

Login: `admin` / `migration2026`

---

## 📊 Feature Availability by Requirements

| Feature | Minimal | Full |
|---------|---------|------|
| Dashboard | ✅ | ✅ |
| Maps | ✅ | ✅ |
| Charts | ✅ | ✅ |
| Data Export | ✅ | ✅ |
| Recommendations | ✅ | ✅ |
| Advanced Models | ❌ | ✅ |
| Satellite Data | ❌ | ✅ |

---

## 🔍 Debugging Tips

1. **Check pip version:**
   ```bash
   pip --version
   ```

2. **See detailed error:**
   ```bash
   pip install streamlit -v  # verbose mode
   ```

3. **Check system Python:**
   ```bash
   python --version
   which python  # Mac/Linux
   where python  # Windows
   ```

4. **Check available disk space:**
   ```bash
   df -h  # Mac/Linux
   ```

---

## 💡 Still Stuck?

Try this nuclear option (completely fresh start):

```bash
# 1. Remove venv completely
rm -rf venv

# 2. Create minimal venv with just Python
python3.11 -m venv venv --without-pip

# 3. Activate
source venv/bin/activate

# 4. Manually upgrade pip
curl https://bootstrap.pypa.io/get-pip.py | python

# 5. Install minimal
pip install -r requirements-minimal.txt
```

---

**Last Resort:** Use Streamlit Cloud (no installation needed!)
Visit: https://streamlit.io/cloud

---

**Status:** 🔧 Troubleshooting Complete  
**Recommended:** Start with `requirements-minimal.txt`  
**Time to Fix:** 5-15 minutes
