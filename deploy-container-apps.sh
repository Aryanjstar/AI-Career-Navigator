#!/bin/bash
set -e

echo "🚀 Deploying to Azure Container Apps..."

# Configuration
RESOURCE_GROUP="ai-career-navigator-rg"
LOCATION="eastus"
ACR_NAME="aicareernavcr$(date +%s | tail -c 6)"
CONTAINER_APP_ENV="ai-career-env"
BACKEND_APP="ai-career-backend"
FRONTEND_APP="ai-career-frontend"

# Load .env
export $(cat .env | grep -v '^#' | xargs)

echo "📦 Creating Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true \
  --output none

echo "✓ ACR created: $ACR_NAME"

# Get ACR credentials
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USER=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASS=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

echo "🔑 Logging into ACR..."
echo $ACR_PASS | docker login $ACR_SERVER -u $ACR_USER --password-stdin

echo "🏗️ Building backend image..."
cd app/backend
docker build -t $ACR_SERVER/backend:latest . --platform linux/amd64
docker push $ACR_SERVER/backend:latest
cd ../..

echo "🏗️ Building frontend image..."
cd app/frontend
docker build -t $ACR_SERVER/frontend:latest . --platform linux/amd64
docker push $ACR_SERVER/frontend:latest
cd ../..

echo "🌐 Creating Container Apps environment..."
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --output none || echo "Environment already exists"

echo "🚀 Deploying backend container..."
az containerapp create \
  --name $BACKEND_APP \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_SERVER/backend:latest \
  --registry-server $ACR_SERVER \
  --registry-username $ACR_USER \
  --registry-password $ACR_PASS \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" \
    "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY" \
    "AZURE_OPENAI_CHATGPT_DEPLOYMENT=$AZURE_OPENAI_CHATGPT_DEPLOYMENT" \
    "AZURE_OPENAI_CHATGPT_MODEL=$AZURE_OPENAI_CHATGPT_MODEL" \
    "AZURE_OPENAI_API_VERSION=$AZURE_OPENAI_API_VERSION" \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --output none

BACKEND_URL=$(az containerapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

echo "🚀 Deploying frontend container..."
az containerapp create \
  --name $FRONTEND_APP \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_SERVER/frontend:latest \
  --registry-server $ACR_SERVER \
  --registry-username $ACR_USER \
  --registry-password $ACR_PASS \
  --target-port 80 \
  --ingress external \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 2 \
  --output none

FRONTEND_URL=$(az containerapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

echo ""
echo "✅ DEPLOYMENT SUCCESSFUL!"
echo ""
echo "🎉 Your application is live at:"
echo "   Frontend: https://$FRONTEND_URL"
echo "   Backend:  https://$BACKEND_URL"
echo ""
