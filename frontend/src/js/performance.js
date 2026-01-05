/**
 * Performance monitoring and optimization utilities
 */

// Monitor page load performance
function trackPerformance() {
    if ('performance' in window && 'PerformanceObserver' in window) {
        // Track Largest Contentful Paint (LCP)
        const lcpObserver = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
        });
        
        try {
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {
            // Browser doesn't support LCP
        }
        
        // Track First Input Delay (FID)
        const fidObserver = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach(entry => {
                console.log('FID:', entry.processingStart - entry.startTime);
            });
        });
        
        try {
            fidObserver.observe({ entryTypes: ['first-input'] });
        } catch (e) {
            // Browser doesn't support FID
        }
    }
}

// Optimize images
function optimizeImages() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        // Add loading="lazy" for below-the-fold images
        if (!img.hasAttribute('loading')) {
            img.loading = 'lazy';
        }
        
        // Add decoding="async"
        if (!img.hasAttribute('decoding')) {
            img.decoding = 'async';
        }
    });
}

// Prefetch next likely pages
function prefetchPages() {
    const links = document.querySelectorAll('a[href]');
    const prefetchLinks = Array.from(links)
        .filter(link => {
            const href = link.getAttribute('href');
            return href && !href.startsWith('#') && !href.startsWith('http');
        })
        .slice(0, 3); // Only prefetch first 3 links
    
    prefetchLinks.forEach(link => {
        const href = link.getAttribute('href');
        const prefetchLink = document.createElement('link');
        prefetchLink.rel = 'prefetch';
        prefetchLink.href = href;
        document.head.appendChild(prefetchLink);
    });
}

// Initialize performance optimizations
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        trackPerformance();
        optimizeImages();
        // Delay prefetch to not interfere with critical resources
        setTimeout(prefetchPages, 2000);
    });
} else {
    trackPerformance();
    optimizeImages();
    setTimeout(prefetchPages, 2000);
}

// Clean up old sessionStorage data
function cleanupStorage() {
    try {
        const keys = Object.keys(sessionStorage);
        const now = Date.now();
        
        keys.forEach(key => {
            if (key.startsWith('cache_')) {
            const data = sessionStorage.getItem(key);
            try {
                const parsed = JSON.parse(data);
                if (parsed.expiry && parsed.expiry < now) {
                    sessionStorage.removeItem(key);
                }
            } catch (e) {
                // Invalid data, remove it
                sessionStorage.removeItem(key);
            }
        }
        });
    } catch (e) {
        console.warn('Storage cleanup failed:', e);
    }
}

// Run cleanup every 5 minutes
setInterval(cleanupStorage, 5 * 60 * 1000);

