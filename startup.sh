#!/bin/bash
# Azure Web App startup script for webapp.growthaccelerator.nl

echo "Starting Growth Accelerator Platform on Azure Web App"
echo "Azure Web App: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net"
echo "Custom Domain: webapp.growthaccelerator.nl"

# Set environment variables
export AZURE_WEBAPP_NAME=ga-hwaffmb0eqajfza5
export CUSTOM_DOMAIN=webapp.growthaccelerator.nl
export FLASK_ENV=production

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start Gunicorn for Azure Web App
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 600 main:app
