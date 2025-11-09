"""
Configuration module for AI Career Navigator
Centralizes all configuration settings
"""
import os
import logging

logger = logging.getLogger(__name__)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

# Flask Configuration
FLASK_PORT = int(os.getenv("PORT", "8000"))
FLASK_HOST = os.getenv("HOST", "0.0.0.0")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Application Metadata
APP_NAME = "AI Career Navigator"
APP_VERSION = "2.0.1"
APP_DESCRIPTION = "Production-ready AI Career Guidance Platform"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'

# Validate Configuration
def validate_config():
    """Validate that required configuration is present"""
    missing = []
    
    if not AZURE_OPENAI_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not AZURE_OPENAI_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")
    
    if missing:
        logger.warning(f"⚠️ Missing configuration: {', '.join(missing)}")
        return False
    
    logger.info("✅ Configuration validated successfully")
    return True

