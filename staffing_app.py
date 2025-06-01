"""
Growth Accelerator Staffing Platform - Core Application
"""
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db = SQLAlchemy(app)

# Workable API Integration
WORKABLE_API_KEY = os.environ.get("WORKABLE_API_KEY")
WORKABLE_SUBDOMAIN = "growthacceleratorstaffing"

def get_workable_candidates():
    """Fetch candidates from Workable API"""
    if not WORKABLE_API_KEY:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {WORKABLE_API_KEY}"}
        response = requests.get(
            f"https://{WORKABLE_SUBDOMAIN}.workable.com/spi/v3/candidates",
            headers=headers
        )
        if response.status_code == 200:
            return response.json().get("candidates", [])
    except Exception as e:
        print(f"Workable API error: {e}")
    
    return []

def get_workable_jobs():
    """Fetch jobs from Workable API"""
    if not WORKABLE_API_KEY:
        return []
    
    try:
        headers = {"Authorization": f"Bearer {WORKABLE_API_KEY}"}
        response = requests.get(
            f"https://{WORKABLE_SUBDOMAIN}.workable.com/spi/v3/jobs",
            headers=headers
        )
        if response.status_code == 200:
            return response.json().get("jobs", [])
    except Exception as e:
        print(f"Workable API error: {e}")
    
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    candidates = get_workable_candidates()
    jobs = get_workable_jobs()
    return render_template('dashboard.html', 
                         candidates=candidates[:10], 
                         jobs=jobs[:10])

@app.route('/candidates')
def candidates():
    candidates_data = get_workable_candidates()
    return render_template('candidates.html', candidates=candidates_data)

@app.route('/jobs')
def jobs():
    jobs_data = get_workable_jobs()
    return render_template('jobs.html', jobs=jobs_data)

@app.route('/api/candidates')
def api_candidates():
    return jsonify(get_workable_candidates())

@app.route('/api/jobs')
def api_jobs():
    return jsonify(get_workable_jobs())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)