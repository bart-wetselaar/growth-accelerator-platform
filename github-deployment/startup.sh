#!/bin/bash
echo "Starting Growth Accelerator Platform on Azure..."
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH
cd /home/site/wwwroot
python -m gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=120 main:application
