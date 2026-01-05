/**
 * Optimized script loader with lazy loading and error handling
 */

// Script loading queue
const scriptQueue = [];
let loading = false;

// Load script dynamically
function loadScript(src, defer = true) {
    return new Promise((resolve, reject) => {
        // Check if already loaded
        if (document.querySelector(`script[src="${src}"]`)) {
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.src = src;
        script.defer = defer;
        script.async = !defer;
        
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`Failed to load script: ${src}`));
        
        document.head.appendChild(script);
    });
}

// Load CSS dynamically
function loadCSS(href) {
    return new Promise((resolve, reject) => {
        // Check if already loaded
        if (document.querySelector(`link[href="${href}"]`)) {
            resolve();
            return;
        }

        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        
        link.onload = () => resolve();
        link.onerror = () => reject(new Error(`Failed to load CSS: ${href}`));
        
        document.head.appendChild(link);
    });
}

// Load scripts in order
async function loadScripts(scripts) {
    for (const src of scripts) {
        try {
            await loadScript(src);
        } catch (error) {
            console.error('Script loading error:', error);
        }
    }
}

// Preload critical resources
function preloadResources() {
    const criticalCSS = [
        '../src/css/base.css'
    ];
    
    criticalCSS.forEach(href => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'style';
        link.href = href;
        link.onload = function() {
            this.rel = 'stylesheet';
        };
        document.head.appendChild(link);
    });
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', preloadResources);
} else {
    preloadResources();
}

