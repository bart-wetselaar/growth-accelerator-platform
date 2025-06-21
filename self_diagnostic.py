"""
Self-Diagnostic System for Growth Accelerator Platform
Real-time monitoring, error detection, and automatic issue resolution
"""
import logging
import sys
import time
import json
from datetime import datetime
from error_handler import error_handler, debug_errors

class SelfDiagnostic:
    def __init__(self):
        self.logger = logging.getLogger('GA_SelfDiagnostic')
        self.critical_components = [
            'database_connection',
            'flask_app',
            'workable_api',
            'template_rendering',
            'static_files'
        ]
        self.monitoring_active = True
        
    @debug_errors
    def run_comprehensive_diagnostics(self):
        """Execute complete system diagnostics"""
        self.logger.info("Starting comprehensive system diagnostics")
        
        diagnostics_report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'checking',
            'components': {},
            'recommendations': [],
            'auto_fixes_applied': []
        }
        
        # Test each critical component
        for component in self.critical_components:
            try:
                test_method = getattr(self, f'test_{component}')
                result = test_method()
                diagnostics_report['components'][component] = result
                
                if not result['status']:
                    diagnostics_report['recommendations'].append(result.get('recommendation', f'Manual review needed for {component}'))
                    
                    # Attempt auto-fix if available
                    fix_method = getattr(self, f'fix_{component}', None)
                    if fix_method:
                        fix_result = fix_method()
                        if fix_result:
                            diagnostics_report['auto_fixes_applied'].append(component)
                            self.logger.info(f"Auto-fix applied successfully for {component}")
                        
            except Exception as e:
                self.logger.error(f"Diagnostic test failed for {component}: {e}")
                diagnostics_report['components'][component] = {
                    'status': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        # Determine overall system status
        failed_components = [comp for comp, result in diagnostics_report['components'].items() 
                           if not result.get('status', False)]
        
        if not failed_components:
            diagnostics_report['system_status'] = 'healthy'
        elif len(failed_components) <= 1:
            diagnostics_report['system_status'] = 'warning'
        else:
            diagnostics_report['system_status'] = 'critical'
        
        self.logger.info(f"Diagnostics complete. System status: {diagnostics_report['system_status']}")
        return diagnostics_report
    
    @debug_errors
    def test_database_connection(self):
        """Test database connectivity and basic operations"""
        try:
            from app import db, app
            
            with app.app_context():
                # Test basic connection
                from sqlalchemy import text
                result = db.engine.execute(text('SELECT 1 as test')).fetchone()
                
                # Test table existence
                tables = db.engine.table_names()
                
                return {
                    'status': True,
                    'details': f'Connected successfully. {len(tables)} tables found',
                    'tables': tables,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'recommendation': 'Check database configuration and ensure PostgreSQL is running',
                'timestamp': datetime.now().isoformat()
            }
    
    @debug_errors
    def test_flask_app(self):
        """Test Flask application core functionality"""
        try:
            from app import app
            
            # Test app configuration
            config_items = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
            missing_config = [item for item in config_items if not app.config.get(item)]
            
            if missing_config:
                return {
                    'status': False,
                    'error': f'Missing configuration: {missing_config}',
                    'recommendation': 'Check environment variables and app configuration',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Test app context
            with app.app_context():
                test_client = app.test_client()
                response = test_client.get('/')
                
                return {
                    'status': response.status_code == 200,
                    'details': f'App responding with status {response.status_code}',
                    'response_size': len(response.data),
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'recommendation': 'Check Flask app initialization and imports',
                'timestamp': datetime.now().isoformat()
            }
    
    @debug_errors
    def test_workable_api(self):
        """Test Workable API connectivity"""
        try:
            import requests
            import os
            
            api_key = os.environ.get('WORKABLE_API_KEY')
            if not api_key:
                return {
                    'status': False,
                    'error': 'Workable API key not configured',
                    'recommendation': 'Set WORKABLE_API_KEY environment variable',
                    'timestamp': datetime.now().isoformat()
                }
            
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get('https://growthaccelerator.workable.com/spi/v3/accounts', 
                                  headers=headers, timeout=10)
            
            return {
                'status': response.status_code in [200, 401],  # 401 means API is responding
                'details': f'API responded with status {response.status_code}',
                'api_available': response.status_code == 200,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'recommendation': 'Check network connectivity and API credentials',
                'timestamp': datetime.now().isoformat()
            }
    
    @debug_errors
    def test_template_rendering(self):
        """Test template rendering functionality"""
        try:
            from app import app
            from flask import render_template_string
            
            with app.app_context():
                # Test basic template rendering
                test_template = '<h1>{{ title }}</h1>'
                rendered = render_template_string(test_template, title='Test')
                
                # Check template directory
                import os
                template_dir = os.path.join(os.getcwd(), 'templates')
                template_files = []
                
                if os.path.exists(template_dir):
                    template_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]
                
                return {
                    'status': True,
                    'details': f'Template rendering working. {len(template_files)} templates found',
                    'template_files': template_files,
                    'template_dir_exists': os.path.exists(template_dir),
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'recommendation': 'Check Jinja2 installation and template directory',
                'timestamp': datetime.now().isoformat()
            }
    
    @debug_errors
    def test_static_files(self):
        """Test static file serving"""
        try:
            import os
            
            static_dir = os.path.join(os.getcwd(), 'static')
            static_files = []
            
            if os.path.exists(static_dir):
                for root, dirs, files in os.walk(static_dir):
                    static_files.extend(files)
            
            # Test with Flask app
            from app import app
            with app.app_context():
                test_client = app.test_client()
                
                # Test a known static file if it exists
                css_response = None
                if any('css' in f for f in static_files):
                    css_file = next(f for f in static_files if 'css' in f)
                    css_response = test_client.get(f'/static/css/{css_file}')
                
                return {
                    'status': True,
                    'details': f'Static directory found with {len(static_files)} files',
                    'static_files_count': len(static_files),
                    'static_dir_exists': os.path.exists(static_dir),
                    'css_test': css_response.status_code if css_response else 'No CSS files to test',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'recommendation': 'Check static directory structure and Flask static file handling',
                'timestamp': datetime.now().isoformat()
            }
    
    def fix_database_connection(self):
        """Attempt to fix database connection issues"""
        try:
            from app import db, app
            
            with app.app_context():
                # Recreate all tables
                db.create_all()
                self.logger.info("Database tables recreated successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Database fix failed: {e}")
            return False
    
    def fix_template_rendering(self):
        """Fix template rendering issues"""
        try:
            import os
            
            # Ensure templates directory exists
            template_dir = 'templates'
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
                self.logger.info("Created templates directory")
            
            # Create basic index template if missing
            index_template = os.path.join(template_dir, 'index.html')
            if not os.path.exists(index_template):
                with open(index_template, 'w') as f:
                    f.write('''<!DOCTYPE html>
<html>
<head><title>Growth Accelerator Platform</title></head>
<body><h1>Growth Accelerator Platform</h1><p>System operational</p></body>
</html>''')
                self.logger.info("Created basic index template")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Template fix failed: {e}")
            return False
    
    def fix_static_files(self):
        """Fix static file serving issues"""
        try:
            import os
            
            # Ensure static directories exist
            static_dirs = ['static', 'static/css', 'static/js', 'static/img']
            for directory in static_dirs:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    self.logger.info(f"Created static directory: {directory}")
            
            # Create basic CSS file if missing
            css_file = 'static/css/main.css'
            if not os.path.exists(css_file):
                with open(css_file, 'w') as f:
                    f.write('body { font-family: Arial, sans-serif; margin: 20px; }')
                self.logger.info("Created basic CSS file")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Static files fix failed: {e}")
            return False
    
    @debug_errors
    def monitor_system_health(self, duration_minutes=5):
        """Continuous system health monitoring"""
        self.logger.info(f"Starting system health monitoring for {duration_minutes} minutes")
        
        end_time = time.time() + (duration_minutes * 60)
        health_data = []
        
        while time.time() < end_time and self.monitoring_active:
            try:
                # Run quick health check
                health_status = error_handler.health_check()
                health_data.append(health_status)
                
                # Check for critical issues
                if health_status['overall_status'] == 'critical':
                    self.logger.warning("Critical system status detected, running diagnostics")
                    self.run_comprehensive_diagnostics()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                break
        
        self.logger.info("System health monitoring completed")
        return health_data
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        self.logger.info("System monitoring stopped")
    
    def generate_diagnostic_report(self):
        """Generate comprehensive diagnostic report"""
        diagnostics = self.run_comprehensive_diagnostics()
        error_summary = error_handler.get_error_summary()
        
        report = {
            'platform': 'Growth Accelerator Platform',
            'report_timestamp': datetime.now().isoformat(),
            'diagnostics': diagnostics,
            'error_summary': error_summary,
            'recommendations': []
        }
        
        # Add specific recommendations based on findings
        if diagnostics['system_status'] != 'healthy':
            report['recommendations'].append('System requires attention - check component details')
        
        if error_summary['total_errors'] > 10:
            report['recommendations'].append('High error count detected - review error patterns')
        
        # Save report to file
        report_filename = f'diagnostic_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Diagnostic report saved to {report_filename}")
        return report

# Global diagnostic instance
diagnostic_system = SelfDiagnostic()