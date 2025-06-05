/**
 * Configuration for Azure Static Web App
 * Connects to production Replit backend APIs
 */

const CONFIG = {
    // Production Replit backend API base URLs
    API_BASE_URL: 'https://staff-match-pro-bart83.replit.app',
    BACKUP_API_URL: 'https://webapp.growthaccelerator.nl',
    
    // API endpoints
    ENDPOINTS: {
        JOBS: '/api/jobs',
        CANDIDATES: '/api/candidates', 
        CLIENTS: '/clients',
        APPLICATIONS: '/applications',
        PLACEMENTS: '/placements',
        UNIFIED_API: '/unified_api',
        AI_SUGGESTIONS: '/api/ai/suggestions',
        SYNC_STATUS: '/sync_status',
        WORKABLE_TEST: '/test_workable'
    },
    
    // App configuration
    APP: {
        NAME: 'Growth Accelerator',
        VERSION: '1.0.0',
        ENVIRONMENT: 'production',
        THEME: 'dark'
    },
    
    // UI Settings
    UI: {
        ITEMS_PER_PAGE: 10,
        TOAST_DURATION: 5000,
        LOADING_TIMEOUT: 30000
    }
};

// Export for use in other scripts
window.CONFIG = CONFIG;