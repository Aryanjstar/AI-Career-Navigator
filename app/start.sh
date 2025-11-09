#!/bin/sh

# AI Career Navigator - Start Script
# Updated for clean repository structure

# cd into the parent directory of the script
cd "${0%/*}" || exit 1
cd ../

echo "🚀 Starting AI Career Navigator..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating python virtual environment '.venv'"
    python3 -m venv .venv
    echo ""
fi

echo "Installing/updating python packages..."
./.venv/bin/python -m pip install -r requirements.txt
out=$?
if [ $out -ne 0 ]; then
    echo "❌ Failed to install python packages"
    exit $out
fi

echo ""
echo "✅ Dependencies installed successfully"
echo ""

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "📋 Loading environment variables from .env file"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  Warning: .env file not found. Please create one with your Azure OpenAI credentials."
fi

echo ""
echo "🌐 Starting AI Career Navigator Pro..."
echo "📍 Application will be available at: http://localhost:8000"
echo ""

# Start the application using the clean career_navigator_pro.py
./.venv/bin/python build/career_navigator_pro.py
out=$?
if [ $out -ne 0 ]; then
    echo "❌ Failed to start application"
    exit $out
fi
