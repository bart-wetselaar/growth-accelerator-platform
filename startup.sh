#!/bin/bash
echo "Starting Growth Accelerator Platform on Azure..."

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export FLASK_APP=main.py
export FLASK_ENV=production

# Change to app directory
cd /home/site/wwwroot

# Install dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .deps_installed
fi

# Start the application
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --preload main:app
