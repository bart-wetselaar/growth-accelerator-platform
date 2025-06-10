"""
Growth Accelerator Platform - Main Entry Point
Production-ready deployment configuration
"""

import os
import logging
from app import app, db

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import models to register them with SQLAlchemy
try:
    import models
    logger.info("Models imported successfully")
except Exception as e:
    logger.error(f"Error importing models: {str(e)}")

# Import routes
try:
    import staffing_app
    logger.info("Staffing app routes imported successfully")
except Exception as e:
    logger.error(f"Error importing staffing app: {str(e)}")

# Create all tables within app context with error handling
try:
    with app.app_context():
        if hasattr(app.config, 'SQLALCHEMY_DATABASE_URI') and app.config.get('SQLALCHEMY_DATABASE_URI'):
            db.create_all()
            logger.info("Database tables created successfully")
        else:
            logger.info("No database configured, skipping table creation")
except Exception as e:
    logger.error(f"Database table creation failed: {str(e)}")
    logger.info("Application will continue without database connectivity")

# Auto-sync deployment to GitHub and Azure
try:
    import replit_deploy_hook
    logger.info("Deployment sync hook activated")
except Exception as e:
    logger.warning(f"Deployment sync hook not available: {e}")

# Production configuration
if os.environ.get('REPLIT_DEPLOYMENT') or os.environ.get('PORT'):
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    logger.info("Production environment detected")

# Configure for Replit deployment
app.config['SERVER_NAME'] = None  # Allow any domain
app.config['APPLICATION_ROOT'] = '/'

# Ensure application is available for production deployment
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Growth Accelerator Platform on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
