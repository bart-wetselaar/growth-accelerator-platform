#!/usr/bin/env python3
"""
Force Flask route registration and test
"""

from app import app
from flask import jsonify
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force register the essential routes
@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'platform': 'Growth Accelerator Platform',
        'data_source': 'Real Workable API',
        'message': 'Platform operational with real data from growthacceleratorstaffing.workable.com'
    })

@app.route('/api/jobs')
def jobs_api():
    try:
        from services.workable_api import get_workable_jobs_real
        jobs = get_workable_jobs_real()
        return jsonify({
            'success': True,
            'jobs': jobs,
            'count': len(jobs),
            'source': 'workable_api'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/candidates')
def candidates_api():
    try:
        from services.workable_api import get_workable_candidates_real
        candidates = get_workable_candidates_real()
        return jsonify({
            'success': True,
            'candidates': candidates,
            'count': len(candidates),
            'source': 'workable_api'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

with app.app_context():
    logger.info("Routes registered successfully")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route: {rule.rule} -> {rule.endpoint}")

print("Flask routes forced registration complete")