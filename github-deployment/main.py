from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>Growth Accelerator Platform</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1 style="color: #2c5aa0;">Growth Accelerator Platform</h1>
        <h2 style="color: #28a745;">Azure Web App - Online</h2>
        <p>Intelligent Staffing & Recruitment Management</p>
        <div style="background: #d4edda; padding: 20px; margin: 20px; border-radius: 8px;">
            <strong>Status: Operational</strong><br>
            Health Check: Active<br>
            Platform: Azure Web Apps
        </div>
        <p><a href="/health">Health Check</a> | <a href="/api/status">API Status</a></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "growth-accelerator-platform",
        "environment": "azure-production"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "api": "operational",
        "version": "1.0",
        "services": ["ai_matching", "workable_integration", "analytics"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
