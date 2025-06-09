import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, redirect, url_for, flash, session

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure for Azure
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

@app.route('/')
def index():
    """Landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Growth Accelerator Platform</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
            .header { text-align: center; margin-bottom: 40px; }
            .logo { font-size: 2.5em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
            .tagline { font-size: 1.2em; color: #7f8c8d; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0; }
            .feature { padding: 30px; background: #ecf0f1; border-radius: 8px; text-align: center; }
            .feature h3 { color: #2c3e50; margin-bottom: 15px; }
            .nav { text-align: center; margin: 40px 0; }
            .nav a { display: inline-block; padding: 12px 24px; margin: 0 10px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            .nav a:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">Growth Accelerator Platform</div>
                <div class="tagline">Intelligent Staffing & Recruitment Management</div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>AI-Powered Matching</h3>
                    <p>Advanced algorithms match candidates with perfect job opportunities</p>
                </div>
                <div class="feature">
                    <h3>Workable Integration</h3>
                    <p>Seamless integration with Workable ATS for streamlined workflows</p>
                </div>
                <div class="feature">
                    <h3>Real-time Analytics</h3>
                    <p>Comprehensive insights into recruitment performance and trends</p>
                </div>
            </div>
            
            <div class="nav">
                <a href="/workspace">Enter Workspace</a>
                <a href="/login">Login</a>
                <a href="/azure-status">System Status</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/workspace')
def workspace():
    """Workspace page"""
    return """
    <h1>Growth Accelerator Workspace</h1>
    <p>Welcome to the Growth Accelerator Platform workspace.</p>
    <a href="/">Return to Home</a>
    """

@app.route('/login')
def login():
    """Login page"""
    return """
    <h1>Login</h1>
    <p>Login functionality for Growth Accelerator Platform.</p>
    <a href="/">Return to Home</a>
    """

@app.route('/logout')
def logout():
    """Logout with proper session handling"""
    session.clear()
    flash("You have been successfully logged out", "success")
    return redirect(url_for('index'))

@app.route('/azure-status')
def azure_status():
    """Azure deployment status"""
    return {
        "status": "healthy",
        "app": "Growth Accelerator Platform",
        "platform": "Azure Web App",
        "domain": "ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net",
        "custom_domain": "app.growthaccelerator.nl"
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "ok", "app": "Growth Accelerator Platform Flask"}

# Azure WSGI application
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
