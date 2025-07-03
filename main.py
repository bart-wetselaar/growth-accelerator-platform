from app import app
from datetime import datetime
import os

# Azure Web App Configuration for webapp.growthaccelerator.nl
AZURE_WEBAPP_NAME = os.environ.get('AZURE_WEBAPP_NAME', 'ga-hwaffmb0eqajfza5')
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN', 'webapp.growthaccelerator.nl')
AZURE_WEBAPP_URL = f"{AZURE_WEBAPP_NAME}.westeurope-01.azurewebsites.net"

# Configure Flask for Azure Web App
if app:
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    
    # Health check endpoint for Azure Web App
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'platform': 'Growth Accelerator Platform',
            'azure_webapp': AZURE_WEBAPP_NAME,
            'custom_domain': CUSTOM_DOMAIN,
            'webapp_url': AZURE_WEBAPP_URL,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0'
        }, 200
    
    # Domain configuration endpoint
    @app.route('/domain-config')
    def domain_config():
        return {
            'custom_domain': CUSTOM_DOMAIN,
            'azure_webapp': AZURE_WEBAPP_URL,
            'dns_configured': True,
            'record_type': 'TXT',
            'ttl': 3600
        }, 200
    
    # Azure Web App status
    @app.route('/azure-status')
    def azure_status():
        return {
            'azure_webapp_name': AZURE_WEBAPP_NAME,
            'location': 'westeurope',
            'resource_group': 'growth-accelerator',
            'custom_domain_configured': True,
            'https_enabled': True,
            'status': 'active'
        }, 200

if __name__ == '__main__':
    print(f"Growth Accelerator Platform configured for Azure Web App: {AZURE_WEBAPP_URL}")
    print(f"Custom domain: {CUSTOM_DOMAIN}")
    
    # Only run if not in Azure environment
    if not os.environ.get('WEBSITE_SITE_NAME'):
        app.run(host='0.0.0.0', port=5000, debug=True)
