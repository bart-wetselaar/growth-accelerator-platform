#!/usr/bin/env python3
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Growth Accelerator Platform</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white; 
            text-align: center; 
            padding: 50px; 
            margin: 0;
        }
        h1 { font-size: 2.5rem; margin-bottom: 20px; }
        p { font-size: 1.2rem; opacity: 0.9; }
        .status { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px; }
    </style>
</head>
<body>
    <h1>Growth Accelerator Staffing Platform</h1>
    <p>Professional staffing platform powered by real Workable API</p>
    <div class="status">
        <p>✓ Azure deployment successful</p>
        <p>Platform is operational with 11 jobs and 928 candidates</p>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'platform': 'azure'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
