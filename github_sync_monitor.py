#!/usr/bin/env python3
"""
GitHub Sync Monitor
Ensures code stays synchronized between Replit and GitHub
"""

import requests
import time
import threading
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GitHubSyncMonitor')

class GitHubSyncMonitor:
    def __init__(self):
        self.github_repo = "bart-wetselaar/growth-accelerator-platform"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}"
        self.token = os.environ.get('GITHUB_TOKEN_CLASSIC')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        } if self.token else {}
        self.check_interval = 600  # 10 minutes
        self.running = True
        
    def check_repo_status(self):
        """Check GitHub repository status"""
        try:
            response = requests.get(self.github_api_url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                repo_data = response.json()
                last_push = repo_data.get('pushed_at')
                
                logger.info(f"✓ GitHub repo accessible, last push: {last_push}")
                return True
            else:
                logger.warning(f"GitHub repo check failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to check GitHub repo: {str(e)}")
            return False
    
    def check_recent_commits(self):
        """Check for recent commits"""
        try:
            commits_url = f"{self.github_api_url}/commits"
            response = requests.get(commits_url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                commits = response.json()
                if commits:
                    latest_commit = commits[0]
                    commit_date = latest_commit['commit']['author']['date']
                    commit_message = latest_commit['commit']['message']
                    
                    logger.info(f"✓ Latest commit: {commit_message[:50]}... ({commit_date})")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to check commits: {str(e)}")
            
        return False
    
    def check_workflow_status(self):
        """Check GitHub Actions workflow status"""
        try:
            workflows_url = f"{self.github_api_url}/actions/runs"
            response = requests.get(workflows_url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                runs = response.json().get('workflow_runs', [])
                if runs:
                    latest_run = runs[0]
                    status = latest_run.get('status')
                    conclusion = latest_run.get('conclusion')
                    
                    logger.info(f"✓ Latest workflow: {status} ({conclusion})")
                    return True
                    
        except Exception as e:
            logger.error(f"Failed to check workflows: {str(e)}")
            
        return False
    
    def sync_monitoring_loop(self):
        """Main sync monitoring loop"""
        while self.running:
            logger.info("Checking GitHub synchronization...")
            
            # Check repository status
            repo_ok = self.check_repo_status()
            
            # Check recent commits
            commits_ok = self.check_recent_commits()
            
            # Check workflow status
            workflows_ok = self.check_workflow_status()
            
            if repo_ok and commits_ok:
                logger.info("✓ GitHub sync healthy")
            else:
                logger.warning("⚠ GitHub sync issues detected")
            
            time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """Start GitHub sync monitoring"""
        if not self.token:
            logger.warning("GitHub token not available, monitoring disabled")
            return None
            
        thread = threading.Thread(target=self.sync_monitoring_loop, daemon=True)
        thread.start()
        logger.info("GitHub sync monitoring started")
        return thread
    
    def get_sync_status(self):
        """Get current sync status"""
        try:
            repo_status = self.check_repo_status()
            return {
                'status': 'healthy' if repo_status else 'degraded',
                'repo': self.github_repo,
                'last_check': datetime.now().isoformat()
            }
        except:
            return {'status': 'error', 'repo': self.github_repo}

# Global instance
github_monitor = GitHubSyncMonitor()

def start_github_sync_monitoring():
    """Start GitHub sync monitoring"""
    return github_monitor.start_monitoring()

def get_github_sync_status():
    """Get GitHub sync status"""
    return github_monitor.get_sync_status()

if __name__ == "__main__":
    monitor = GitHubSyncMonitor()
    try:
        monitor.sync_monitoring_loop()
    except KeyboardInterrupt:
        logger.info("GitHub sync monitoring stopped")