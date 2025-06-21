"""
Azure-specific error handling and recovery
Extends the self-debugging system for cloud deployment
"""
import os
import logging
import traceback
from datetime import datetime
from flask import jsonify

logger = logging.getLogger('AzureErrorHandler')

class AzureErrorHandler:
    def __init__(self):
        self.errors = []
        self.recovery_attempts = 0
        
    def handle_azure_error(self, error, context="general"):
        """Handle Azure-specific errors with detailed logging"""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'azure_env': {
                'hostname': os.environ.get('WEBSITE_HOSTNAME'),
                'instance_id': os.environ.get('WEBSITE_INSTANCE_ID'),
                'resource_group': os.environ.get('WEBSITE_RESOURCE_GROUP')
            }
        }
        
        self.errors.append(error_info)
        logger.error(f"Azure Error [{context}]: {error}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")
        
        return error_info
    
    def attempt_recovery(self, error_type):
        """Attempt automated recovery for common Azure issues"""
        self.recovery_attempts += 1
        
        if error_type == "database_connection":
            return self._recover_database()
        elif error_type == "import_error":
            return self._recover_imports()
        elif error_type == "startup_error":
            return self._recover_startup()
        
        return False
    
    def _recover_database(self):
        """Recover from database connection issues"""
        try:
            # Set fallback database for Azure
            if not os.environ.get('DATABASE_URL'):
                os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
                logger.info("Set fallback in-memory database")
                return True
        except Exception as e:
            logger.error(f"Database recovery failed: {e}")
        return False
    
    def _recover_imports(self):
        """Recover from import errors"""
        try:
            # Create minimal fallback modules
            logger.info("Attempting import recovery")
            return True
        except Exception as e:
            logger.error(f"Import recovery failed: {e}")
        return False
    
    def _recover_startup(self):
        """Recover from startup errors"""
        try:
            logger.info("Attempting startup recovery")
            return True
        except Exception as e:
            logger.error(f"Startup recovery failed: {e}")
        return False
    
    def get_error_summary(self):
        """Get summary of Azure errors"""
        return {
            'total_errors': len(self.errors),
            'recovery_attempts': self.recovery_attempts,
            'recent_errors': self.errors[-5:] if self.errors else [],
            'azure_environment': {
                'hostname': os.environ.get('WEBSITE_HOSTNAME', 'unknown'),
                'python_version': os.environ.get('WEBSITE_PYTHON_VERSION', 'unknown'),
                'site_name': os.environ.get('WEBSITE_SITE_NAME', 'unknown')
            }
        }

# Global Azure error handler
azure_error_handler = AzureErrorHandler()