/**
 * Enhanced Match Suggestions JavaScript
 * Handles showing and hiding match suggestion popups with improved animations
 */

// Show match suggestion popup after page load with improved animations
function showMatchSuggestion(elementId, delay = 2000) {
    setTimeout(() => {
        const element = document.getElementById(elementId);
        if (element) {
            // First make it visible but with 0 opacity
            element.style.display = 'block';
            element.style.opacity = '0';
            
            // Force a reflow to ensure the transition applies
            void element.offsetWidth;
            
            // Apply the slide-in animation
            element.style.animation = 'slide-in-right 0.5s cubic-bezier(0.25, 1, 0.5, 1) forwards';
            
            // Add a subtle bounce effect at the end
            setTimeout(() => {
                element.classList.add('pulse-once');
                setTimeout(() => element.classList.remove('pulse-once'), 600);
            }, 500);
            
            // Play a subtle notification sound if available
            playNotificationSound();
        }
    }, delay);
}

// Play a subtle notification sound (if available)
function playNotificationSound() {
    try {
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.volume = 0.3; // Keep it subtle
        audio.play().catch(e => {
            // Browser might block autoplay, that's fine
            console.log('Notification sound not played:', e);
        });
    } catch (e) {
        // Sound not available or not supported, that's fine
    }
}

// Close match suggestion popup with smooth exit animation
function closeMatchSuggestion(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        // Apply the exit animation
        element.style.animation = 'slide-out-right 0.4s cubic-bezier(0.5, 0, 0.75, 0) forwards';
        
        // Remove element after animation completes
        setTimeout(() => {
            element.style.display = 'none';
            element.style.animation = ''; // Reset animation
        }, 400);
    }
}

// Dismiss all match suggestions sequentially with staggered animation
function dismissAllMatchSuggestions() {
    const suggestions = document.querySelectorAll('.match-suggestion-popup');
    
    suggestions.forEach((suggestion, index) => {
        // Stagger the closing animations
        setTimeout(() => {
            closeMatchSuggestion(suggestion.id);
        }, index * 150);
    });
}

// Store dismissed suggestions in session storage
function storeDismissedSuggestion(id) {
    const dismissed = JSON.parse(sessionStorage.getItem('dismissedSuggestions') || '[]');
    if (!dismissed.includes(id)) {
        dismissed.push(id);
        sessionStorage.setItem('dismissedSuggestions', JSON.stringify(dismissed));
        
        // Also store the timestamp of dismissal
        const dismissalTimes = JSON.parse(sessionStorage.getItem('dismissalTimes') || '{}');
        dismissalTimes[id] = Date.now();
        sessionStorage.setItem('dismissalTimes', JSON.stringify(dismissalTimes));
    }
}

// Check if suggestion was already dismissed within the last 4 hours
function wasSuggestionDismissed(id) {
    const dismissed = JSON.parse(sessionStorage.getItem('dismissedSuggestions') || '[]');
    if (!dismissed.includes(id)) {
        return false;
    }
    
    // Check if it was dismissed more than 4 hours ago
    const dismissalTimes = JSON.parse(sessionStorage.getItem('dismissalTimes') || '{}');
    const dismissedTime = dismissalTimes[id] || 0;
    const fourHoursAgo = Date.now() - (4 * 60 * 60 * 1000);
    
    // If dismissed more than 4 hours ago, consider it not dismissed
    if (dismissedTime < fourHoursAgo) {
        return false;
    }
    
    return true;
}

// Handle ESC key to close all popups
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        dismissAllMatchSuggestions();
    }
});

// Initialize match suggestions when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Show match suggestions for items that haven't been dismissed yet
    const suggestions = document.querySelectorAll('.match-suggestion-popup');
    
    if (suggestions.length > 0) {
        // Count how many suggestions will be shown
        const visibleSuggestions = Array.from(suggestions).filter(
            suggestion => !wasSuggestionDismissed(suggestion.id)
        );
        
        // If there are multiple suggestions, spread them out more
        const baseDelay = 2000;
        const spreadFactor = visibleSuggestions.length > 1 ? 800 : 500;
        
        // Show suggestions one by one with a delay between them
        visibleSuggestions.forEach((suggestion, index) => {
            showMatchSuggestion(suggestion.id, baseDelay + (index * spreadFactor));
        });
        
        // If we have more than 2 suggestions, add a "dismiss all" button to the page
        if (visibleSuggestions.length > 2) {
            setTimeout(() => {
                addDismissAllButton();
            }, baseDelay);
        }
    }
});

// Add a floating "dismiss all" button for multiple popups
function addDismissAllButton() {
    // Create the button if it doesn't exist
    if (!document.getElementById('dismissAllSuggestions')) {
        const button = document.createElement('button');
        button.id = 'dismissAllSuggestions';
        button.className = 'btn btn-sm btn-primary dismiss-all-btn';
        button.innerHTML = '<i class="bi bi-x-circle me-1"></i> Dismiss All';
        button.onclick = dismissAllMatchSuggestions;
        
        document.body.appendChild(button);
        
        // Animate the button in
        setTimeout(() => {
            button.style.opacity = '1';
        }, 100);
    }
}