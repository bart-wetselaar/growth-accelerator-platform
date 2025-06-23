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
