#!/bin/bash
# Azure Web App startup script for Growth Accelerator Platform

# Set environment variables
export PYTHONPATH=/home/site/wwwroot
export FLASK_APP=main.py
export FLASK_ENV=production

# Install dependencies if needed
if [ ! -d "/home/site/wwwroot/venv" ]; then
    python -m venv /home/site/wwwroot/venv
    source /home/site/wwwroot/venv/bin/activate
    pip install -r requirements.txt
else
    source /home/site/wwwroot/venv/bin/activate
fi

# Start Gunicorn
cd /home/site/wwwroot
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 main:app
