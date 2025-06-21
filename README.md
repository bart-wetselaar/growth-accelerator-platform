# Growth Accelerator Platform

A comprehensive staffing and recruitment management system with AI-powered consultant matching, advanced self-debugging capabilities, and seamless multi-platform deployment.

## Features

- **Staffing Management**: Complete recruitment workflow management
- **Self-Debugging System**: Automated error detection and recovery
- **Multi-Platform Sync**: Unified Replit → GitHub → Azure deployment pipeline
- **Real-time Monitoring**: Comprehensive health checking and diagnostics
- **Workable Integration**: Professional ATS integration for job and candidate management

## Architecture

### Self-Debugging Components
- `error_handler.py` - Automated error capture and categorization
- `self_diagnostic.py` - Comprehensive system health diagnostics
- `auto_recovery.py` - 24/7 monitoring with automated fixes
- `azure_error_handler.py` - Cloud-specific error handling

### Deployment Pipeline
- **Replit**: Development and testing environment
- **GitHub**: Version control with automated workflows
- **Azure**: Production deployment with self-healing capabilities

## Quick Start

### Local Development
```bash
git clone https://github.com/your-username/growth-accelerator-platform.git
cd growth-accelerator-platform
pip install flask flask-login flask-sqlalchemy flask-wtf gunicorn requests sqlalchemy werkzeug
python main.py
```

### Azure Deployment
The platform automatically deploys to Azure via GitHub Actions when changes are pushed to the main branch.

## Monitoring Endpoints

- `/health` - Basic health check
- `/diagnostics` - Comprehensive system diagnostics
- `/admin/error-dashboard` - Real-time error monitoring
- `/admin/sync-dashboard` - Platform synchronization status
- `/azure-status` - Azure environment information

## Environment Variables

```
DATABASE_URL=postgresql://your-database-url
SESSION_SECRET=your-secure-session-key
FLASK_ENV=production
WORKABLE_API_KEY=your-workable-key (optional)
WORKABLE_SUBDOMAIN=your-subdomain (optional)
```

## Self-Debugging Features

The platform includes comprehensive error handling that automatically:
- Detects and categorizes errors
- Applies automated fixes for common issues
- Provides detailed diagnostic information
- Maintains 24/7 monitoring with recovery capabilities
- Syncs diagnostic data across all deployment platforms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper error handling
4. Run diagnostics: `python -m self_diagnostic`
5. Submit a pull request

The GitHub Actions workflow will automatically run diagnostics and deploy to Azure upon merge.

## License

MIT License - see LICENSE file for details