#!/usr/bin/env python3
"""
Azure Startup Script for Growth Accelerator Platform
Handles Azure-specific initialization and error recovery
"""

import os
import sys
import logging
from datetime import datetime

# Azure environment setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('azure_startup.log')
    ]
)
logger = logging.getLogger('AzureStartup')

def setup_azure_environment():
    """Setup Azure-specific environment variables and configurations"""
    try:
        # Set default environment variables for Azure
        os.environ.setdefault('FLASK_ENV', 'production')
        os.environ.setdefault('SESSION_SECRET', 'ga-azure-production-key-2025')
        
        # Azure database URL handling
        if not os.environ.get('DATABASE_URL') and os.environ.get('WEBSITE_HOSTNAME'):
            logger.warning("No DATABASE_URL found in Azure environment")
            # Set a fallback in-memory database for emergency operation
            os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        
        logger.info("Azure environment setup completed")
        
    except Exception as e:
        logger.error(f"Azure environment setup failed: {e}")

def initialize_app():
    """Initialize the Flask application with Azure optimizations"""
    try:
        setup_azure_environment()
        
        # Import Azure error handler first
        from azure_error_handler import azure_error_handler
        
        # Import and initialize the application
        from main import app, logger as main_logger
        
        main_logger.info("Starting Growth Accelerator Platform on Azure")
        main_logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'unknown')}")
        main_logger.info(f"Host: {os.environ.get('WEBSITE_HOSTNAME', 'localhost')}")
        
        # Add Azure error monitoring routes
        @app.route('/azure-errors')
        def azure_errors():
            return jsonify(azure_error_handler.get_error_summary())
        
        @app.route('/azure-recovery', methods=['POST'])
        def azure_recovery():
            try:
                error_type = request.json.get('error_type', 'general')
                success = azure_error_handler.attempt_recovery(error_type)
                return jsonify({
                    'recovery_successful': success,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'recovery_successful': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        return app
        
    except Exception as e:
        logger.error(f"Application initialization failed: {e}")
        
        # Initialize Azure error handler for emergency mode
        try:
            from azure_error_handler import azure_error_handler
            azure_error_handler.handle_azure_error(e, "initialization")
        except:
            pass
        
        # Return a minimal emergency app
        from flask import Flask, jsonify, request
        emergency_app = Flask(__name__)
        
        @emergency_app.route('/')
        def emergency_status():
            return jsonify({
                'status': 'emergency_mode',
                'message': 'Growth Accelerator Platform initializing, please wait...',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'azure_info': {
                    'hostname': os.environ.get('WEBSITE_HOSTNAME', 'unknown'),
                    'site_name': os.environ.get('WEBSITE_SITE_NAME', 'unknown')
                }
            })
        
        @emergency_app.route('/health')
        def emergency_health():
            return jsonify({
                'status': 'initializing',
                'service': 'Growth Accelerator Platform',
                'mode': 'emergency',
                'timestamp': datetime.now().isoformat()
            })
        
        @emergency_app.route('/azure-status')
        def emergency_azure_status():
            return jsonify({
                'status': 'emergency',
                'platform': 'Azure Web App',
                'hostname': os.environ.get('WEBSITE_HOSTNAME', 'unknown'),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        return emergency_app

# Initialize the application
app = initialize_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)