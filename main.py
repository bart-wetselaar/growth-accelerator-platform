"""
Main entry point for Growth Accelerator Staffing Platform on Azure
"""

# Import the complete staffing application
from staffing_app import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)