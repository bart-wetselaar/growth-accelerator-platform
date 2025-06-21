#!/usr/bin/env python3
"""
Replit Always-On Service
Ensures Replit deployment stays active 24/7
"""

import requests
import time
import threading
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ReplitKeepAlive')

class ReplitKeepAlive:
    def __init__(self):
        # Use the current Replit URL
        self.replit_url = "https://eb44c92f-21f3-4aed-9cb2-28ca14f82460-00-296c0ebbkj4nd.riker.replit.dev"
        self.ping_interval = 300  # 5 minutes
        self.running = True
        self.self_ping = True  # Enable self-pinging for development
        
    def ping_replit_app(self):
        """Ping Replit app to keep it active"""
        try:
            # Use health endpoint if available, otherwise use root
            endpoints = ['/health', '/api/platform-status', '/']
            
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.replit_url}{endpoint}", timeout=30)
                    if response.status_code == 200:
                        logger.info(f"✓ Replit app pinged successfully via {endpoint} at {datetime.now()}")
                        return True
                except:
                    continue
                    
            logger.warning("All Replit ping endpoints failed")
            return False
            
        except Exception as e:
            logger.error(f"Failed to ping Replit app: {str(e)}")
            return False
    
    def self_ping_local(self):
        """Ping local instance to prevent sleeping"""
        if not self.self_ping:
            return
            
        try:
            # Ping localhost to keep the local instance active
            response = requests.get("http://localhost:5000/health", timeout=10)
            if response.status_code == 200:
                logger.info("✓ Local instance self-ping successful")
                return True
        except:
            pass
            
        return False
    
    def keep_alive_loop(self):
        """Main keep-alive loop for Replit"""
        while self.running:
            # Ping external Replit URL
            self.ping_replit_app()
            
            # Self-ping local instance
            self.self_ping_local()
            
            time.sleep(self.ping_interval)
    
    def start_service(self):
        """Start Replit keep-alive service"""
        thread = threading.Thread(target=self.keep_alive_loop, daemon=True)
        thread.start()
        logger.info("Replit keep-alive service started")
        return thread

# Global instance
replit_keeper = ReplitKeepAlive()

def start_replit_keep_alive():
    """Start Replit keep-alive service"""
    return replit_keeper.start_service()

if __name__ == "__main__":
    keeper = ReplitKeepAlive()
    try:
        keeper.keep_alive_loop()
    except KeyboardInterrupt:
        logger.info("Replit keep-alive service stopped")