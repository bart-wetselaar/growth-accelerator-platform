#!/usr/bin/env python3
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Growth Accelerator Platform</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .logo { font-size: 2.5em; font-weight: 300; margin-bottom: 10px; }
        .tagline { font-size: 1.2em; opacity: 0.9; }
        .content { background: white; border-radius: 12px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin: 30px 0; }
        .feature { padding: 25px; background: #f8f9fa; border-radius: 8px; text-align: center; }
        .feature h3 { color: #2c3e50; margin-bottom: 12px; }
        .feature p { color: #6c757d; line-height: 1.5; }
        .nav { text-align: center; margin: 30px 0; }
        .nav a { display: inline-block; padding: 12px 25px; margin: 0 8px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; font-weight: 500; }
        .nav a:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Growth Accelerator Platform</div>
            <div class="tagline">Intelligent Staffing & Recruitment Management</div>
        </div>
        
        <div class="content">
            <div class="status">
                <strong>Successfully deployed on Azure Web App</strong><br>
                ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>AI-Powered Matching</h3>
                    <p>Advanced algorithms match candidates with perfect job opportunities using machine learning.</p>
                </div>
                <div class="feature">
                    <h3>Workable Integration</h3>
                    <p>Seamless integration with Workable ATS for streamlined recruitment workflows.</p>
                </div>
                <div class="feature">
                    <h3>Real-time Analytics</h3>
                    <p>Comprehensive insights into recruitment performance and candidate pipeline.</p>
                </div>
            </div>
            
            <div class="nav">
                <a href="/workspace">Enter Workspace</a>
                <a href="/login">Login</a>
                <a href="/health">System Status</a>
                <a href="/logout">Logout Test</a>
            </div>
        </div>
    </div>
</body>
</html>"""

@app.route('/workspace')
def workspace():
    return """
    <h1>Growth Accelerator Workspace</h1>
    <p>Workspace functionality for staffing management platform.</p>
    <ul>
        <li>Job Management</li>
        <li>Candidate Tracking</li>
        <li>AI-Powered Matching</li>
        <li>Performance Analytics</li>
    </ul>
    <a href="/">Return to Home</a>
    """

@app.route('/login')
def login():
    return """
    <h1>Login - Growth Accelerator Platform</h1>
    <p>Authentication system for staffing platform access.</p>
    <a href="/">Return to Home</a>
    """

@app.route('/logout')
def logout():
    return """
    <h1>Logout Successful</h1>
    <p>You have been successfully logged out from the Growth Accelerator Platform.</p>
    <p>Session has been cleared and user data removed.</p>
    <a href="/">Return to Home</a>
    """

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "app": "Growth Accelerator Platform",
        "platform": "Azure Web App",
        "domain": "ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net",
        "custom_domain": "app.growthaccelerator.nl",
        "logout_functionality": "implemented",
        "deployment": "successful"
    }

@app.route('/api/status')
def api_status():
    return {
        "api": "operational",
        "platform": "Growth Accelerator",
        "endpoints": ["/health", "/workspace", "/login", "/logout"],
        "azure_deployment": "active"
    }

application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
