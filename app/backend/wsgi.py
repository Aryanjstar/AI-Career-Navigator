"""
WSGI Entry Point for Render Deployment
This ensures proper module imports
"""
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the Flask app
from app import app

# For Gunicorn
application = app

if __name__ == "__main__":
    app.run()

