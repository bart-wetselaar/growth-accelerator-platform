#!/bin/bash
echo "Starting Growth Accelerator Platform on Azure..."
cd /home/site/wwwroot
python -m pip install --upgrade pip
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 600 main:app
