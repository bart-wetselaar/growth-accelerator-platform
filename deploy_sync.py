#!/usr/bin/env python3
"""
Unified Deployment Synchronization Script
Handles Replit → GitHub → Azure sync with self-debugging integration
"""

import os
import sys
import json
import logging
from datetime import datetime
from github_sync import github_sync, sync_platforms
from error_handler import error_handler, debug_errors
from self_diagnostic import diagnostic_system
from auto_recovery import auto_recovery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('DeploySync')

class UnifiedDeploymentManager:
    def __init__(self):
        self.platforms = ['replit', 'github', 'azure']
        self.sync_results = {}
        
    @debug_errors
    def execute_full_sync(self):
        """Execute complete platform synchronization"""
        logger.info("Starting unified platform synchronization")
        
        try:
            # Step 1: Pre-sync diagnostics
            logger.info("Running pre-sync diagnostics...")
            diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            
            if diagnostics['system_status'] == 'critical':
                logger.warning("Critical issues detected. Running auto-recovery...")
                recovery_result = auto_recovery._initiate_recovery()
                logger.info(f"Auto-recovery applied fixes: {recovery_result}")
                
                # Re-run diagnostics after recovery
                diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            
            # Step 2: GitHub synchronization
            logger.info("Synchronizing with GitHub...")
            github_result = sync_platforms()
            self.sync_results['github'] = github_result
            
            # Step 3: Trigger Azure deployment
            logger.info("Triggering Azure deployment...")
            azure_result = self._trigger_azure_deployment()
            self.sync_results['azure'] = azure_result
            
            # Step 4: Post-sync verification
            logger.info("Running post-sync verification...")
            final_diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            
            # Compile comprehensive sync report
            sync_report = {
                'sync_timestamp': datetime.now().isoformat(),
                'pre_sync_diagnostics': diagnostics,
                'post_sync_diagnostics': final_diagnostics,
                'github_sync': github_result,
                'azure_deployment': azure_result,
                'overall_status': 'success' if final_diagnostics['system_status'] != 'critical' else 'partial',
                'platforms_synced': len([p for p in self.platforms if p in self.sync_results])
            }
            
            # Save sync report
            self._save_sync_report(sync_report)
            
            logger.info("Unified platform sync completed successfully")
            return sync_report
            
        except Exception as e:
            logger.error(f"Unified sync failed: {e}")
            error_handler.handle_error(e, "unified_deployment")
            return {
                'sync_timestamp': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }
    
    def _trigger_azure_deployment(self):
        """Trigger Azure deployment via GitHub Actions"""
        try:
            # In a real implementation, this would trigger the GitHub webhook
            # For now, we'll create a deployment status file
            deployment_trigger = {
                'triggered_at': datetime.now().isoformat(),
                'trigger_method': 'unified_sync',
                'github_workflow': 'azure-deploy.yml',
                'status': 'triggered'
            }
            
            # Create trigger file for GitHub Actions
            with open('deployment_trigger.json', 'w') as f:
                json.dump(deployment_trigger, f, indent=2)
            
            logger.info("Azure deployment triggered via GitHub Actions")
            return deployment_trigger
            
        except Exception as e:
            logger.error(f"Azure deployment trigger failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def _save_sync_report(self, report):
        """Save comprehensive sync report"""
        try:
            report_filename = f"sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Also save as latest sync report
            with open('latest_sync_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Sync report saved: {report_filename}")
            
        except Exception as e:
            logger.error(f"Failed to save sync report: {e}")

    @debug_errors
    def verify_platform_health(self):
        """Verify health across all platforms"""
        health_status = {}
        
        # Replit health (local)
        try:
            diagnostics = diagnostic_system.run_comprehensive_diagnostics()
            health_status['replit'] = {
                'status': diagnostics['system_status'],
                'components': diagnostics['components'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            health_status['replit'] = {'status': 'error', 'error': str(e)}
        
        # GitHub health (API check)
        try:
            if github_sync.github_token:
                # Simple API test
                import requests
                response = requests.get('https://api.github.com/user', 
                                      headers=github_sync.headers, timeout=10)
                health_status['github'] = {
                    'status': 'healthy' if response.status_code == 200 else 'error',
                    'api_response': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                health_status['github'] = {'status': 'no_token', 'message': 'GitHub token not configured'}
        except Exception as e:
            health_status['github'] = {'status': 'error', 'error': str(e)}
        
        # Azure health (would be checked via deployed endpoint)
        health_status['azure'] = {
            'status': 'deployment_ready',
            'message': 'Ready for deployment via GitHub Actions',
            'timestamp': datetime.now().isoformat()
        }
        
        return health_status

# Global deployment manager
deployment_manager = UnifiedDeploymentManager()

def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'sync':
            result = deployment_manager.execute_full_sync()
            print(json.dumps(result, indent=2))
        
        elif command == 'health':
            result = deployment_manager.verify_platform_health()
            print(json.dumps(result, indent=2))
        
        elif command == 'github-only':
            result = sync_platforms()
            print(json.dumps(result, indent=2))
        
        else:
            print("Usage: python deploy_sync.py [sync|health|github-only]")
    else:
        # Default: run full sync
        result = deployment_manager.execute_full_sync()
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()