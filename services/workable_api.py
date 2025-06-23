#!/usr/bin/env python3
"""
Real Workable API Integration
Fetches actual jobs and candidates data from Workable API
"""

import requests
import os
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class WorkableAPI:
    def __init__(self):
        self.api_key = os.environ.get('WORKABLE_API_KEY')
        self.subdomain = 'growthacceleratorstaffing'
        self.base_url = f"https://{self.subdomain}.workable.com/spi/v3"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
    def _make_request(self, endpoint: str, method: str = 'GET', params: dict = None) -> Optional[Dict]:
        """Make authenticated request to Workable API"""
        if not self.api_key:
            logger.error("Workable API key not configured")
            return None
            
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.error("Workable API authentication failed - check API key")
                return None
            elif response.status_code == 404:
                logger.error("Workable API endpoint not found - check subdomain")
                return None
            else:
                logger.error(f"Workable API error: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Workable API request failed: {str(e)}")
            return None
    
    def get_jobs(self, state: str = None, limit: int = 100) -> List[Dict]:
        """Get jobs from Workable API"""
        params = {'limit': limit}
        if state:
            params['state'] = state
            
        response = self._make_request('jobs', params=params)
        if response and 'jobs' in response:
            jobs = response['jobs']
            logger.info(f"Retrieved {len(jobs)} jobs from Workable API")
            return jobs
        return []
    
    def get_candidates(self, stage: str = None, limit: int = 100) -> List[Dict]:
        """Get candidates from Workable API"""
        params = {'limit': limit}
        if stage:
            params['stage'] = stage
            
        response = self._make_request('candidates', params=params)
        if response and 'candidates' in response:
            candidates = response['candidates']
            logger.info(f"Retrieved {len(candidates)} candidates from Workable API")
            return candidates
        return []
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed job information"""
        response = self._make_request(f'jobs/{job_id}')
        if response:
            logger.info(f"Retrieved details for job {job_id}")
            return response
        return None
    
    def get_candidate_details(self, candidate_id: str) -> Optional[Dict]:
        """Get detailed candidate information"""
        response = self._make_request(f'candidates/{candidate_id}')
        if response:
            logger.info(f"Retrieved details for candidate {candidate_id}")
            return response
        return None
    
    def test_connection(self) -> bool:
        """Test API connection and credentials"""
        try:
            response = self._make_request('jobs', params={'limit': 1})
            if response is not None:
                logger.info("Workable API connection test successful")
                return True
            else:
                logger.error("Workable API connection test failed")
                return False
        except Exception as e:
            logger.error(f"Workable API connection test error: {str(e)}")
            return False

# Global instance
workable_api = WorkableAPI() if os.environ.get('WORKABLE_API_KEY') else None

def get_workable_jobs_real() -> List[Dict]:
    """Get real jobs from Workable API"""
    if not workable_api:
        logger.warning("Workable API not configured")
        return []
    
    try:
        # Get both published and archived jobs
        published_jobs = workable_api.get_jobs(state='published')
        archived_jobs = workable_api.get_jobs(state='archived')
        
        all_jobs = []
        
        # Process published jobs
        for job in published_jobs:
            formatted_job = {
                'id': job.get('id'),
                'title': job.get('title'),
                'full_title': job.get('full_title'),
                'shortcode': job.get('shortcode'),
                'state': job.get('state', 'published'),
                'status': 'published',
                'department': job.get('department', {}).get('name', '') if job.get('department') else '',
                'location': job.get('location', {}),
                'formatted_location': format_location(job.get('location', {})),
                'created_at': job.get('created_at'),
                'updated_at': job.get('updated_at'),
                'employment_type': job.get('employment_type'),
                'experience': job.get('experience'),
                'description': job.get('description', ''),
                'requirements': job.get('requirements', ''),
                'application_url': job.get('application_url', ''),
                'applications': job.get('candidate_count', 0)
            }
            all_jobs.append(formatted_job)
        
        # Process archived jobs
        for job in archived_jobs:
            formatted_job = {
                'id': job.get('id'),
                'title': job.get('title'),
                'state': job.get('state', 'archived'),
                'status': 'archived',
                'department': job.get('department', {}).get('name', '') if job.get('department') else '',
                'location': job.get('location', {}),
                'formatted_location': format_location(job.get('location', {})),
                'created_at': job.get('created_at'),
                'applications': job.get('candidate_count', 0)
            }
            all_jobs.append(formatted_job)
        
        logger.info(f"Retrieved {len(all_jobs)} total jobs from Workable API ({len(published_jobs)} published, {len(archived_jobs)} archived)")
        return all_jobs
        
    except Exception as e:
        logger.error(f"Error fetching jobs from Workable API: {str(e)}")
        return []

def get_workable_candidates_real() -> List[Dict]:
    """Get real candidates from Workable API"""
    if not workable_api:
        logger.warning("Workable API not configured")
        return []
    
    try:
        candidates = workable_api.get_candidates(limit=1000)  # Get up to 1000 candidates
        
        formatted_candidates = []
        for candidate in candidates:
            formatted_candidate = {
                'id': candidate.get('id'),
                'name': candidate.get('name'),
                'first_name': candidate.get('firstname', ''),
                'last_name': candidate.get('lastname', ''),
                'email': candidate.get('email'),
                'phone': candidate.get('phone'),
                'created_at': candidate.get('created_at'),
                'updated_at': candidate.get('updated_at'),
                'stage': candidate.get('stage'),
                'status': map_candidate_status(candidate.get('stage')),
                'summary': candidate.get('summary', ''),
                'cover_letter': candidate.get('cover_letter', ''),
                'resume_url': candidate.get('resume_url', ''),
                'profile_url': candidate.get('profile_url', ''),
                'skills': extract_skills(candidate.get('tags', [])),
                'social_profiles': candidate.get('social_profiles', []),
                'domain': infer_domain_from_tags(candidate.get('tags', [])),
                'experience': infer_experience_level(candidate)
            }
            formatted_candidates.append(formatted_candidate)
        
        logger.info(f"Retrieved {len(formatted_candidates)} candidates from Workable API")
        return formatted_candidates
        
    except Exception as e:
        logger.error(f"Error fetching candidates from Workable API: {str(e)}")
        return []

def format_location(location: Dict) -> str:
    """Format location dictionary into readable string"""
    if not location:
        return "Remote"
    
    parts = []
    if location.get('city'):
        parts.append(location['city'])
    if location.get('region') and location.get('region') != location.get('city'):
        parts.append(location['region'])
    if location.get('country'):
        parts.append(location['country'])
    
    return ', '.join(parts) if parts else "Remote"

def map_candidate_status(stage: str) -> str:
    """Map Workable stage to our status"""
    stage_mapping = {
        'applied': 'applied',
        'sourced': 'applied',
        'phone_interview': 'screening',
        'interview': 'interviewing',
        'technical': 'technical_interview',
        'final': 'final_interview',
        'offer': 'qualified',
        'hired': 'hired',
        'rejected': 'rejected',
        'withdrawn': 'rejected'
    }
    return stage_mapping.get(stage, 'applied')

def extract_skills(tags: List[Dict]) -> List[str]:
    """Extract skills from candidate tags"""
    skills = []
    for tag in tags:
        if tag.get('type') == 'skill' or 'skill' in tag.get('name', '').lower():
            skills.append(tag.get('name', ''))
    return skills

def infer_domain_from_tags(tags: List[Dict]) -> str:
    """Infer professional domain from candidate tags"""
    domain_keywords = {
        'Software Engineering': ['developer', 'engineer', 'programming', 'coding', 'software'],
        'Product Management': ['product', 'manager', 'pm', 'product manager'],
        'Data Science': ['data', 'analytics', 'scientist', 'machine learning'],
        'DevOps Engineering': ['devops', 'infrastructure', 'cloud', 'deployment'],
        'Marketing': ['marketing', 'growth', 'digital marketing'],
        'Sales': ['sales', 'business development', 'account'],
        'Design': ['designer', 'ux', 'ui', 'design'],
        'Finance': ['finance', 'accounting', 'financial'],
        'Human Resources': ['hr', 'human resources', 'recruiting']
    }
    
    tag_text = ' '.join([tag.get('name', '').lower() for tag in tags])
    
    for domain, keywords in domain_keywords.items():
        if any(keyword in tag_text for keyword in keywords):
            return domain
    
    return 'General'

def infer_experience_level(candidate: Dict) -> str:
    """Infer experience level from candidate data"""
    # This is a simplified heuristic - in practice you might use more sophisticated logic
    tags = candidate.get('tags', [])
    tag_text = ' '.join([tag.get('name', '').lower() for tag in tags])
    
    if 'senior' in tag_text or 'lead' in tag_text:
        return 'senior'
    elif 'junior' in tag_text or 'entry' in tag_text:
        return 'junior'
    else:
        return 'mid_level'

# Test connection on import
if workable_api:
    connection_ok = workable_api.test_connection()
    if connection_ok:
        logger.info("✓ Workable API connection established")
    else:
        logger.error("✗ Workable API connection failed")