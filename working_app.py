#!/usr/bin/env python3
"""
Working Growth Accelerator Platform with Real Workable Data
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify
from services.workable_api import get_workable_jobs_real, get_workable_candidates_real

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Homepage with real Workable data summary"""
    try:
        # Get actual counts from Workable API
        jobs = get_workable_jobs_real()
        candidates = get_workable_candidates_real()
        
        return jsonify({
            'status': 'success',
            'platform': 'Growth Accelerator Platform',
            'data_source': 'Real Workable API',
            'workable_account': 'growthacceleratorstaffing.workable.com',
            'jobs_count': len(jobs),
            'candidates_count': len(candidates),
            'api_endpoints': {
                'jobs': '/api/jobs',
                'candidates': '/api/candidates'
            },
            'sample_data': {
                'first_job': jobs[0].get('title') if jobs else 'No jobs',
                'first_candidate': candidates[0].get('name') if candidates else 'No candidates'
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/jobs')
def api_jobs():
    """Jobs API endpoint with real Workable data"""
    try:
        jobs = get_workable_jobs_real()
        return jsonify({
            'success': True,
            'jobs': jobs,
            'count': len(jobs),
            'source': 'workable_api'
        })
    except Exception as e:
        logger.error(f"Error in jobs API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
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
            'source': 'workable_api'
        })
    except Exception as e:
        logger.error(f"Error in candidates API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Growth Accelerator Platform',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)