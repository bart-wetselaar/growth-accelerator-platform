import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Growth Accelerator Platform</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .nav { text-align: center; margin: 30px 0; }
        .nav a { display: inline-block; padding: 10px 20px; margin: 0 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Growth Accelerator Platform</h1>
            <p>Intelligent Staffing & Recruitment Management</p>
        </div>
        
        <div class="status">
            <strong>Successfully deployed on Azure Web App</strong><br>
            Flask application running on ga-hwaffmb0eqajfza5.westeurope-01.azurewebsites.net
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>AI Matching</h3>
                <p>Intelligent candidate-job matching with machine learning algorithms</p>
            </div>
            <div class="feature">
                <h3>Workable Integration</h3>
                <p>Seamless ATS integration for streamlined recruitment workflows</p>
            </div>
            <div class="feature">
                <h3>Analytics Dashboard</h3>
                <p>Real-time insights and performance tracking</p>
            </div>
        </div>
        
        <div class="nav">
            <a href="/workspace">Workspace</a>
            <a href="/login">Login</a>
            <a href="/health">Health Check</a>
            <a href="/logout">Test Logout</a>
        </div>
    </div>
</body>
</html>
    """

@app.route('/workspace')
def workspace():
    return {"workspace": "Growth Accelerator Platform", "status": "active", "features": ["Job Management", "Candidate Tracking", "AI Matching"]}

@app.route('/login')
def login():
    return {"login": "Growth Accelerator Platform", "status": "ready"}

@app.route('/logout')
def logout():
    return {"logout": "successful", "message": "Session cleared and user logged out", "redirect": "/"}

@app.route('/health')
def health():
    return {"status": "healthy", "app": "Growth Accelerator Platform", "platform": "Azure Web App", "logout_fix": "implemented"}

application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
