# Growth Accelerator Platform - Azure Static Web App

A sophisticated AI-powered Staffing and Deployment Acceleration Platform with Azure Static Web App frontend and Replit backend integration.

## 🚀 Live Production Deployment

- **Frontend**: Azure Static Web Apps (Global CDN) - https://black-stone-0c2b8303.6.azurestaticapps.net
- **Backend Primary**: https://staff-match-pro-bart83.replit.app
- **Backend Secondary**: https://webapp.growthaccelerator.nl
- **Database**: PostgreSQL on Replit

## 📁 Project Structure

```
├── index.html              # Main application entry point
├── css/                    # Stylesheets (preserves exact design)
│   ├── main.css
│   ├── style.css
│   ├── workflow.css
│   └── ...
├── js/                     # JavaScript modules
│   ├── static-config.js    # Configuration and API endpoints
│   ├── static-api.js       # API client with retry logic
│   ├── static-router.js    # Client-side routing
│   └── static-app.js       # Main application controller
├── img/                    # Images and assets
└── staticwebapp.config.json # Azure routing configuration
```

## 🔗 API Integration

The static frontend connects to production Replit backend APIs:

- **Primary URL**: https://staff-match-pro-bart83.replit.app
- **Secondary URL**: https://webapp.growthaccelerator.nl
- **Endpoints**: Jobs, Candidates, Clients, Applications, AI Suggestions
- **Authentication**: Session-based with CORS support
- **Error Handling**: Automatic retry with failover between URLs

## 🛠 Features

- **Real-time Data**: Connects to live PostgreSQL database
- **Responsive Design**: Bootstrap 5 dark theme
- **Client-side Routing**: Hash-based navigation
- **Connection Monitoring**: Auto-retry failed requests with URL failover
- **Toast Notifications**: User feedback system
- **Global CDN**: Azure edge locations worldwide

## 📋 Platform Capabilities

- Job Management & Posting
- Candidate Sourcing & Matching
- Client Relationship Management
- AI-Powered Suggestions
- Real-time Sync Status
- Workable API Integration
- LinkedIn API Integration

## 🔧 Development

This is a production-ready static web application that maintains the exact design and functionality of the original Growth Accelerator platform while providing enhanced performance through Azure's global CDN.

## 📞 Backend APIs

All data operations are handled by the production Replit backend:
- Job listings and management
- Candidate profiles and applications
- Client information and relationships
- AI-powered matching algorithms
- Real-time synchronization status

## 🌐 Deployment

Automatic deployment via GitHub Actions to Azure Static Web Apps.
Push to `main` branch to trigger deployment.

## Production URLs

- Azure Static Web App: https://black-stone-0c2b8303.6.azurestaticapps.net
- Replit Production Primary: https://staff-match-pro-bart83.replit.app
- Replit Production Secondary: https://webapp.growthaccelerator.nl
