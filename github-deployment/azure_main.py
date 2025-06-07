#!/usr/bin/env python3
import os
import sys

# Ensure proper module loading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app
try:
    from app import app
    print("Flask app imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback import
    import main
    app = main.app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
