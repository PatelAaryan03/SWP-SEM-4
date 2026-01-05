// Dashboard Page JavaScript

const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:5000/api';

// Check authentication
if (typeof requireAuth === 'function') {
    requireAuth();
}

// Load dashboard data with caching
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Try cache first
        const cacheKey = 'dashboard_data';
        const cached = typeof getCachedResponse === 'function' 
            ? getCachedResponse(cacheKey) 
            : null;
        
        if (cached) {
            displayDashboardData(cached);
            // Still fetch fresh data in background
            fetchDashboardData(true);
        } else {
            await fetchDashboardData(false);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        displayEmptyState();
    }
});

async function fetchDashboardData(background = false) {
    try {
        const token = typeof getToken === 'function' ? getToken() : null;
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/dashboard`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // Cache the response
            if (typeof setCachedResponse === 'function') {
                setCachedResponse('dashboard_data', data);
            }
            
            if (!background) {
                displayDashboardData(data);
            } else {
                // Update UI in background
                displayDashboardData(data);
            }
        } else {
            if (!background) {
                displayEmptyState();
            }
        }
    } catch (error) {
        if (!background) {
            console.error('Error fetching dashboard:', error);
            displayEmptyState();
        }
    }
}

function displayDashboardData(data) {
    const stats = data.stats || {};
    const platformBreakdown = data.platform_breakdown || {};
    const recentPredictions = data.recent_predictions || [];
    
    // Update main stats
    document.getElementById('totalPredictions').textContent = stats.total_predictions || 0;
    document.getElementById('avgLikes').textContent = Math.round(stats.avg_likes || 0);
    document.getElementById('bestTime').textContent = stats.best_time !== null 
        ? formatHour(stats.best_time) 
        : '--:--';
    
    // Count platforms
    document.getElementById('platformsCount').textContent = stats.platforms_count || 0;
    
    // Update platform breakdown
    updatePlatformBreakdownFromData(platformBreakdown, recentPredictions);
    
    // Update predictions list
    updatePredictionsList(recentPredictions);
}

function updatePlatformBreakdownFromData(platformBreakdown, recentPredictions) {
    const breakdown = document.getElementById('platformBreakdown');
    if (!breakdown) return;
    
    const platforms = {
        'Instagram': { icon: '📷', avg: 0, count: 0 },
        'Facebook': { icon: '📘', avg: 0, count: 0 },
        'LinkedIn': { icon: '💼', avg: 0, count: 0 }
    };
    
    // Calculate averages from recent predictions
    recentPredictions.forEach(pred => {
        if (pred.platform_analysis) {
            Object.entries(pred.platform_analysis).forEach(([platform, data]) => {
                const key = platform.charAt(0).toUpperCase() + platform.slice(1);
                if (platforms[key]) {
                    platforms[key].avg = Math.round((platforms[key].avg + data.avg_predicted_likes) / 2);
                    platforms[key].count += data.post_count || 0;
                }
            });
        }
    });
    
    // Update DOM
    const platformItems = breakdown.querySelectorAll('.platform-item');
    platformItems.forEach((item) => {
        const platformName = item.querySelector('h3').textContent;
        const platformData = platforms[platformName];
        
        if (platformData) {
            const stats = item.querySelectorAll('.stat-number');
            if (stats.length >= 2) {
                stats[0].textContent = platformData.avg || 0;
                stats[1].textContent = platformData.count || 0;
            }
        }
    });
}

function updatePredictionsList(recentPredictions) {
    const list = document.getElementById('predictionsList');
    if (!list) return;
    
    if (recentPredictions.length === 0) {
        return; // Keep empty state
    }
    
    list.innerHTML = recentPredictions.map(pred => {
        const avgLikes = Math.round(pred.predictions?.average_likes || 0);
        const date = pred.created_at ? new Date(pred.created_at).toLocaleDateString() : 'Recently';
        return `
            <div class="prediction-item">
                <div class="prediction-info">
                    <h4>Prediction #${pred.id}</h4>
                    <p>${date} - ${pred.total_posts_analyzed} posts analyzed</p>
                </div>
                <div class="prediction-value">${avgLikes}</div>
            </div>
        `;
    }).join('');
}

function displayEmptyState() {
    // Already handled in HTML
}

function formatHour(hour) {
    if (hour === 0) return '12:00 AM';
    if (hour < 12) return `${hour}:00 AM`;
    if (hour === 12) return '12:00 PM';
    return `${hour - 12}:00 PM`;
}

