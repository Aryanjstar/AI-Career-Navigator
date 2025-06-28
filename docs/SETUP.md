# 📖 Setup Guide

Complete installation and configuration guide for AI Career Navigator.

## 📋 Prerequisites

### Required Software
- **Node.js 20+** and npm - [Download](https://nodejs.org/)
- **Python 3.11+** and pip - [Download](https://python.org/)
- **Git** - [Download](https://git-scm.com/)
- **Visual Studio Code** (recommended) - [Download](https://code.visualstudio.com/)

### Azure Requirements
- **Azure Subscription** - [Get free trial](https://azure.microsoft.com/free/)
- **Azure Developer CLI (azd)** - [Installation guide](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)

## ⚡ Quick Start Options

### Option 1: One-Click Azure Deployment

```bash
# Clone the repository
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Authenticate with Azure
azd auth login

# Deploy everything to Azure (provisions resources + deploys code)
azd up
```

This command will:
- ✅ Provision all Azure resources (App Service, OpenAI, Search, Storage)
- ✅ Configure environment variables and secrets
- ✅ Deploy both frontend and backend
- ✅ Set up monitoring and analytics
- ✅ Provide you with live URLs

### Option 2: Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# 2. Install frontend dependencies
cd frontend
npm install

# 3. Install backend dependencies
cd ../backend
pip install -r requirements.txt

# 4. Set up environment configuration
cp .env.example .env
# Edit .env with your Azure service configurations

# 5. Run the application
# Terminal 1 - Backend
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## ⚙️ Environment Configuration

### Frontend Environment (.env.local)

Create `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_APP_TITLE="AI Career Navigator - Dev"
VITE_ENABLE_ANALYTICS=false
```

### Backend Environment (.env)

Create `backend/.env`:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_CHATGPT_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Search
AZURE_SEARCH_SERVICE=your-search-service
AZURE_SEARCH_INDEX=career-navigator-index
AZURE_SEARCH_API_KEY=your-search-api-key

# Azure Storage
AZURE_STORAGE_ACCOUNT=your-storage-account
AZURE_STORAGE_KEY=your-storage-key
AZURE_STORAGE_CONTAINER=resumes

# Database
DATABASE_URL=sqlite:///./career_navigator.db

# Application Settings
SECRET_KEY=your-secret-key-here
DEBUG=true
ENABLE_ANALYTICS=true
MAX_FILE_SIZE_MB=10
```

## 🔧 Azure Services Setup

### 1. Azure OpenAI Service

```bash
# Create Azure OpenAI resource
az cognitiveservices account create \
  --name your-openai-service \
  --resource-group your-resource-group \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy GPT-4 model
az cognitiveservices account deployment create \
  --name your-openai-service \
  --resource-group your-resource-group \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version 0613
```

### 2. Azure AI Search

```bash
# Create Azure AI Search service
az search service create \
  --name your-search-service \
  --resource-group your-resource-group \
  --sku Basic \
  --location eastus
```

### 3. Azure Storage Account

```bash
# Create storage account
az storage account create \
  --name your-storage-account \
  --resource-group your-resource-group \
  --location eastus \
  --sku Standard_LRS

# Create container for resumes
az storage container create \
  --name resumes \
  --account-name your-storage-account
```

## 🧪 Testing the Setup

### Backend API Tests

```bash
cd backend

# Test API health
curl http://localhost:8000/health

# Test Azure OpenAI connection
curl -X POST http://localhost:8000/api/test-openai \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, test!"}'

# Run unit tests
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend

# Run component tests
npm test

# Run end-to-end tests
npm run test:e2e

# Check build
npm run build
```

## 🐛 Troubleshooting

### Common Issues

#### Azure OpenAI Connection Failed
```bash
# Check your environment variables
echo $AZURE_OPENAI_ENDPOINT
echo $AZURE_OPENAI_API_KEY

# Test connectivity
curl -H "Authorization: Bearer $AZURE_OPENAI_API_KEY" \
  "$AZURE_OPENAI_ENDPOINT/openai/models?api-version=2024-02-01"
```

#### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 20+
```

#### Backend Python Issues
```bash
# Create fresh virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

## 🚀 Next Steps

After successful setup:

1. **Explore the Application**: Upload a test resume and job description
2. **Read the Architecture Guide**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
3. **Check Development Workflow**: [docs/DEVELOPMENT.md](DEVELOPMENT.md)
4. **Deploy to Production**: [docs/DEPLOYMENT.md](DEPLOYMENT.md)

## 📞 Getting Help

- **📧 Email**: [aryanjstar@gmail.com](mailto:aryanjstar@gmail.com)
- **🐛 Issues**: [GitHub Issues](https://github.com/Aryanjstar/AI-Career-Navigator/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Aryanjstar/AI-Career-Navigator/discussions)
