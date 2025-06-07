"""
Azure Health Check Module
"""

import os
import time
from flask import jsonify
from sqlalchemy import text

def register_azure_health_routes(app):
    """Register health check routes for Azure App Service - disabled to prevent conflicts"""
    # Health check endpoint is now handled in main application
    pass