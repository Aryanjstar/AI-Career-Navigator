# 🚀 Deployment Guide - AI Career Navigator

This guide walks you through deploying AI Career Navigator to Azure using the Azure Developer CLI (azd).

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Azure Subscription**: [Get free trial](https://azure.microsoft.com/free/)
- ✅ **Azure Developer CLI**: [Install azd](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- ✅ **Node.js 20+**: [Download](https://nodejs.org/)
- ✅ **Python 3.11+**: [Download](https://python.org/)
- ✅ **Git**: [Download](https://git-scm.com/)

## 🎯 Quick Deployment (5 minutes)

### Option 1: Deploy from GitHub Template

```bash
# Initialize directly from GitHub
azd init --template https://github.com/Aryanjstar/AI-Career-Navigator
cd AI-Career-Navigator

# Authenticate with Azure
azd auth login

# Deploy everything with one command
azd up
```

### Option 2: Clone and Deploy

```bash
# Clone the repository
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Initialize azd in the project
azd init

# Authenticate and deploy
azd auth login
azd up
```

## ⚙️ Detailed Setup

### 1. Environment Configuration

```bash
# Create a new environment
azd env new ai-career-navigator-prod

# Set required environment variables
azd env set AZURE_OPENAI_SERVICE_NAME "your-openai-service"
azd env set AZURE_OPENAI_DEPLOYMENT_NAME "gpt-4"
azd env set AZURE_SEARCH_SERVICE "your-search-service"
azd env set AZURE_STORAGE_ACCOUNT "your-storage-account"
```

### 2. Azure Resource Provisioning

The `azd up` command will create:

| Resource | Purpose | Estimated Cost/Month |
|----------|---------|---------------------|
| **App Service** | Web hosting | $13-25 |
| **Azure OpenAI** | AI services | $30-100 |
| **AI Search** | Document search | $25-50 |
| **Storage Account** | File storage | $5-15 |
| **Application Insights** | Monitoring | $0-10 |
| **Key Vault** | Secrets | $3-5 |

### 3. Post-Deployment Configuration

After deployment, configure these settings:

#### Azure OpenAI Setup
```bash
# If you don't have Azure OpenAI, create it
az cognitiveservices account create \
  --name your-openai-service \
  --resource-group rg-ai-career-navigator \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy GPT-4 model
az cognitiveservices account deployment create \
  --name your-openai-service \
  --resource-group rg-ai-career-navigator \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version "0613"
```

#### Application Settings
```bash
# Update app settings with your values
azd env set AZURE_OPENAI_API_KEY "$(az cognitiveservices account keys list --name your-openai-service --resource-group rg-ai-career-navigator --query key1 -o tsv)"
azd env set AZURE_OPENAI_ENDPOINT "https://your-openai-service.openai.azure.com/"

# Redeploy with new settings
azd deploy
```

## 🔧 Local Development Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies  
cd ../backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Create environment files:

**Frontend (.env.local):**
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_APP_TITLE="AI Career Navigator - Dev"
```

**Backend (.env):**
```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Search
AZURE_SEARCH_SERVICE=your-search-service
AZURE_SEARCH_INDEX=career-navigator-index
AZURE_SEARCH_API_KEY=your-search-key

# Azure Storage
AZURE_STORAGE_ACCOUNT=your-storage-account
AZURE_STORAGE_CONTAINER=resumes
AZURE_STORAGE_CONNECTION_STRING=your-connection-string

# Development settings
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### 3. Start Development Servers

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend  
npm run dev
```

Access the application:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔄 CI/CD Pipeline Setup

### GitHub Actions Workflow

The project includes automated CI/CD. To set it up:

1. **Fork the repository** to your GitHub account

2. **Configure GitHub secrets**:
   ```
   AZURE_CREDENTIALS: Your Azure service principal
   AZURE_CLIENT_ID: Service principal client ID
   AZURE_CLIENT_SECRET: Service principal secret
   AZURE_TENANT_ID: Your Azure tenant ID
   ```

3. **Create service principal**:
   ```bash
   az ad sp create-for-rbac --name "ai-career-navigator-sp" \
     --role contributor \
     --scopes /subscriptions/{subscription-id} \
     --sdk-auth
   ```

4. **Enable GitHub Actions**: Push to main branch triggers deployment

### Manual Deployment Commands

```bash
# Deploy only backend
azd deploy backend

# Deploy only frontend  
azd deploy frontend

# Deploy with custom environment
azd deploy --environment staging

# View deployment status
azd show

# Stream logs
azd logs --follow
```

## 🔍 Monitoring & Troubleshooting

### Health Checks

```bash
# Check application health
curl https://your-app-name.azurewebsites.net/api/health

# Check backend API
curl https://your-app-name.azurewebsites.net/api/docs

# View application insights
az monitor app-insights component show \
  --app your-app-insights \
  --resource-group rg-ai-career-navigator
```

### Common Issues

#### 1. OpenAI API Errors
```bash
# Verify OpenAI configuration
azd env get-values | grep AZURE_OPENAI

# Test API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://your-resource.openai.azure.com/openai/models?api-version=2024-02-01"
```

#### 2. Build Failures
```bash
# Clear caches
rm -rf frontend/node_modules frontend/dist
rm -rf backend/__pycache__ backend/.pytest_cache

# Reinstall dependencies
cd frontend && npm install
cd backend && pip install -r requirements.txt --force-reinstall
```

#### 3. Resource Conflicts
```bash
# Check resource status
azd show --output table

# Clean up and redeploy
azd down --force --purge
azd up
```

## 💰 Cost Management

### Resource Optimization

```bash
# Scale down for development
azd env set APP_SERVICE_SKU "B1"
azd env set AZURE_SEARCH_SKU "basic"

# Scale up for production
azd env set APP_SERVICE_SKU "P1v2"
azd env set AZURE_SEARCH_SKU "standard"
```

### Monitoring Costs

```bash
# Set up cost alerts
az consumption budget create \
  --budget-name "ai-career-navigator-budget" \
  --amount 100 \
  --time-grain Monthly \
  --time-period start-date=2024-01-01
```

## 🔒 Security Configuration

### Environment Variables

Never commit these to version control:
- `AZURE_OPENAI_API_KEY`
- `AZURE_SEARCH_API_KEY`
- `AZURE_STORAGE_CONNECTION_STRING`
- Any `*_SECRET` or `*_PASSWORD` variables

### Key Vault Integration

```bash
# Store secrets in Key Vault
az keyvault secret set \
  --vault-name your-keyvault \
  --name "azure-openai-api-key" \
  --value "your-secret-key"

# Reference in app settings
azd env set AZURE_OPENAI_API_KEY "@Microsoft.KeyVault(VaultName=your-keyvault;SecretName=azure-openai-api-key)"
```

## 📊 Performance Optimization

### Caching Configuration

```python
# Backend caching
CACHE_CONFIG = {
    "redis_url": os.getenv("REDIS_CONNECTION_STRING"),
    "cache_ttl": int(os.getenv("CACHE_TTL_MINUTES", 60)) * 60,
    "max_connections": 10
}
```

### CDN Setup

```bash
# Enable Azure CDN for static assets
az cdn profile create \
  --name ai-career-navigator-cdn \
  --resource-group rg-ai-career-navigator \
  --sku Standard_Microsoft
```

## 🚀 Production Checklist

Before going live:

- [ ] **SSL Certificate**: Verify HTTPS is working
- [ ] **Custom Domain**: Configure your domain name
- [ ] **Monitoring**: Set up alerts and dashboards  
- [ ] **Backup**: Configure automated backups
- [ ] **Security**: Review access policies and permissions
- [ ] **Performance**: Run load tests and optimize
- [ ] **Documentation**: Update user guides and API docs
- [ ] **Support**: Set up error tracking and user feedback

## 📞 Support

Need help with deployment?

- 📚 [Azure Developer CLI Docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- 💬 [GitHub Discussions](https://github.com/Aryanjstar/AI-Career-Navigator/discussions)
- 🐛 [Report Issues](https://github.com/Aryanjstar/AI-Career-Navigator/issues)
- 📧 [Email Support](mailto:aryanjstar@gmail.com)

---

**🎉 Congratulations! Your AI Career Navigator is now live!**
