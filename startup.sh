#!/bin/bash

# Azure Web App startup script for Growth Accelerator Platform
echo "Starting Growth Accelerator Platform on Azure..."

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export FLASK_APP=main.py
export FLASK_ENV=production

# Install dependencies if not cached
if [ ! -d "/home/site/wwwroot/.azure_cache" ]; then
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    mkdir -p /home/site/wwwroot/.azure_cache
    echo "Dependencies installed and cached"
else
    echo "Using cached dependencies"
fi

# Start the application
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --preload main:app