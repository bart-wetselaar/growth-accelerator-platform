"""
Real Workable API Integration
Fetches live job and candidate data from Workable API
"""
import os
import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class WorkableAPIService:
    def __init__(self):
        self.api_key = os.environ.get('WORKABLE_API_KEY')
        self.subdomain = os.environ.get('WORKABLE_SUBDOMAIN', 'growthacceleratorstaffing')
        self.base_url = f"https://{self.subdomain}.workable.com/spi/v3"
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test connection on initialization
        self.connected = self._test_connection()
        
    def _test_connection(self) -> bool:
        """Test Workable API connection"""
        try:
            if not self.api_key or not self.subdomain:
                logger.warning("Workable API credentials not provided")
                return False
                
            response = requests.get(f"{self.base_url}/jobs", headers=self.headers, timeout=10)
            if response.status_code == 200:
                logger.info("✓ Workable API connection successful")
                return True
            else:
                logger.error(f"Workable API connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Workable API connection error: {str(e)}")
            return False
    
    def get_jobs(self, limit: int = 100) -> List[Dict]:
        """Fetch jobs from Workable API"""
        if not self.connected:
            return []
            
        try:
            response = requests.get(
                f"{self.base_url}/jobs",
                headers=self.headers,
                params={'limit': limit},  # Get all jobs (published and archived)
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                logger.info(f"Retrieved {len(jobs)} jobs from Workable API")
                
                # Transform jobs to our format
                formatted_jobs = []
                for job in jobs:
                    formatted_job = {
                        'id': job.get('id'),
                        'title': job.get('title'),
                        'description': job.get('description', ''),
                        'requirements': job.get('requirements', []),
                        'department': job.get('department'),
                        'employment_type': job.get('employment_type'),
                        'experience_level': job.get('experience_level'),
                        'location': job.get('location', {}),
                        'created_at': job.get('created_at'),
                        'status': job.get('state', 'published'),
                        'application_url': f"/apply/{job.get('shortcode', job.get('id'))}",
                        'applications': job.get('candidate_count', 0),
                        'benefits': job.get('benefits', []),
                        'salary_min': job.get('salary_min'),
                        'salary_max': job.get('salary_max'),
                        'rate_min': job.get('salary_min'),
                        'rate_max': job.get('salary_max')
                    }
                    formatted_jobs.append(formatted_job)
                    
                return formatted_jobs
            else:
                logger.error(f"Failed to fetch jobs: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching jobs from Workable: {str(e)}")
            return []
    
    def get_candidates(self, limit: int = 100) -> List[Dict]:
        """Fetch candidates from Workable API"""
        if not self.connected:
            return []
            
        try:
            response = requests.get(
                f"{self.base_url}/candidates",
                headers=self.headers,
                params={'limit': 1000},  # Get up to 1000 candidates
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                logger.info(f"Retrieved {len(candidates)} candidates from Workable API")
                
                # Transform candidates to our format
                formatted_candidates = []
                for candidate in candidates:
                    formatted_candidate = {
                        'id': candidate.get('id'),
                        'first_name': candidate.get('firstname', ''),
                        'last_name': candidate.get('lastname', ''),
                        'name': f"{candidate.get('firstname', '')} {candidate.get('lastname', '')}".strip(),
                        'email': candidate.get('email'),
                        'phone': candidate.get('phone'),
                        'created_at': candidate.get('created_at'),
                        'stage': candidate.get('stage'),
                        'status': candidate.get('stage', 'new'),
                        'domain': candidate.get('domain', 'General'),
                        'experience': candidate.get('experience_level', 'mid'),
                        'skills': candidate.get('skills', []),
                        'current_position': candidate.get('headline', ''),
                        'cover_letter': candidate.get('cover_letter', ''),
                        'resume_url': candidate.get('resume_url'),
                        'applications': len(candidate.get('jobs', [])),
                        'hourly_rate': candidate.get('salary_expectation')
                    }
                    formatted_candidates.append(formatted_candidate)
                    
                return formatted_candidates
            else:
                logger.error(f"Failed to fetch candidates: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching candidates from Workable: {str(e)}")
            return []
    
    def get_job_details(self, job_id: str) -> Optional[Dict]:
        """Get detailed information for a specific job"""
        if not self.connected:
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/jobs/{job_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                job = response.json()
                logger.info(f"Retrieved job details for ID {job_id}")
                return job
            else:
                logger.error(f"Failed to fetch job details: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching job details: {str(e)}")
            return None
    
    def get_candidate_details(self, candidate_id: str) -> Optional[Dict]:
        """Get detailed information for a specific candidate"""
        if not self.connected:
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/candidates/{candidate_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                candidate = response.json()
                logger.info(f"Retrieved candidate details for ID {candidate_id}")
                return candidate
            else:
                logger.error(f"Failed to fetch candidate details: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching candidate details: {str(e)}")
            return None

# Global instance
workable_api = WorkableAPIService()

def validate_workable_api_key() -> bool:
    """Validate if Workable API is properly configured"""
    return workable_api.connected