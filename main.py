#!/usr/bin/env python3
"""
Growth Accelerator Platform - Main Application
Real Workable API Integration
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from services.workable_api import get_workable_jobs_real, get_workable_candidates_real

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def home():
    """Homepage with Enter Workspace landing page"""
    try:
        from flask import render_template
        return render_template('staffing_app/landing.html')
    except Exception as e:
        logger.error(f"Error loading landing page: {str(e)}")
        # Fallback to simple HTML if template not found
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Growth Accelerator Platform</title>
            <style>
                body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
                            border-radius: 15px; backdrop-filter: blur(10px); }
                h1 { font-size: 3rem; margin-bottom: 1rem; }
                p { font-size: 1.2rem; margin-bottom: 2rem; }
                .btn { background: #4CAF50; color: white; padding: 15px 30px; font-size: 1.2rem; 
                       border: none; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; }
                .btn:hover { background: #45a049; }
                .stats { margin-top: 2rem; font-size: 0.9rem; opacity: 0.8; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Growth Accelerator Platform</h1>
                <p>Staffing & Recruitment Management</p>
                <a href="/workspace" class="btn">Enter Workspace</a>
                <div class="stats">
                    <p>Connected to Workable API • Real recruitment data</p>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/api/jobs')
def api_jobs():
    """Jobs API endpoint with real Workable data"""
    try:
        jobs = get_workable_jobs_real()
        return jsonify({
            'success': True,
            'jobs': jobs,
            'count': len(jobs),
            'source': 'workable_api',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in jobs API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/candidates')
def api_candidates():
    """Candidates API endpoint with real Workable data"""
    try:
        candidates = get_workable_candidates_real()
        return jsonify({
            'success': True,
            'candidates': candidates,
            'count': len(candidates),
            'source': 'workable_api',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in candidates API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/workspace')
def workspace():
    """Workspace dashboard with real Workable data"""
    try:
        # Get real data from Workable API
        jobs = get_workable_jobs_real()
        candidates = get_workable_candidates_real()
        
        return jsonify({
            'status': 'success',
            'platform': 'Growth Accelerator Platform',
            'data_source': 'Real Workable API',
            'workable_account': 'growthacceleratorstaffing.workable.com',
            'stats': {
                'jobs_count': len(jobs),
                'candidates_count': len(candidates)
            },
            'api_endpoints': {
                'jobs': '/api/jobs',
                'candidates': '/api/candidates',
                'health': '/health'
            },
            'sample_data': {
                'first_job': jobs[0].get('title') if jobs else 'No jobs available',
                'first_candidate': candidates[0].get('name') if candidates else 'No candidates available'
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in workspace route: {str(e)}")
        return jsonify({
            'status': 'error',
            'platform': 'Growth Accelerator Platform',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Growth Accelerator Platform',
        'workable_connection': 'active',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    logger.info("Starting Growth Accelerator Platform with real Workable data")
    app.run(host='0.0.0.0', port=5000, debug=True)