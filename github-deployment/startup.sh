#!/bin/bash
echo "Starting Growth Accelerator Platform for GA App (Resource Group: GA_group)..."
cd /home/site/wwwroot

# Set GA-specific environment variables
export AZURE_APP_NAME=GA
export AZURE_RESOURCE_GROUP=GA_group
export FLASK_ENV=production
export DEPLOYMENT_SOURCE=github-deployment

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start application with GA-specific configuration
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info main:app
