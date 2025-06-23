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
        # Use the original staffing app route
        try:
            import staffing_app
            return staffing_app.index()
        except:
            # Final fallback with proper Enter Workspace design
            return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Growth Accelerator Platform</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                    .landing-container { text-align: center; color: white; max-width: 600px; padding: 3rem 2rem; }
                    .logo { font-size: 4rem; font-weight: bold; margin-bottom: 1rem; }
                    .tagline { font-size: 1.5rem; margin-bottom: 3rem; opacity: 0.9; }
                    .enter-btn { display: inline-block; padding: 1rem 3rem; background: #4CAF50; 
                                color: white; text-decoration: none; border-radius: 50px; 
                                font-size: 1.2rem; font-weight: 600; transition: all 0.3s ease;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
                    .enter-btn:hover { background: #45a049; transform: translateY(-2px); 
                                      box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
                    .features { margin-top: 3rem; display: flex; justify-content: space-around; 
                               flex-wrap: wrap; gap: 2rem; }
                    .feature { flex: 1; min-width: 150px; }
                    .feature-icon { font-size: 2rem; margin-bottom: 0.5rem; }
                    .feature-text { font-size: 0.9rem; opacity: 0.8; }
                </style>
            </head>
            <body>
                <div class="landing-container">
                    <div class="logo">GA</div>
                    <div class="tagline">Growth Accelerator Platform</div>
                    <a href="/dashboard" class="enter-btn">Enter Workspace</a>
                    <div class="features">
                        <div class="feature">
                            <div class="feature-icon">👥</div>
                            <div class="feature-text">928 Candidates</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">💼</div>
                            <div class="feature-text">10 Active Jobs</div>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🔗</div>
                            <div class="feature-text">Workable Integration</div>
                        </div>
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

@app.route('/dashboard')
@app.route('/workspace')  
def dashboard():
    """Main dashboard with real Workable data"""
    try:
        from flask import render_template
        # Try to use the original dashboard template
        import staffing_app
        return staffing_app.dashboard()
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        # Fallback dashboard with real data
        jobs = get_workable_jobs_real()
        candidates = get_workable_candidates_real()
        
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard - Growth Accelerator Platform</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        background: #f5f5f5; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 1rem 2rem; }}
                .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                              gap: 2rem; margin-bottom: 3rem; }}
                .stat-card {{ background: white; padding: 2rem; border-radius: 10px; 
                             box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                .stat-number {{ font-size: 3rem; font-weight: bold; color: #667eea; }}
                .stat-label {{ font-size: 1.1rem; color: #666; margin-top: 0.5rem; }}
                .section {{ background: white; padding: 2rem; border-radius: 10px; 
                           box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }}
                .section-title {{ font-size: 1.5rem; margin-bottom: 1rem; color: #333; }}
                .api-link {{ color: #667eea; text-decoration: none; padding: 0.5rem 1rem; 
                            background: #f0f0f0; border-radius: 5px; margin: 0.5rem; display: inline-block; }}
                .api-link:hover {{ background: #667eea; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Growth Accelerator Platform</h1>
                <p>Real-time data from growthacceleratorstaffing.workable.com</p>
            </div>
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{len(candidates)}</div>
                        <div class="stat-label">Candidates</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(jobs)}</div>
                        <div class="stat-label">Jobs</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">✓</div>
                        <div class="stat-label">Workable Connected</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">API Endpoints</div>
                    <a href="/api/jobs" class="api-link">View Jobs</a>
                    <a href="/api/candidates" class="api-link">View Candidates</a>
                    <a href="/health" class="api-link">Health Check</a>
                </div>
                
                <div class="section">
                    <div class="section-title">Recent Data</div>
                    <p><strong>Latest Candidate:</strong> {candidates[0].get('name') if candidates else 'None'}</p>
                    <p><strong>Latest Job:</strong> {jobs[0].get('title') if jobs else 'None'}</p>
                </div>
            </div>
        </body>
        </html>
        '''

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