"""
Growth Accelerator Platform - Azure Production Entry Point
"""

import os
import logging
from datetime import datetime
from flask import jsonify
from app import app, db
from sqlalchemy import text

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
    logger.info("Models imported successfully")
except ImportError as e:
    logger.warning(f"Models import: {e}")
except Exception as e:
    logger.error(f"Models import error: {e}")

try:
    # Import staffing_app to register all routes
    import staffing_app
    logger.info("Staffing app imported successfully")
    
    # Force route registration
    with app.app_context():
        route_count = len([rule for rule in app.url_map.iter_rules()])
        logger.info(f"Total routes registered: {route_count}")
    
    # Initialize self-debugging system for Azure
    if is_azure:
        try:
            from error_handler import error_handler
            from auto_recovery import auto_recovery
            auto_recovery.start_monitoring()
            logger.info("Self-debugging system initialized for Azure")
        except Exception as debug_error:
            logger.warning(f"Self-debugging initialization failed: {debug_error}")
            
except ImportError as e:
    logger.warning(f"Staffing app import: {e}")
except Exception as e:
    logger.error(f"Unexpected import error: {e}")

# Register error monitoring routes
@app.route('/health')
def health():
    """Basic health check endpoint"""
    try:
        # Test database connection if available
        db_status = "not_configured"
        if database_url:
            try:
                from sqlalchemy import text
                db.session.execute(text('SELECT 1'))
                db_status = "connected"
            except:
                db_status = "error"
        
        return jsonify({
            "status": "healthy",
            "service": "Growth Accelerator Platform",
            "environment": "Azure" if is_azure else "Development",
            "database": db_status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "service": "Growth Accelerator Platform",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/azure-status')
def azure_status():
    """Azure-specific status endpoint"""
    return jsonify({
        "platform": "Azure Web App",
        "hostname": os.environ.get('WEBSITE_HOSTNAME', 'unknown'),
        "instance_id": os.environ.get('WEBSITE_INSTANCE_ID', 'unknown'),
        "resource_group": os.environ.get('WEBSITE_RESOURCE_GROUP', 'unknown'),
        "site_name": os.environ.get('WEBSITE_SITE_NAME', 'unknown'),
        "timestamp": datetime.now().isoformat()
    })

# Initialize database with Azure-specific handling
database_url = os.environ.get("DATABASE_URL")
with app.app_context():
    try:
        if database_url:
            db.create_all()
            logger.info("Database tables initialized")
        else:
            logger.warning("No database URL configured")
    except Exception as e:
        logger.warning(f"Database initialization: {e}")
        logger.info("Application will continue without database")

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
