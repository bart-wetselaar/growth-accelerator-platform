# Growth Accelerator Platform - Azure Static Web App

A sophisticated AI-powered Staffing and Deployment Acceleration Platform with Azure Static Web App frontend and Replit backend integration.

## 🚀 Live Deployment

- **Frontend**: Azure Static Web Apps (Global CDN)
- **Backend**: Replit (Live APIs)
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

The static frontend connects to live Replit backend APIs:

- **Base URL**: `https://eb44c92f-21f3-4aed-9cb2-28ca14f82460-00-296c0ebbkj4nd.riker.replit.dev`
- **Endpoints**: Jobs, Candidates, Clients, Applications, AI Suggestions
- **Authentication**: Session-based with CORS support
- **Error Handling**: Automatic retry with exponential backoff

## 🛠 Features

- **Real-time Data**: Connects to live PostgreSQL database
- **Responsive Design**: Bootstrap 5 dark theme
- **Client-side Routing**: Hash-based navigation
- **Connection Monitoring**: Auto-retry failed requests
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

All data operations are handled by the live Replit backend:
- Job listings and management
- Candidate profiles and applications
- Client information and relationships
- AI-powered matching algorithms
- Real-time synchronization status

## 🌐 Deployment

Automatic deployment via GitHub Actions to Azure Static Web Apps.
Push to `main` branch to trigger deployment.