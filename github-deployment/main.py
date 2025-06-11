"""
Growth Accelerator Platform - Azure Production
"""

import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Growth Accelerator Platform</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Growth Accelerator Platform</h1>
        <p>Intelligent Staffing & Recruitment Management</p>
    </div>
    
    <div class="status">
        <strong>Azure Web App - Operational</strong><br>
        Successfully deployed with health monitoring
    </div>
    
    <div class="features">
        <div class="feature">
            <h3>AI Matching</h3>
            <p>Intelligent candidate-job matching</p>
        </div>
        <div class="feature">
            <h3>Workable Integration</h3>
            <p>Seamless ATS integration</p>
        </div>
        <div class="feature">
            <h3>Analytics Dashboard</h3>
            <p>Real-time insights</p>
        </div>
    </div>
</body>
</html>
    """)

@app.route('/health')
def health():
    """Azure health check endpoint"""
    return jsonify({
        "status": "healthy",
        "app": "Growth Accelerator Platform",
        "timestamp": "{{ datetime.utcnow().isoformat() }}",
        "version": "1.0.0",
        "environment": "azure_production"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "api": "operational",
        "services": ["workable", "ai_matching", "analytics"],
        "health": "ok"
    })

application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
