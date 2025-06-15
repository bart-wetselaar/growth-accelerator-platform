"""
Growth Accelerator Platform - Azure Production Entry Point
"""

import os
import logging
from app import app, db

# Configure logging for Azure
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Azure environment detection
is_azure = "WEBSITE_HOSTNAME" in os.environ
logger.info(f"Running on {'Azure Web App' if is_azure else 'development environment'}")

# Import application components with error handling
try:
    import models
    import staffing_app
    logger.info("Growth Accelerator Platform components loaded successfully")
except ImportError as e:
    logger.warning(f"Component import: {e}")
except Exception as e:
    logger.error(f"Unexpected import error: {e}")

# Initialize database with Azure-specific handling
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables initialized")
    except Exception as e:
        logger.info(f"Database initialization: {e}")

# Azure production configuration
if is_azure:
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['PREFERRED_URL_SCHEME'] = 'https'

# Ensure WSGI compatibility for Azure
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting Growth Accelerator Platform on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
