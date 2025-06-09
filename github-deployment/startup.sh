#!/bin/bash
echo "=== Growth Accelerator Platform Flask Startup ==="
cd /home/site/wwwroot
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed"
echo "Starting Flask application with Gunicorn..."
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=4 main:app
