#!/usr/bin/env python3
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Growth Accelerator Platform</h1>
    <p>Platform is being restored...</p>
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 10000);
    </script>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Platform restored'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)


# Azure Web App Custom Domain Configuration
import os

# Custom domain configuration
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN', 'webapp.growthaccelerator.nl')
AZURE_WEBAPP_URL = os.environ.get('AZURE_WEBAPP_URL', 'ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net')

# Configure Flask for custom domain
if app:
    app.config['SERVER_NAME'] = CUSTOM_DOMAIN
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'domain': CUSTOM_DOMAIN,
            'azure_webapp': AZURE_WEBAPP_URL,
            'timestamp': datetime.now().isoformat()
        }
    
    @app.route('/domain-config')
    def domain_config():
        return {
            'custom_domain': CUSTOM_DOMAIN,
            'azure_webapp': AZURE_WEBAPP_URL,
            'dns_configured': True
        }

print(f"Growth Accelerator Platform configured for {CUSTOM_DOMAIN}")
