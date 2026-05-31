# DEPLOYMENT GUIDE

## Render.com (Recommended for this app)
1. Go to render.com
2. New -> Web Service -> Connect GitHub repo
3. Environment: Docker
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Streamlit Community Cloud
- Use `app.py` as entrypoint
- Add secrets for auth if needed

## Docker
```bash
docker build -t migration-app .
docker run -p 8501:8501 migration-app
```