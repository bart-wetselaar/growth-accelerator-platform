"""
Growth Accelerator Platform - Azure Production Entry Point
Configured for ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
"""

import os
import logging
from flask import Flask

# Configure logging for Azure
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=== GROWTH ACCELERATOR PLATFORM STARTING ON AZURE ===")
logger.info("Domain: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net")

# Import Flask app
from app import app, db

# Import models and routes
try:
    import models
    logger.info("Models imported successfully")
except Exception as e:
    logger.error(f"Models import error: {str(e)}")

try:
    import staffing_app
    logger.info("Staffing app routes imported successfully")
except Exception as e:
    logger.error(f"Staffing app import error: {str(e)}")

# Initialize database
try:
    with app.app_context():
        if app.config.get('SQLALCHEMY_DATABASE_URI'):
            db.create_all()
            logger.info("Database initialized")
        else:
            logger.info("No database configured")
except Exception as e:
    logger.error(f"Database error: {str(e)}")

# Azure production configuration
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Health check for Azure
@app.route('/azure-status')
def azure_status():
    return {
        "status": "healthy",
        "app": "Growth Accelerator Platform",
        "domain": "ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net",
        "custom_domain": "app.growthaccelerator.nl",
        "version": "1.0"
    }, 200

# Override default route to ensure Flask serves content
@app.route('/test-flask')
def test_flask():
    return "<h1>Growth Accelerator Platform Flask App Active</h1><p>Deployed on Azure Web App</p>"

# WSGI application for Azure
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
