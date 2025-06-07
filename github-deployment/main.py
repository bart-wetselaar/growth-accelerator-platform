"""
Growth Accelerator Platform - GA App Entry Point
Configured for Azure GA Web App deployment in GA_group resource group
"""

import os
import logging
from app import app, db

# Configure logging for GA app
logging.basicConfig(
    level=logging.INFO,
    format='[GA-APP] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import models and routes
try:
    import models
    logger.info("GA App: Models imported successfully")
except Exception as e:
    logger.error(f"GA App: Error importing models: {str(e)}")

try:
    import staffing_app
    logger.info("GA App: Staffing app routes imported successfully")
except Exception as e:
    logger.error(f"GA App: Error importing staffing app: {str(e)}")

# GA-specific configuration
app.config['AZURE_APP_NAME'] = 'GA'
app.config['AZURE_RESOURCE_GROUP'] = 'GA_group'
app.config['DEPLOYMENT_SOURCE'] = 'github-deployment'

# Create all tables within app context
try:
    with app.app_context():
        if hasattr(app.config, 'SQLALCHEMY_DATABASE_URI') and app.config.get('SQLALCHEMY_DATABASE_URI'):
            db.create_all()
            logger.info("GA App: Database tables created successfully")
        else:
            logger.info("GA App: No database configured, skipping table creation")
except Exception as e:
    logger.error(f"GA App: Database table creation failed: {str(e)}")

# Production configuration for GA
if os.environ.get('PORT') or os.environ.get('AZURE_APP_NAME') == 'GA':
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    logger.info("GA App: Production environment detected")

# Application instance for Azure GA deployment
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Growth Accelerator Platform (GA App) on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
