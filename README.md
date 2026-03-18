# Python Cloud Deployment Test App

A simple Flask web app you can use to test cloud deployment.

## Endpoints

- `GET /` returns a message and active environment.
- `GET /health` returns a health check payload.
- `GET /dashboard` returns a visual status page.

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

## Cloud Deploy Option 2: Azure App Service (Code, no container)

### Prerequisites

1. Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli
2. Login:

```powershell
az login
```

### Fast Deploy (script)

From this project folder:

```powershell
.\scripts\deploy_azure_code.ps1 -ResourceGroup rg-py-cloud-test -AppName <unique-app-name> -Location eastus
```

This script will:
- Create or reuse a resource group
- Deploy source code with `az webapp up`
- Configure startup command to run Flask via Gunicorn
- Set `ENVIRONMENT=azure-code`

### Manual Deploy (Azure CLI)

```powershell
az group create --name rg-py-cloud-test --location eastus
az webapp up --name <unique-app-name> --resource-group rg-py-cloud-test --runtime "PYTHON:3.12" --sku B1
az webapp config set --name <unique-app-name> --resource-group rg-py-cloud-test --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
az webapp config appsettings set --name <unique-app-name> --resource-group rg-py-cloud-test --settings ENVIRONMENT=azure-code
```

Then validate:
- `https://<unique-app-name>.azurewebsites.net/dashboard`
- `https://<unique-app-name>.azurewebsites.net/health`

## Verify Deployment

After cloud deployment, this should return HTTP 200:

```text
GET https://<your-app-url>/health
```
