#!/bin/bash
set -e

echo "🚀 Creating PRODUCTION deployment of AI Career Navigator"
echo ""

# Configuration
RESOURCE_GROUP="ai-career-nav-prod"
LOCATION="eastus"
APP_SERVICE_PLAN="ai-career-nav-plan"
APP_NAME="ai-career-navigator"

# Load environment variables
if [ -f .env ]; then
    echo "📋 Loading environment variables"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

echo "📦 Creating Azure resources..."

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION --output none
echo "✅ Resource group created"

# Create App Service Plan with B1 (Always-On)
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --is-linux \
    --sku B1 \
    --output none
echo "✅ App Service Plan created (B1 - Always-On)"

# Create Web App
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --runtime "PYTHON:3.11" \
    --output none
echo "✅ Web App created"

# Configure Always-On
az webapp config set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --always-on true \
    --startup-file "startup.sh" \
    --output none
echo "✅ Always-On enabled"

# Set environment variables
az webapp config appsettings set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
        AZURE_OPENAI_ENDPOINT="$AZURE_OPENAI_ENDPOINT" \
        AZURE_OPENAI_API_KEY="$AZURE_OPENAI_API_KEY" \
        AZURE_OPENAI_CHATGPT_DEPLOYMENT="$AZURE_OPENAI_CHATGPT_DEPLOYMENT" \
        AZURE_OPENAI_CHATGPT_MODEL="$AZURE_OPENAI_CHATGPT_MODEL" \
        AZURE_OPENAI_API_VERSION="2024-02-01" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    --output none
echo "✅ Environment variables configured"

# Deploy application
echo "📤 Deploying application..."
az webapp deploy \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --src-path backend-production.zip \
    --type zip \
    --clean true \
    --restart true \
    --async false

# Get URL
APP_URL=$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PRODUCTION DEPLOYMENT COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Your application is live at:"
echo "   https://$APP_URL"
echo ""
echo "🔧 Features:"
echo "   ✅ Always-On (no cold starts)"
echo "   ✅ OpenAI retry logic"
echo "   ✅ Responsive design (mobile/tablet/desktop)"
echo "   ✅ Health monitoring"
echo "   ✅ Production logging"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
