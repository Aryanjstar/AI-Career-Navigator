#!/usr/bin/env python3
"""
WSGI entry point for AI Career Navigator
"""
from app import create_app

# Create the application instance
application = create_app()
app = application

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

