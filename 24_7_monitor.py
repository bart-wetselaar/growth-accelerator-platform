#!/usr/bin/env python3
"""
24/7 Platform Monitoring System
Ensures Growth Accelerator Platform stays online across all platforms
"""

import requests
import time
import logging
import threading
from datetime import datetime
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('24_7_Monitor')

class PlatformMonitor:
    def __init__(self):
        self.platforms = {
            'replit_main': 'https://eb44c92f-21f3-4aed-9cb2-28ca14f82460-00-296c0ebbkj4nd.riker.replit.dev',
            'azure_webapp': 'https://ga-hwaffmb0eqajfza5.azurewebsites.net',
            'github_repo': 'https://api.github.com/repos/bart-wetselaar/growth-accelerator-platform'
        }
        self.check_interval = 120  # 2 minutes
        self.timeout = 30
        self.running = True
        self.status_log = []
        
    def check_platform_health(self, name, url):
        """Check if platform is responsive"""
        try:
            if 'github.com' in url:
                response = requests.get(url, timeout=self.timeout)
            else:
                response = requests.get(url + '/health', timeout=self.timeout)
            
            if response.status_code == 200:
                logger.info(f"✓ {name} is online")
                return True
            else:
                logger.warning(f"⚠ {name} returned status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ {name} is unreachable: {str(e)}")
            return False
    
    def wake_up_platform(self, name, url):
        """Attempt to wake up a sleeping platform"""
        try:
            # Try multiple endpoints to wake up the platform
            endpoints = ['/', '/health', '/dashboard']
            
            for endpoint in endpoints:
                if 'github.com' not in url:
                    wake_url = url + endpoint
                    requests.get(wake_url, timeout=10)
                    time.sleep(2)
                    
            logger.info(f"Attempted to wake up {name}")
            
        except Exception as e:
            logger.error(f"Failed to wake up {name}: {str(e)}")
    
    def monitor_all_platforms(self):
        """Continuously monitor all platforms"""
        while self.running:
            timestamp = datetime.now().isoformat()
            status_report = {'timestamp': timestamp, 'platforms': {}}
            
            for name, url in self.platforms.items():
                is_healthy = self.check_platform_health(name, url)
                status_report['platforms'][name] = {
                    'url': url,
                    'status': 'online' if is_healthy else 'offline',
                    'checked_at': timestamp
                }
                
                # If platform is down, try to wake it up
                if not is_healthy and 'github.com' not in url:
                    self.wake_up_platform(name, url)
                    time.sleep(10)  # Wait before rechecking
                    is_healthy = self.check_platform_health(name, url)
                    if is_healthy:
                        logger.info(f"Successfully revived {name}")
            
            # Log status
            self.status_log.append(status_report)
            
            # Keep only last 100 status reports
            if len(self.status_log) > 100:
                self.status_log = self.status_log[-100:]
            
            time.sleep(self.check_interval)
    
    def get_status_summary(self):
        """Get current status summary"""
        if not self.status_log:
            return {'status': 'monitoring_starting'}
            
        latest = self.status_log[-1]
        online_count = sum(1 for p in latest['platforms'].values() if p['status'] == 'online')
        total_count = len(latest['platforms'])
        
        return {
            'overall_status': 'healthy' if online_count == total_count else 'degraded',
            'online_platforms': online_count,
            'total_platforms': total_count,
            'last_check': latest['timestamp'],
            'platforms': latest['platforms']
        }
    
    def start_monitoring(self):
        """Start 24/7 monitoring in background"""
        monitor_thread = threading.Thread(target=self.monitor_all_platforms, daemon=True)
        monitor_thread.start()
        logger.info("24/7 platform monitoring started")
        return monitor_thread

# Global monitor instance
platform_monitor = PlatformMonitor()

def start_24_7_monitoring():
    """Initialize and start 24/7 monitoring"""
    return platform_monitor.start_monitoring()

def get_monitoring_status():
    """Get current monitoring status"""
    return platform_monitor.get_status_summary()

if __name__ == "__main__":
    # Start monitoring if run directly
    monitor = PlatformMonitor()
    try:
        monitor.monitor_all_platforms()
    except KeyboardInterrupt:
        logger.info("Monitoring stopped")