# 🚀 Deployment Guide - AI Career Navigator

This guide will help you deploy the AI Career Navigator application to Azure.

## 📋 Prerequisites

1. **Azure Account** with active subscription
2. **Azure CLI** installed (`az --version` to verify)
3. **Docker** installed and running
4. **Node.js 20+** and **Python 3.11+**
5. **Azure OpenAI** service provisioned

## 🔧 Local Setup

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Update the `.env` file with your Azure credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_CHATGPT_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_CHATGPT_MODEL=gpt-4.1
AZURE_OPENAI_API_VERSION=2024-02-01
```

### 2. Local Testing with Docker

Build and run the application locally:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Health Check: http://localhost:8000/health

### 3. Local Development (without Docker)

**Backend:**
```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd app/frontend
npm install
npm run dev
```

## ☁️ Azure Deployment

### Option 1: Azure Container Apps (Recommended)

#### Step 1: Create Azure Resources

```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="ai-career-navigator-rg"
LOCATION="eastus"
ACR_NAME="aicareernavigatoracr"
CONTAINER_APP_ENV="ai-career-navigator-env"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Create Container Apps environment
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

#### Step 2: Build and Push Images

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Build and push backend
cd app/backend
docker build -t $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest .
docker push $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest

# Build and push frontend
cd ../frontend
docker build -t $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest .
docker push $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest
```

#### Step 3: Deploy Container Apps

```bash
# Deploy backend
az containerapp create \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY \
    AZURE_OPENAI_CHATGPT_DEPLOYMENT=$AZURE_OPENAI_CHATGPT_DEPLOYMENT \
    AZURE_OPENAI_CHATGPT_MODEL=$AZURE_OPENAI_CHATGPT_MODEL \
    AZURE_OPENAI_API_VERSION=$AZURE_OPENAI_API_VERSION \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3

# Get backend URL
BACKEND_URL=$(az containerapp show \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

# Deploy frontend
az containerapp create \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 80 \
  --ingress external \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 2

# Get frontend URL
FRONTEND_URL=$(az containerapp show \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo "🎉 Deployment complete!"
echo "Frontend: https://$FRONTEND_URL"
echo "Backend: https://$BACKEND_URL"
```

### Option 2: Azure App Service

#### Step 1: Create App Service Resources

```bash
# Create App Service Plan
az appservice plan create \
  --name ai-career-navigator-plan \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --is-linux \
  --sku B2

# Create backend web app
az webapp create \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --plan ai-career-navigator-plan \
  --runtime "PYTHON:3.11"

# Configure backend
az webapp config appsettings set \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY \
    AZURE_OPENAI_CHATGPT_DEPLOYMENT=$AZURE_OPENAI_CHATGPT_DEPLOYMENT \
    AZURE_OPENAI_CHATGPT_MODEL=$AZURE_OPENAI_CHATGPT_MODEL \
    AZURE_OPENAI_API_VERSION=$AZURE_OPENAI_API_VERSION

# Deploy backend
cd app/backend
zip -r backend.zip .
az webapp deploy \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --src-path backend.zip \
  --type zip

# Create frontend web app
az webapp create \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --plan ai-career-navigator-plan \
  --runtime "NODE:20-lts"

# Deploy frontend
cd ../frontend
npm run build
cd dist
zip -r frontend.zip .
az webapp deploy \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --src-path frontend.zip \
  --type zip
```

### Option 3: Using Azure Developer CLI (azd)

```bash
# Install azd
curl -fsSL https://aka.ms/install-azd.sh | bash

# Login
azd auth login

# Initialize
azd init

# Set environment variables
azd env set AZURE_OPENAI_ENDPOINT $AZURE_OPENAI_ENDPOINT
azd env set AZURE_OPENAI_API_KEY $AZURE_OPENAI_API_KEY
azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT $AZURE_OPENAI_CHATGPT_DEPLOYMENT
azd env set AZURE_OPENAI_CHATGPT_MODEL $AZURE_OPENAI_CHATGPT_MODEL

# Deploy
azd up
```

## 🔍 Monitoring & Troubleshooting

### View Container Logs

```bash
# Backend logs
az containerapp logs show \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --follow

# Frontend logs
az containerapp logs show \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --follow
```

### Health Checks

```bash
# Check backend health
curl https://BACKEND_URL/health

# Check backend config
curl https://BACKEND_URL/config
```

### Common Issues

1. **CORS Errors**: Update `CORS_ORIGINS` in backend config
2. **OpenAI Errors**: Verify API key and endpoint
3. **Container Startup Failures**: Check logs for dependency issues
4. **Memory Issues**: Increase container memory allocation

## 🔄 Updates & Redeployment

### Update Backend

```bash
cd app/backend
docker build -t $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest .
docker push $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest

az containerapp update \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_LOGIN_SERVER/ai-career-navigator-backend:latest
```

### Update Frontend

```bash
cd app/frontend
docker build -t $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest .
docker push $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest

az containerapp update \
  --name ai-career-navigator-frontend \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_LOGIN_SERVER/ai-career-navigator-frontend:latest
```

## 💰 Cost Optimization

- Use **Basic tier** for Container Registry ($5/month)
- Use **Consumption plan** for Container Apps (pay-per-use)
- Set **min replicas to 0** for non-production environments
- Use **Azure Free Tier** services where possible

## 🔐 Security Best Practices

1. Use **Azure Key Vault** for secrets
2. Enable **HTTPS** only
3. Configure **network restrictions**
4. Enable **managed identities**
5. Implement **rate limiting**
6. Set up **Azure Monitor** alerts

## 📊 Scaling

Container Apps automatically scale based on:
- HTTP requests
- CPU usage
- Memory usage

Configure scaling rules:

```bash
az containerapp update \
  --name ai-career-navigator-backend \
  --resource-group $RESOURCE_GROUP \
  --min-replicas 1 \
  --max-replicas 10 \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 50
```

## 🎯 CI/CD with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/azure-deploy.yml`).

Configure secrets in GitHub:
- `ACR_LOGIN_SERVER`
- `ACR_USERNAME`
- `ACR_PASSWORD`
- `AZURE_RESOURCE_GROUP`

Every push to `main` branch will trigger automatic deployment.

## 📞 Support

For issues or questions:
- Email: aryanjstar3@gmail.com
- GitHub: https://github.com/Aryanjstar/AI-Career-Navigator
- LinkedIn: https://www.linkedin.com/in/aryanjstar

---

**Happy Deploying! 🚀**

