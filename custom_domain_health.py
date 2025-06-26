"""
Enhanced Health Check for Custom Domain Deployment
"""

from flask import request, jsonify
import os
from datetime import datetime

def create_health_endpoint(app):
    """Add enhanced health check endpoint"""
    
    @app.route('/health')
    def health_check():
        """Comprehensive health check for custom domain"""
        
        # Get request info
        host = request.headers.get('Host', 'unknown')
        user_agent = request.headers.get('User-Agent', 'unknown')
        
        # Determine deployment type
        is_custom_domain = 'growthaccelerator.nl' in host
        is_azure_webapp = 'azurewebsites.net' in host
        is_replit = 'replit' in host
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'host': host,
            'deployment_info': {
                'custom_domain': is_custom_domain,
                'azure_webapp': is_azure_webapp,
                'replit_dev': is_replit,
                'environment': os.environ.get('FLASK_ENV', 'development')
            },
            'platform_urls': {
                'custom_domain': 'https://app.growthaccelerator.nl',
                'azure_webapp': 'https://ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net',
                'replit_dev': 'https://eb44c92f-21f3-4aed-9cb2-28ca14f82460-00-296c0ebbkj4nd.riker.replit.dev'
            },
            'features': {
                'workable_api': True,
                'ai_suggestions': True,
                'self_solving_system': True,
                'integration_sdk': True
            }
        }
        
        return jsonify(health_data)
    
    return app
