# Python Cloud Deployment Test App

A simple Flask web app you can use to test cloud deployment.

## Endpoints

- `GET /` returns a message and active environment.
- `GET /health` returns a health check payload.

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

App URL: `http://localhost:8000`

## Run Tests

```powershell
pytest -q
```

## Run with Docker

```powershell
docker compose up --build
```

## Cloud Deploy Option 1: Render (easiest)

1. Push this project to GitHub.
2. In Render, create a new **Web Service** from the repo.
3. Use these settings:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
4. Deploy and open:
   - `/`
   - `/health`

You can also deploy with the included `render.yaml` Blueprint for one-click setup.

## Cloud Deploy Option 2: Azure App Service (Container)

1. Build and test container locally:

```powershell
docker build -t py-cloud-test:latest .
docker run -p 8000:8000 py-cloud-test:latest
```

2. Push image to Azure Container Registry (ACR).
3. Create Azure App Service (Linux, container-based).
4. Point App Service to your ACR image.
5. Ensure the app listens on port `8000`.
6. Browse `/health` to validate deployment.

## Verify Deployment

After cloud deployment, this should return HTTP 200:

```text
GET https://<your-app-url>/health
```
