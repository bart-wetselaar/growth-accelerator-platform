#!/bin/bash
# Kudu deployment script for Azure Web App

echo "Starting Kudu deployment..."

# Set paths
DEPLOYMENT_SOURCE=${BASH_SOURCE[0]%/*}
DEPLOYMENT_TARGET=${HOME}/site/wwwroot

# Copy files
cp -r github-deployment/* $DEPLOYMENT_TARGET/

echo "Deployment completed"
