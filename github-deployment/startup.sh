#!/bin/bash
echo "Starting Growth Accelerator Platform..."
gunicorn --bind=0.0.0.0 --timeout 600 main:application
