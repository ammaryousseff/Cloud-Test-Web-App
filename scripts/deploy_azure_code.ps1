param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroup,

    [Parameter(Mandatory = $true)]
    [string]$AppName,

    [Parameter(Mandatory = $false)]
    [string]$Location = "eastus",

    [Parameter(Mandatory = $false)]
    [string]$Runtime = "PYTHON:3.12"
)

$ErrorActionPreference = "Stop"

Write-Host "Checking Azure CLI..."
az version | Out-Null

Write-Host "Ensuring login session..."
az account show | Out-Null

Write-Host "Creating resource group if needed..."
az group create --name $ResourceGroup --location $Location | Out-Null

Write-Host "Deploying app code to Azure App Service (no container)..."
az webapp up `
    --name $AppName `
    --resource-group $ResourceGroup `
    --runtime $Runtime `
    --sku B1

Write-Host "Setting startup command for Flask/Gunicorn..."
az webapp config set `
    --name $AppName `
    --resource-group $ResourceGroup `
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app" | Out-Null

Write-Host "Setting app environment variable..."
az webapp config appsettings set `
    --name $AppName `
    --resource-group $ResourceGroup `
    --settings ENVIRONMENT=azure-code | Out-Null

Write-Host "Done. Open these URLs:"
Write-Host "https://$AppName.azurewebsites.net/dashboard"
Write-Host "https://$AppName.azurewebsites.net/health"
