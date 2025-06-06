"""
Growth Accelerator Platform - Main Entry Point
Clean deployment configuration without duplicate model imports
"""

import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
