#!/bin/bash

# AI Career Navigator - Azure Deployment Script
set -e

echo "🚀 Starting Azure deployment for AI Career Navigator..."
echo ""

# Configuration
RESOURCE_GROUP="ai-career-navigator-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="ai-career-navigator-plan"
BACKEND_APP="ai-career-navigator-backend"
FRONTEND_APP="ai-career-navigator-frontend"

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env file not found!"
    exit 1
fi

# Check if resource group exists
echo "🔍 Checking Azure resources..."
if az group show --name $RESOURCE_GROUP &>/dev/null; then
    echo "✓ Resource group '$RESOURCE_GROUP' already exists"
else
    echo "📦 Creating resource group '$RESOURCE_GROUP'..."
    az group create --name $RESOURCE_GROUP --location $LOCATION
fi

# Check if App Service Plan exists
if az appservice plan show --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP &>/dev/null; then
    echo "✓ App Service Plan '$APP_SERVICE_PLAN' already exists"
else
    echo "📦 Creating App Service Plan..."
    az appservice plan create \
        --name $APP_SERVICE_PLAN \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION \
        --is-linux \
        --sku B1
fi

# Deploy Backend
echo ""
echo "🔧 Deploying Backend..."

# Check if backend app exists
if az webapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP &>/dev/null; then
    echo "✓ Backend app '$BACKEND_APP' already exists"
else
    echo "📦 Creating backend web app..."
    az webapp create \
        --name $BACKEND_APP \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --runtime "PYTHON:3.11"
fi

# Configure backend settings
echo "⚙️  Configuring backend environment variables..."
az webapp config appsettings set \
    --name $BACKEND_APP \
    --resource-group $RESOURCE_GROUP \
    --settings \
        AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
        AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
        AZURE_OPENAI_CHATGPT_DEPLOYMENT="$AZURE_OPENAI_CHATGPT_DEPLOYMENT" \
        AZURE_OPENAI_CHATGPT_MODEL="$AZURE_OPENAI_CHATGPT_MODEL" \
        AZURE_OPENAI_API_VERSION="$AZURE_OPENAI_API_VERSION" \
        DEBUG="False" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    --output none

# Set startup command
echo "⚙️  Setting startup command..."
az webapp config set \
    --name $BACKEND_APP \
    --resource-group $RESOURCE_GROUP \
    --startup-file "gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 app:create_app()" \
    --output none

# Deploy backend code
echo "📤 Deploying backend code..."
cd app/backend
zip -r ../../backend-deploy.zip . -x "*.pyc" -x "__pycache__/*" -x ".venv/*" -x "*.git*"
cd ../..

az webapp deploy \
    --name $BACKEND_APP \
    --resource-group $RESOURCE_GROUP \
    --src-path backend-deploy.zip \
    --type zip \
    --async true

# Get backend URL
BACKEND_URL=$(az webapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)

# Deploy Frontend
echo ""
echo "🎨 Deploying Frontend..."

# Check if frontend app exists
if az webapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP &>/dev/null; then
    echo "✓ Frontend app '$FRONTEND_APP' already exists"
else
    echo "📦 Creating frontend web app..."
    az webapp create \
        --name $FRONTEND_APP \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --runtime "NODE:20-lts"
fi

# Build and deploy frontend
echo "🔨 Building frontend..."
cd app/frontend

# Update API endpoint in build
export VITE_API_BASE_URL="https://$BACKEND_URL"

npm install --legacy-peer-deps
npm run build

# Create deployment package
cd dist
zip -r ../../../frontend-deploy.zip .
cd ../../..

echo "📤 Deploying frontend code..."
az webapp deploy \
    --name $FRONTEND_APP \
    --resource-group $RESOURCE_GROUP \
    --src-path frontend-deploy.zip \
    --type zip \
    --async true

# Get frontend URL
FRONTEND_URL=$(az webapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)

# Cleanup
rm -f backend-deploy.zip frontend-deploy.zip

echo ""
echo "✅ Deployment initiated successfully!"
echo ""
echo "📍 Application URLs:"
echo "   Frontend: https://$FRONTEND_URL"
echo "   Backend:  https://$BACKEND_URL"
echo ""
echo "⏳ Note: First deployment may take 5-10 minutes to complete."
echo "   Check status with: az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP"
echo ""
echo "🎉 Deployment complete!"

