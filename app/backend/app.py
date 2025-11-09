"""
AI Career Navigator - Main Application
Modular Flask application with clean architecture
"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

from config import (
    FLASK_HOST,
    FLASK_PORT,
    FLASK_DEBUG,
    APP_NAME,
    APP_VERSION,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_MODEL,
    AZURE_OPENAI_DEPLOYMENT,
    LOG_FORMAT,
    LOG_LEVEL,
    validate_config
)
from routes.api_routes import api_bp
from services.ai_service import get_client

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Register Blueprints
app.register_blueprint(api_bp)

# Health check endpoint
@app.route('/health')
def health_check():
    """Comprehensive health check"""
    client_status = get_client()
    health_status = {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "openai_configured": bool(client_status),
            "endpoint": bool(AZURE_OPENAI_ENDPOINT),
            "api_key": bool(AZURE_OPENAI_API_KEY)
        }
    }
    
    status_code = 200 if client_status else 503
    return jsonify(health_status), status_code

# Keep-alive endpoint for FREE tier
@app.route('/ping')
def ping():
    """Simple ping endpoint to keep app alive"""
    return jsonify({"status": "pong", "timestamp": datetime.utcnow().isoformat()})

@app.route('/')
def home():
    """Serve the responsive Career Navigator template"""
    try:
        with open('template_responsive.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Template file not found!")
        return jsonify({"error": "Template not found"}), 500

@app.route('/config')
def config():
    """API configuration endpoint"""
    return jsonify({
        "platform": APP_NAME,
        "version": f"{APP_VERSION}-production",
        "ai": {
            "model": AZURE_OPENAI_MODEL,
            "deployment": AZURE_OPENAI_DEPLOYMENT,
            "endpoint_configured": bool(AZURE_OPENAI_ENDPOINT),
            "api_key_configured": bool(AZURE_OPENAI_API_KEY),
            "status": "connected" if get_client() else "disconnected"
        },
        "features": {
            "career_chat": True,
            "resume_analysis": True,
            "interview_prep": True,
            "skill_assessment": True
        },
        "tech_stack": ["Python", "Flask", "Azure OpenAI", "React", "Tailwind CSS"],
        "responsive": True,
        "developer": {
            "name": "Aryan Jaiswal",
            "email": "aryanjstar3@gmail.com",
            "linkedin": "https://www.linkedin.com/in/aryanjstar",
            "github": "https://github.com/Aryanjstar/AI-Career-Navigator"
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {APP_NAME} (Production)")
    logger.info("=" * 60)
    logger.info(f"Azure OpenAI Endpoint: {AZURE_OPENAI_ENDPOINT}")
    logger.info(f"Azure OpenAI Model: {AZURE_OPENAI_MODEL}")
    logger.info(f"Client Status: {'✅ Connected' if get_client() else '❌ Not Connected'}")
    logger.info("=" * 60)
    
    # Validate configuration
    validate_config()
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
