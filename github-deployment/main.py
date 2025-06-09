"""
Growth Accelerator Platform - Azure Production Entry Point
Forces Flask application deployment
"""

import os
import logging

# Set up production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import Flask app
from app import app, db

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

# Production configuration
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Ensure this is recognized as a Flask application
application = app

# Health check endpoint for Azure
@app.route('/health')
def health_check():
    return {"status": "healthy", "app": "Growth Accelerator Platform Flask"}, 200

# Root route override
@app.route('/')
def force_flask_index():
    return staffing_app.index()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Growth Accelerator Platform Flask App on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
