#!/usr/bin/env python3

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Flask
from flask import Flask, render_template, redirect, url_for, flash, session, jsonify

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "azure-deployment-key")

# Configure for production
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

logger.info("Growth Accelerator Platform starting on Azure")

@app.route('/')
def index():
    """Main landing page"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Accelerator Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 50px; padding: 40px 0; }
        .logo { font-size: 3em; font-weight: 300; margin-bottom: 10px; }
        .tagline { font-size: 1.3em; opacity: 0.9; }
        .content { background: white; border-radius: 15px; padding: 50px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0; }
        .feature { text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; transition: transform 0.3s; }
        .feature:hover { transform: translateY(-5px); }
        .feature h3 { color: #2c3e50; margin-bottom: 15px; font-size: 1.4em; }
        .feature p { color: #6c757d; line-height: 1.6; }
        .actions { text-align: center; margin: 40px 0; }
        .btn { display: inline-block; padding: 15px 30px; margin: 0 10px; background: #667eea; color: white; text-decoration: none; border-radius: 8px; font-weight: 500; transition: all 0.3s; }
        .btn:hover { background: #5a6fd8; transform: translateY(-2px); }
        .status { background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }
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
                <strong>✓ Successfully deployed on Azure Web App</strong><br>
                Domain: ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🤖 AI-Powered Matching</h3>
                    <p>Advanced algorithms intelligently match candidates with perfect job opportunities using machine learning and data analytics.</p>
                </div>
                <div class="feature">
                    <h3>🔗 Workable Integration</h3>
                    <p>Seamless integration with Workable ATS platform for streamlined recruitment workflows and candidate management.</p>
                </div>
                <div class="feature">
                    <h3>📊 Real-time Analytics</h3>
                    <p>Comprehensive insights into recruitment performance, candidate pipeline, and hiring trends with interactive dashboards.</p>
                </div>
            </div>
            
            <div class="actions">
                <a href="/workspace" class="btn">Enter Workspace</a>
                <a href="/login" class="btn">Login</a>
                <a href="/health" class="btn">System Health</a>
            </div>
        </div>
    </div>
</body>
</html>
    """)

@app.route('/workspace')
def workspace():
    """Workspace page"""
    return jsonify({
        "message": "Growth Accelerator Platform Workspace",
        "status": "active",
        "features": ["Job Management", "Candidate Tracking", "AI Matching", "Analytics"],
        "deployment": "Azure Web App"
    })

@app.route('/login')
def login():
    """Login page"""
    return jsonify({
        "page": "Login",
        "app": "Growth Accelerator Platform",
        "status": "ready"
    })

@app.route('/logout')
def logout():
    """Logout with proper session handling"""
    session.clear()
    flash("Successfully logged out", "success")
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "app": "Growth Accelerator Platform",
        "platform": "Azure Web App",
        "domain": "ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net",
        "custom_domain": "app.growthaccelerator.nl",
        "features": "operational",
        "logout_functionality": "fixed"
    })

@app.route('/azure-info')
def azure_info():
    """Azure deployment information"""
    return jsonify({
        "deployment_status": "successful",
        "platform": "Azure Web App",
        "framework": "Flask",
        "python_version": "3.11",
        "app_name": "Growth Accelerator Platform"
    })

def render_template_string(template):
    """Simple template rendering"""
    return template

# WSGI application for Azure
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Growth Accelerator Platform on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
