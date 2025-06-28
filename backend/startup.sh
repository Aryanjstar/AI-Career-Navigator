#!/bin/bash

# Startup script for AI Career Navigator on Azure App Service
echo "🚀 Starting AI Career Navigator Flask App"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:/home/site/wwwroot"

# Install any missing dependencies
pip install flask-cors

# Set default values for environment variables if not set
export AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION:-"2024-02-15-preview"}
export AZURE_OPENAI_CHATGPT_DEPLOYMENT=${AZURE_OPENAI_CHATGPT_DEPLOYMENT:-"gpt-4.1"}
export AZURE_OPENAI_CHATGPT_MODEL=${AZURE_OPENAI_CHATGPT_MODEL:-"gpt-4.1"}

# Start the application
exec gunicorn --bind=0.0.0.0:$PORT --workers=1 --timeout=230 --access-logfile='-' --error-logfile='-' flask_app:app 