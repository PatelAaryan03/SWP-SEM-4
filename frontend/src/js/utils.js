/**
 * Utility functions for performance optimization
 */

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Cache API responses
const apiCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

function getCachedResponse(key) {
    const cached = apiCache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.data;
    }
    apiCache.delete(key);
    return null;
}

function setCachedResponse(key, data) {
    apiCache.set(key, {
        data,
        timestamp: Date.now()
    });
}

// Clear old cache entries
function clearExpiredCache() {
    const now = Date.now();
    for (const [key, value] of apiCache.entries()) {
        if (now - value.timestamp > CACHE_DURATION) {
            apiCache.delete(key);
        }
    }
}

// Run cache cleanup every 10 minutes
setInterval(clearExpiredCache, 10 * 60 * 1000);

// Optimized fetch with caching
async function cachedFetch(url, options = {}) {
    const cacheKey = `${url}_${JSON.stringify(options)}`;
    const cached = getCachedResponse(cacheKey);
    
    if (cached && !options.forceRefresh) {
        return cached;
    }
    
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        
        if (response.ok) {
            setCachedResponse(cacheKey, data);
        }
        
        return data;
    } catch (error) {
        // Return cached data if available even on error
        if (cached) {
            return cached;
        }
        throw error;
    }
}

// Performance monitoring
function measurePerformance() {
    if ('performance' in window && 'PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.entryType === 'navigation') {
                    console.log('Page Load Time:', entry.loadEventEnd - entry.fetchStart, 'ms');
                }
            }
        });
        observer.observe({ entryTypes: ['navigation'] });
    }
}

// Initialize performance monitoring
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', measurePerformance);
} else {
    measurePerformance();
}

// Export utilities
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        debounce,
        throttle,
        lazyLoadImages,
        cachedFetch,
        getCachedResponse,
        setCachedResponse
    };
}

