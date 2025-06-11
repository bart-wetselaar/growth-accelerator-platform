#!/usr/bin/env python3
import os
import sys
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Simple home page"""
    return """
<!DOCTYPE html>
<html>
<head><title>Growth Accelerator Platform</title></head>
<body style="font-family: Arial; text-align: center; padding: 50px;">
    <h1 style="color: #2c5aa0;">Growth Accelerator Platform</h1>
    <h2 style="color: #28a745;">Azure Web App - Online</h2>
    <p>Intelligent Staffing & Recruitment Platform</p>
    <div style="background: #d4edda; padding: 20px; margin: 20px; border-radius: 8px;">
        <strong>Status: Operational</strong><br>
        Health Check: Active
    </div>
</body>
</html>
    """

@app.route('/health')
def health():
    """Health check endpoint for Azure"""
    return jsonify({
        "status": "healthy",
        "service": "growth-accelerator-platform",
        "environment": "azure-production"
    })

@app.route('/api/health') 
def api_health():
    """Alternative health endpoint"""
    return health()

# WSGI application object
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting on port {port}")
    app.run(host='0.0.0.0', port=port)
