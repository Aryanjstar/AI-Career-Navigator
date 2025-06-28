#!/usr/bin/env python3

import os
import sys
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from load_azd_env import load_azd_env

# WEBSITE_HOSTNAME is always set by App Service, RUNNING_IN_PRODUCTION is set in main.bicep
RUNNING_ON_AZURE = os.getenv("WEBSITE_HOSTNAME") is not None or os.getenv("RUNNING_IN_PRODUCTION") is not None

if not RUNNING_ON_AZURE:
    load_azd_env()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the application
app = create_app()

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    # For production (gunicorn)
    logger.info("Starting AI Career Navigator backend")
    logger.info(f"OpenAI Host: {os.getenv('OPENAI_HOST')}")
    logger.info(f"Azure OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"Azure OpenAI Model: {os.getenv('AZURE_OPENAI_CHATGPT_MODEL')}")
