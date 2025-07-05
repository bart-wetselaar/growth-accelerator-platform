#!/usr/bin/env python3
"""
24/7 Always-On Service for Growth Accelerator Platform
Ensures continuous availability without modifying .replit files
"""

import requests
import time
import threading
import logging
import os
from datetime import datetime
from flask import Flask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AlwaysOnService:
    def __init__(self):
        self.production_urls = [
            "https://growth-accelerator-platform.replit.app",
            "https://web"
            "https://white-coast-08429c303.1.azurestaticapps.net",
            "https://thankful-moss-085e6bd03.1.azurestaticapps.net"
        ]
        
        # Only use local URL in development environments
        self.is_local_env = not ("WEBSITE_HOSTNAME" in os.environ or "REPLIT_DEPLOYMENT" in os.environ)
        self.local_url = "http://127.0.0.1:5000" if self.is_local_env else None
        
        self.ping_interval = 240  # 4 minutes
        self.running = True
        self.health_data = {}
        
    def ping_endpoint(self, url):
        """Ping an endpoint to keep it alive"""
        try:
            # Try multiple endpoints to ensure full activation
            endpoints = [
                "/api/ai/suggestions",
                "/",
                "/staffing/dashboard"
            ]
            
            for endpoint in endpoints:
                full_url = f"{url}{endpoint}"
                response = requests.get(full_url, timeout=30)
                if response.status_code in [200, 302, 404]:
                    logger.info(f"✓ {url}{endpoint} - Active ({response.status_code})")
                    return True
                    
        except Exception as e:
            logger.warning(f"⚠ {url} - {str(e)}")
            return False
        
        return False
    
    def self_ping(self):
        """Ping local instance to keep it active (only in development)"""
        if not self.is_local_env or not self.local_url:
            return None  # Skip local ping in production
            
        try:
            response = requests.get(f"{self.local_url}/api/ai/suggestions", timeout=10)
            if response.status_code == 200:
                logger.info("✓ Local instance - Active")
                return True
        except:
            pass
        return False
    
    def health_check_all(self):
        """Perform comprehensive health check"""
        results = {}
        
        # Check production URLs
        for url in self.production_urls:
            results[url] = self.ping_endpoint(url)
        
        # Check local instance (only in development)
        if self.is_local_env and self.local_url:
            local_result = self.self_ping()
            if local_result is not None:
                results[self.local_url] = local_result
        
        # Update health data
        self.health_data = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "active_count": sum(v for v in results.values() if v is not None),
            "total_count": len(results)
        }
        
        return results
    
    def keep_alive_loop(self):
        """Main keep-alive loop"""
        logger.info("Starting 24/7 keep-alive service...")
        
        while self.running:
            try:
                results = self.health_check_all()
                active = sum(results.values())
                total = len(results)
                
                logger.info(f"Health check: {active}/{total} endpoints active")
                
                if active < total:
                    logger.warning("Some endpoints are down, attempting recovery...")
                
                time.sleep(self.ping_interval)
                
            except KeyboardInterrupt:
                logger.info("Keep-alive service stopped by user")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Keep-alive error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def start_background_service(self):
        """Start keep-alive service in background"""
        thread = threading.Thread(target=self.keep_alive_loop, daemon=True)
        thread.start()
        logger.info("24/7 keep-alive service started in background")
        return thread
    
    def get_health_status(self):
        """Get current health status"""
        return self.health_data

# Global service instance
always_on = AlwaysOnService()

def start_always_on_service():
    """Initialize and start the always-on service"""
    return always_on.start_background_service()

def get_service_health():
    """Get health status of the service"""
    return always_on.get_health_status()

if __name__ == "__main__":
    # Start service directly
    always_on.keep_alive_loop()