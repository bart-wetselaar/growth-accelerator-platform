#!/bin/bash
# Azure Web App startup script for Growth Accelerator Platform
echo "Starting Growth Accelerator Platform (Flask) on Azure..."

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export FLASK_APP=main.py
export FLASK_ENV=production

# Navigate to app directory
cd /home/site/wwwroot

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
fi

# Start Flask application with Gunicorn
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --preload main:app
