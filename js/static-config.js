/**
 * Multi-platform configuration for Growth Accelerator Platform
 * Supports Azure Static Web Apps, GitHub Pages, and direct hosting
 */

const CONFIG = {
    // Production backend URLs with automatic failover
    API_BASE_URL: 'https://staff-match-pro-bart83.replit.app',
    BACKUP_API_URL: 'https://webapp.growthaccelerator.nl',
    
    // Deployment platform detection
    PLATFORM: {
        AZURE: 'azurestaticapps.net',
        GITHUB: 'github.io',
        REPLIT: 'replit.app',
        CUSTOM: 'growthaccelerator.nl'
    },
    
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
    
    // Platform-specific settings
    DEPLOYMENT: {
        azure: 'https://black-stone-0c2b8303.6.azurestaticapps.net',
        github: 'https://bart-wetselaar.github.io/growth-accelerator-platform',
        replit: 'https://staff-match-pro-bart83.replit.app',
        custom: 'https://webapp.growthaccelerator.nl'
    },
    
    // UI Settings
    UI: {
        ITEMS_PER_PAGE: 10,
        TOAST_DURATION: 5000,
        LOADING_TIMEOUT: 30000
    }
};

// Auto-detect current platform
CONFIG.CURRENT_PLATFORM = (function() {
    const hostname = window.location.hostname;
    if (hostname.includes('azurestaticapps.net')) return 'azure';
    if (hostname.includes('github.io')) return 'github';
    if (hostname.includes('replit.app')) return 'replit';
    if (hostname.includes('growthaccelerator.nl')) return 'custom';
    return 'local';
})();

// Export for use in other scripts
window.CONFIG = CONFIG;