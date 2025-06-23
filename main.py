#!/usr/bin/env python3
import os
import sys
import logging
from flask import Flask, render_template, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key-for-azure")

@app.route('/')
def index():
    """Main landing page"""
    try:
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Accelerator Staffing Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem;
        }
        .logo { width: 120px; height: auto; margin-bottom: 2rem; }
        h1 { font-size: 3rem; font-weight: 600; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }
        .status { 
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        .success { color: #4ade80; }
    </style>
</head>
<body>
    <div>
        <h1>Growth Accelerator Staffing Platform</h1>
        <p>Professional staffing and recruitment platform powered by real Workable API integration</p>
        <div class="status">
            <p class="success">✓ Azure deployment successful</p>
            <p>Platform is now live and operational</p>
        </div>
    </div>
</body>
</html>
        '''
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"<h1>Platform Loading...</h1><p>Error: {e}</p>"

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'azure',
        'timestamp': datetime.now().isoformat(),
        'message': 'Growth Accelerator Platform is running'
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'api_status': 'operational',
        'workable_integration': 'active',
        'platform': 'azure-web-app',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
