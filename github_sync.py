#!/usr/bin/env python3
"""
GitHub Synchronization with Self-Debugging Integration
Ensures Replit, GitHub, and Azure stay synchronized with error handling
"""

import os
import json
import requests
import logging
from datetime import datetime
from error_handler import error_handler, debug_errors
from self_diagnostic import diagnostic_system

logger = logging.getLogger('GitHubSync')

class GitHubSyncManager:
    def __init__(self):
        self.github_token = os.environ.get('GITHUB_TOKEN_CLASSIC')
        self.repo_owner = os.environ.get('GITHUB_REPO_OWNER', 'bart-wetselaar')
        self.repo_name = os.environ.get('GITHUB_REPO_NAME', 'growth-accelerator-platform')
        self.base_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}'
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
    @debug_errors
    def sync_replit_to_github(self):
        """Sync Replit changes to GitHub with error handling integration"""
        try:
            # Run diagnostics before sync
            diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            logger.info(f"Pre-sync diagnostics: {diagnostics['system_status']}")
            
            # Get current file structure
            files_to_sync = self._get_replit_files()
            
            # Sync core application files
            sync_results = []
            for file_path, content in files_to_sync.items():
                result = self._upload_file_to_github(file_path, content)
                sync_results.append({
                    'file': file_path,
                    'success': result,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Update GitHub with diagnostics data
            self._upload_diagnostics_to_github(diagnostics)
            
            logger.info(f"GitHub sync completed. {len([r for r in sync_results if r['success']])} files synced")
            return sync_results
            
        except Exception as e:
            error_handler.handle_error(e, "github_sync")
            logger.error(f"GitHub sync failed: {e}")
            return []
    
    def _get_replit_files(self):
        """Get current Replit files for synchronization"""
        files_to_sync = {}
        
        # Core application files
        core_files = [
            'main.py', 'app.py', 'staffing_app.py', 'models.py',
            'error_handler.py', 'self_diagnostic.py', 'auto_recovery.py',
            'azure_error_handler.py', 'startup.py', 'web.config',
            '.github/workflows/azure-deploy.yml'
        ]
        
        for file_path in core_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        files_to_sync[file_path] = f.read()
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
        
        # Template files
        template_dir = 'templates'
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                files_to_sync[file_path] = f.read()
                        except Exception as e:
                            logger.warning(f"Could not read template {file_path}: {e}")
        
        # Static files
        static_dir = 'static'
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    if file.endswith(('.css', '.js', '.png', '.jpg', '.svg')):
                        file_path = os.path.join(root, file)
                        try:
                            if file.endswith(('.png', '.jpg')):
                                # Handle binary files
                                with open(file_path, 'rb') as f:
                                    import base64
                                    files_to_sync[file_path] = base64.b64encode(f.read()).decode('utf-8')
                            else:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    files_to_sync[file_path] = f.read()
                        except Exception as e:
                            logger.warning(f"Could not read static file {file_path}: {e}")
        
        return files_to_sync
    
    def _upload_file_to_github(self, file_path, content):
        """Upload single file to GitHub"""
        try:
            # Get current file SHA if it exists
            url = f"{self.base_url}/contents/{file_path}"
            response = requests.get(url, headers=self.headers)
            
            data = {
                'message': f'Sync from Replit: Update {file_path}',
                'content': self._encode_content(content, file_path),
                'branch': 'main'
            }
            
            if response.status_code == 200:
                # File exists, include SHA for update
                data['sha'] = response.json()['sha']
            
            # Upload/update file
            response = requests.put(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                logger.info(f"Successfully synced {file_path} to GitHub")
                return True
            else:
                logger.error(f"Failed to sync {file_path}: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error syncing {file_path}: {e}")
            return False
    
    def _encode_content(self, content, file_path):
        """Encode content for GitHub API"""
        import base64
        
        # Check if content is already base64 encoded (binary files)
        if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return content  # Already base64 encoded
        else:
            return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    def _upload_diagnostics_to_github(self, diagnostics):
        """Upload diagnostics data to GitHub"""
        try:
            diagnostics_content = json.dumps(diagnostics, indent=2)
            self._upload_file_to_github('diagnostics.json', diagnostics_content)
            
            # Create deployment status file
            deployment_status = {
                'last_sync': datetime.now().isoformat(),
                'system_status': diagnostics['system_status'],
                'replit_to_github': True,
                'azure_ready': diagnostics['system_status'] != 'critical',
                'auto_fixes_applied': diagnostics.get('auto_fixes_applied', [])
            }
            
            status_content = json.dumps(deployment_status, indent=2)
            self._upload_file_to_github('deployment_status.json', status_content)
            
        except Exception as e:
            logger.error(f"Failed to upload diagnostics: {e}")
    
    @debug_errors
    def setup_github_repo(self):
        """Set up GitHub repository with proper configuration"""
        try:
            # Create repository if it doesn't exist
            repo_data = {
                'name': self.repo_name,
                'description': 'Growth Accelerator Platform - Staffing & Recruitment Management with Self-Debugging',
                'private': False,
                'auto_init': True
            }
            
            create_url = f'https://api.github.com/user/repos'
            response = requests.post(create_url, headers=self.headers, json=repo_data)
            
            if response.status_code == 201:
                logger.info("GitHub repository created successfully")
            elif response.status_code == 422:
                logger.info("GitHub repository already exists")
            else:
                logger.warning(f"Repository creation response: {response.status_code}")
            
            # Set up repository settings for Azure deployment
            self._setup_repository_secrets()
            
            return True
            
        except Exception as e:
            logger.error(f"GitHub repository setup failed: {e}")
            return False
    
    def _setup_repository_secrets(self):
        """Set up GitHub secrets for Azure deployment"""
        try:
            # Note: Setting secrets requires additional GitHub API permissions
            # This would typically be done manually in GitHub settings
            logger.info("Repository secrets should be configured manually in GitHub settings")
            logger.info("Required secrets: AZURE_WEBAPP_PUBLISH_PROFILE")
            
        except Exception as e:
            logger.error(f"Failed to set up repository secrets: {e}")

# Global sync manager
github_sync = GitHubSyncManager()

@debug_errors
def sync_platforms():
    """Sync all platforms: Replit → GitHub → Azure"""
    try:
        # Run pre-sync diagnostics
        diagnostics = diagnostic_system.run_comprehensive_diagnostics()
        
        if diagnostics['system_status'] == 'critical':
            logger.warning("Critical system issues detected. Attempting auto-recovery before sync.")
            # Trigger auto-recovery
            from auto_recovery import auto_recovery
            auto_recovery._initiate_recovery()
        
        # Sync to GitHub
        sync_results = github_sync.sync_replit_to_github()
        
        return {
            'sync_timestamp': datetime.now().isoformat(),
            'diagnostics': diagnostics,
            'github_sync': sync_results,
            'total_files_synced': len([r for r in sync_results if r['success']])
        }
        
    except Exception as e:
        error_handler.handle_error(e, "platform_sync")
        return {'error': str(e), 'timestamp': datetime.now().isoformat()}

if __name__ == "__main__":
    # Run platform synchronization
    result = sync_platforms()
    print(json.dumps(result, indent=2))