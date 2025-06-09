"""
Growth Accelerator Platform - Azure Flask App
Explicit Flask application entry point
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the Flask app
from app import app, db

logger.info("=== GROWTH ACCELERATOR PLATFORM FLASK APP STARTING ===")

# Import models and routes
try:
    import models
    logger.info("Models imported successfully")
except Exception as e:
    logger.error(f"Error importing models: {str(e)}")

try:
    import staffing_app
    logger.info("Staffing app routes imported successfully")
except Exception as e:
    logger.error(f"Error importing staffing app: {str(e)}")

# Initialize database
try:
    with app.app_context():
        if app.config.get('SQLALCHEMY_DATABASE_URI'):
            db.create_all()
            logger.info("Database tables created successfully")
        else:
            logger.info("No database configured, skipping table creation")
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")

# Production configuration for Azure
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Override routes to ensure Flask app is served
@app.route('/azure-health')
def azure_health():
    """Azure-specific health check"""
    return {
        "status": "healthy",
        "app": "Growth Accelerator Platform Flask",
        "platform": "Azure Web App",
        "version": "1.0"
    }, 200

@app.route('/app-info')
def app_info():
    """Application information endpoint"""
    return {
        "name": "Growth Accelerator Platform",
        "type": "Flask Application",
        "deployment": "Azure Web App",
        "status": "active"
    }, 200

# Ensure this is the WSGI application
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Growth Accelerator Platform Flask App on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
