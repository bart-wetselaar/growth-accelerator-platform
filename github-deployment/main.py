#!/usr/bin/env python3
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Growth Accelerator Platform</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { color: #2c5aa0; text-align: center; margin-bottom: 30px; }
        .status { background: #d4edda; color: #155724; padding: 20px; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Growth Accelerator Platform</h1>
        <h2>Azure Web App - Operational</h2>
    </div>
    <div class="status">
        <h3>System Status: Healthy</h3>
        <p>Azure deployment successful - Health checks active</p>
    </div>
</body>
</html>"""

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "growth-accelerator-platform"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
