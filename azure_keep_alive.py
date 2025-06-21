#!/usr/bin/env python3
"""
Azure Web App Keep-Alive Service
Prevents Azure Web App from going to sleep
"""

import requests
import time
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AzureKeepAlive')

class AzureKeepAlive:
    def __init__(self):
        self.azure_url = "https://ga-hwaffmb0eqajfza5.azurewebsites.net"
        self.ping_interval = 240  # 4 minutes (Azure sleeps after 5 minutes of inactivity)
        self.running = True
        
    def ping_azure_app(self):
        """Ping Azure Web App to keep it awake"""
        try:
            response = requests.get(f"{self.azure_url}/health", timeout=30)
            if response.status_code == 200:
                logger.info(f"✓ Azure Web App pinged successfully at {datetime.now()}")
                return True
            else:
                logger.warning(f"Azure Web App responded with {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to ping Azure Web App: {str(e)}")
            return False
    
    def keep_alive_loop(self):
        """Main keep-alive loop for Azure"""
        while self.running:
            self.ping_azure_app()
            time.sleep(self.ping_interval)
    
    def start_service(self):
        """Start Azure keep-alive service"""
        thread = threading.Thread(target=self.keep_alive_loop, daemon=True)
        thread.start()
        logger.info("Azure Web App keep-alive service started")
        return thread

# Global instance
azure_keeper = AzureKeepAlive()

def start_azure_keep_alive():
    """Start Azure keep-alive service"""
    return azure_keeper.start_service()

if __name__ == "__main__":
    keeper = AzureKeepAlive()
    try:
        keeper.keep_alive_loop()
    except KeyboardInterrupt:
        logger.info("Azure keep-alive service stopped")