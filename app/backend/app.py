#!/usr/bin/env python3
"""
AI Career Navigator - Main Application
Modern, modular Flask application for career guidance
"""
import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern"""
    
    # Initialize Flask app
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Load configuration
    try:
        Config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.warning("Some features may not work without proper configuration")
    
    # Configure Flask
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    # Enable CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    logger.info(f"CORS enabled for origins: {Config.CORS_ORIGINS}")
    
    # Register blueprints
    from routes import api_bp
    app.register_blueprint(api_bp)
    logger.info("API routes registered")
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            "status": "healthy",
            "service": "AI Career Navigator",
            "version": "2.0.0"
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
    
    return app


# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 Starting AI Career Navigator Pro")
    logger.info("=" * 60)
    logger.info(f"Azure OpenAI Endpoint: {Config.AZURE_OPENAI_ENDPOINT}")
    logger.info(f"Azure OpenAI Model: {Config.AZURE_OPENAI_MODEL}")
    logger.info(f"Host: {Config.HOST}:{Config.PORT}")
    logger.info(f"Debug Mode: {Config.DEBUG}")
    logger.info("=" * 60)
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

