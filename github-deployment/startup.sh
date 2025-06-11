#!/bin/bash
echo "Initializing Growth Accelerator Platform on Azure..."
cd /home/site/wwwroot
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH
python -m gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=300 --keep-alive=2 app:application
