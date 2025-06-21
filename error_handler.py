"""
Self-Debugging Error Handler for Growth Accelerator Platform
Comprehensive error detection, logging, and automatic resolution
"""
import logging
import traceback
import os
import sys
import time
from datetime import datetime
from functools import wraps
import json
import requests

class ErrorHandler:
    def __init__(self):
        self.error_log_file = 'ga_errors.log'
        self.debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
        self.setup_logging()
        self.error_patterns = {
            'database': ['sqlalchemy', 'database', 'connection', 'psycopg2'],
            'api': ['workable', 'http', 'request', 'api', 'timeout'],
            'template': ['jinja2', 'template', 'render'],
            'import': ['importerror', 'modulenotfounderror', 'no module'],
            'permission': ['permission', 'denied', 'access'],
            'memory': ['memory', 'allocation', 'out of memory'],
            'azure': ['azure', 'deployment', 'publish', 'kudu']
        }
        self.auto_fixes = {
            'database': self.fix_database_issues,
            'api': self.fix_api_issues,
            'template': self.fix_template_issues,
            'import': self.fix_import_issues,
            'permission': self.fix_permission_issues,
            'azure': self.fix_azure_issues
        }
        
    def setup_logging(self):
        """Configure comprehensive logging system"""
        logging.basicConfig(
            level=logging.DEBUG if self.debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.error_log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('GA_ErrorHandler')
        
    def capture_error(self, func):
        """Decorator to capture and analyze errors"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_info = self.analyze_error(e, func.__name__)
                self.log_error(error_info)
                
                # Attempt automatic resolution
                if error_info['auto_fixable']:
                    self.logger.info(f"Attempting auto-fix for {error_info['category']} error")
                    try:
                        fix_result = self.auto_fixes[error_info['category']](error_info)
                        if fix_result:
                            self.logger.info(f"Auto-fix successful for {error_info['category']}")
                            return func(*args, **kwargs)  # Retry after fix
                    except Exception as fix_error:
                        self.logger.error(f"Auto-fix failed: {fix_error}")
                
                # Re-raise if not auto-fixable or fix failed
                raise e
        return wrapper
    
    def analyze_error(self, error, function_name):
        """Analyze error and categorize for automatic resolution"""
        error_str = str(error).lower()
        traceback_str = traceback.format_exc().lower()
        
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'function': function_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'category': 'unknown',
            'auto_fixable': False,
            'severity': 'medium'
        }
        
        # Categorize error
        for category, patterns in self.error_patterns.items():
            if any(pattern in error_str or pattern in traceback_str for pattern in patterns):
                error_info['category'] = category
                error_info['auto_fixable'] = category in self.auto_fixes
                break
        
        # Determine severity
        if any(critical in error_str for critical in ['critical', 'fatal', 'crash']):
            error_info['severity'] = 'critical'
        elif any(high in error_str for high in ['connection', 'timeout', 'database']):
            error_info['severity'] = 'high'
        
        return error_info
    
    def log_error(self, error_info):
        """Log error with structured format"""
        self.logger.error(f"ERROR DETECTED: {error_info['category'].upper()}")
        self.logger.error(f"Function: {error_info['function']}")
        self.logger.error(f"Type: {error_info['error_type']}")
        self.logger.error(f"Message: {error_info['error_message']}")
        self.logger.error(f"Severity: {error_info['severity']}")
        self.logger.error(f"Auto-fixable: {error_info['auto_fixable']}")
        
        if self.debug_mode:
            self.logger.debug(f"Full traceback:\n{error_info['traceback']}")
    
    def fix_database_issues(self, error_info):
        """Automatic database issue resolution"""
        self.logger.info("Attempting database issue resolution")
        
        try:
            # Check database connection
            from app import db
            db.engine.execute('SELECT 1')
            self.logger.info("Database connection test passed")
            return True
        except Exception as db_error:
            self.logger.warning(f"Database connection failed: {db_error}")
            
            # Attempt to recreate tables
            try:
                from app import app
                with app.app_context():
                    db.create_all()
                    self.logger.info("Database tables recreated successfully")
                    return True
            except Exception as create_error:
                self.logger.error(f"Failed to recreate tables: {create_error}")
                return False
    
    def fix_api_issues(self, error_info):
        """Automatic API issue resolution"""
        self.logger.info("Attempting API issue resolution")
        
        # Check API endpoints
        try:
            # Test internal health endpoint
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                self.logger.info("Internal API health check passed")
                return True
        except Exception as api_error:
            self.logger.warning(f"API health check failed: {api_error}")
        
        # Check Workable API if configured
        workable_api_key = os.environ.get('WORKABLE_API_KEY')
        if workable_api_key:
            try:
                headers = {'Authorization': f'Bearer {workable_api_key}'}
                response = requests.get('https://growthaccelerator.workable.com/spi/v3/accounts', 
                                      headers=headers, timeout=10)
                if response.status_code in [200, 401]:  # 401 means API is responding
                    self.logger.info("Workable API connectivity confirmed")
                    return True
            except Exception as workable_error:
                self.logger.warning(f"Workable API check failed: {workable_error}")
        
        return False
    
    def fix_template_issues(self, error_info):
        """Automatic template issue resolution"""
        self.logger.info("Attempting template issue resolution")
        
        # Check if templates directory exists
        if not os.path.exists('templates'):
            os.makedirs('templates')
            self.logger.info("Created missing templates directory")
        
        # Check for missing template files
        required_templates = ['index.html', 'dashboard.html', 'jobs.html']
        for template in required_templates:
            template_path = os.path.join('templates', template)
            if not os.path.exists(template_path):
                self.create_fallback_template(template_path)
                self.logger.info(f"Created fallback template: {template}")
        
        return True
    
    def fix_import_issues(self, error_info):
        """Automatic import issue resolution"""
        self.logger.info("Attempting import issue resolution")
        
        # Extract missing module name
        error_msg = error_info['error_message']
        if 'no module named' in error_msg.lower():
            module_name = error_msg.split("'")[1] if "'" in error_msg else None
            
            if module_name:
                # Common module fixes
                module_fixes = {
                    'flask_login': 'Flask-Login',
                    'flask_sqlalchemy': 'Flask-SQLAlchemy',
                    'flask_wtf': 'Flask-WTF',
                    'werkzeug': 'Werkzeug',
                    'psycopg2': 'psycopg2-binary'
                }
                
                install_name = module_fixes.get(module_name, module_name)
                self.logger.info(f"Missing module detected: {module_name}")
                # Note: Actual installation would require package manager access
                return False
        
        return False
    
    def fix_permission_issues(self, error_info):
        """Automatic permission issue resolution"""
        self.logger.info("Attempting permission issue resolution")
        
        # Check file permissions
        critical_files = ['app.py', 'main.py', 'staffing_app.py']
        for file in critical_files:
            if os.path.exists(file):
                try:
                    # Ensure file is readable
                    with open(file, 'r') as f:
                        f.read(1)
                    self.logger.info(f"File permission check passed: {file}")
                except Exception as perm_error:
                    self.logger.warning(f"Permission issue with {file}: {perm_error}")
                    return False
        
        return True
    
    def fix_azure_issues(self, error_info):
        """Automatic Azure deployment issue resolution"""
        self.logger.info("Attempting Azure issue resolution")
        
        # Check Azure configuration files
        azure_files = ['web.config', 'requirements.txt']
        for file in azure_files:
            if not os.path.exists(file):
                self.create_azure_config_file(file)
                self.logger.info(f"Created missing Azure config: {file}")
        
        return True
    
    def create_fallback_template(self, template_path):
        """Create a basic fallback template"""
        template_name = os.path.basename(template_path).replace('.html', '')
        
        fallback_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Accelerator Platform - {template_name.title()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .error-notice {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="error-notice">
        <h1>Growth Accelerator Platform</h1>
        <p>Fallback template for {template_name}</p>
        <p>The system has automatically created this template to prevent errors.</p>
        <a href="/">Return to Home</a>
    </div>
</body>
</html>'''
        
        with open(template_path, 'w') as f:
            f.write(fallback_content)
    
    def create_azure_config_file(self, filename):
        """Create missing Azure configuration files"""
        if filename == 'web.config':
            config_content = '''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="python" arguments="app.py" startupTimeLimit="60">
      <environmentVariables>
        <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>'''
        elif filename == 'requirements.txt':
            config_content = '''Flask==2.3.3
Flask-Login==0.6.2
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.1.1
gunicorn==21.2.0
requests==2.31.0
Werkzeug==2.3.7
psycopg2-binary==2.9.7
'''
        
        with open(filename, 'w') as f:
            f.write(config_content)
    
    def health_check(self):
        """Comprehensive system health check"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'components': {}
        }
        
        # Check database
        try:
            from app import db
            db.engine.execute('SELECT 1')
            health_report['components']['database'] = 'healthy'
        except Exception as e:
            health_report['components']['database'] = f'error: {str(e)}'
            health_report['overall_status'] = 'degraded'
        
        # Check file system
        try:
            required_files = ['app.py', 'main.py', 'staffing_app.py']
            missing_files = [f for f in required_files if not os.path.exists(f)]
            if missing_files:
                health_report['components']['filesystem'] = f'missing: {missing_files}'
                health_report['overall_status'] = 'degraded'
            else:
                health_report['components']['filesystem'] = 'healthy'
        except Exception as e:
            health_report['components']['filesystem'] = f'error: {str(e)}'
        
        # Check memory usage
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            health_report['components']['memory'] = f'{memory_percent}% used'
            if memory_percent > 85:
                health_report['overall_status'] = 'warning'
        except ImportError:
            health_report['components']['memory'] = 'monitoring unavailable'
        
        self.logger.info(f"Health check completed: {health_report['overall_status']}")
        return health_report
    
    def get_error_summary(self):
        """Get summary of recent errors"""
        if not os.path.exists(self.error_log_file):
            return {'total_errors': 0, 'recent_errors': []}
        
        with open(self.error_log_file, 'r') as f:
            logs = f.readlines()
        
        error_lines = [line for line in logs if 'ERROR' in line]
        recent_errors = error_lines[-10:] if len(error_lines) > 10 else error_lines
        
        return {
            'total_errors': len(error_lines),
            'recent_errors': recent_errors,
            'categories': self.categorize_errors(error_lines)
        }
    
    def categorize_errors(self, error_lines):
        """Categorize errors by type"""
        categories = {}
        for line in error_lines:
            for category, patterns in self.error_patterns.items():
                if any(pattern in line.lower() for pattern in patterns):
                    categories[category] = categories.get(category, 0) + 1
                    break
        return categories

# Global error handler instance
error_handler = ErrorHandler()

# Decorator for easy use
def debug_errors(func):
    return error_handler.capture_error(func)