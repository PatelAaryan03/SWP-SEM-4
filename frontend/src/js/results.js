// Results Page JavaScript

const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:5000/api';

// Load results data
document.addEventListener('DOMContentLoaded', () => {
    // Try to load from sessionStorage
    const predictionData = sessionStorage.getItem('predictionData');
    const uploadStats = sessionStorage.getItem('uploadStats');
    
    if (predictionData && uploadStats) {
        const data = JSON.parse(predictionData);
        const stats = JSON.parse(uploadStats);
        displayResults(data, stats);
    } else {
        // Try to fetch from API if available
        // Or show message to upload data first
        displayNoData();
    }
});

function displayResults(data, stats) {
    const predictions = data.predictions || {};
    const likesData = predictions.likes || {};
    const growthData = predictions.follower_growth;
    const platformAnalysis = data.platform_analysis || {};
    
    // Update main predictions for LIKES (handle both old and new format)
    const avgLikes = likesData.average || predictions.average_likes || predictions.average || 0;
    const maxLikes = likesData.max || predictions.max_likes || predictions.max || 0;
    const minLikes = likesData.min || predictions.min_likes || predictions.min || 0;
    
    document.getElementById('avgLikes').textContent = Math.round(avgLikes);
    document.getElementById('maxLikes').textContent = Math.round(maxLikes);
    document.getElementById('minLikes').textContent = Math.round(minLikes);
    
    // Update FOLLOWER GROWTH if available
    if (growthData) {
        const growthSection = document.getElementById('followerGrowthSection');
        if (growthSection) {
            growthSection.style.display = 'block';
            document.getElementById('avgGrowth').textContent = Math.round(growthData.average || 0);
            document.getElementById('maxGrowth').textContent = Math.round(growthData.max || 0);
            document.getElementById('minGrowth').textContent = Math.round(growthData.min || 0);
        }
    }
    
    // Update best time
    const bestTimeElement = document.getElementById('bestTime');
    if (bestTimeElement) {
        const bestHour = predictions.best_posting_hour !== undefined 
            ? predictions.best_posting_hour 
            : (data.predictions?.best_posting_hour);
        bestTimeElement.textContent = bestHour !== null && bestHour !== undefined
            ? formatHour(bestHour) 
            : 'Not available';
    }
    
    // Update platform analysis
    updatePlatformAnalysis(platformAnalysis);
    
    // Update summary
    document.getElementById('totalPosts').textContent = data.total_posts_analyzed || stats.total_posts || 0;
}

function updatePlatformAnalysis(platformAnalysis) {
    // Instagram
    const instagram = platformAnalysis['Instagram'] || platformAnalysis['instagram'] || {};
    document.getElementById('instagramAvg').textContent = Math.round(instagram.avg_predicted_likes || 0);
    document.getElementById('instagramCount').textContent = instagram.post_count || 0;
    
    // Facebook
    const facebook = platformAnalysis['Facebook'] || platformAnalysis['facebook'] || {};
    document.getElementById('facebookAvg').textContent = Math.round(facebook.avg_predicted_likes || 0);
    document.getElementById('facebookCount').textContent = facebook.post_count || 0;
    
    // LinkedIn
    const linkedin = platformAnalysis['LinkedIn'] || platformAnalysis['linkedin'] || {};
    document.getElementById('linkedinAvg').textContent = Math.round(linkedin.avg_predicted_likes || 0);
    document.getElementById('linkedinCount').textContent = linkedin.post_count || 0;
}

function displayNoData() {
    // Could show a message or redirect to upload page
    console.log('No prediction data available');
}

function formatHour(hour) {
    if (hour === 0) return '12:00 AM';
    if (hour < 12) return `${hour}:00 AM`;
    if (hour === 12) return '12:00 PM';
    return `${hour - 12}:00 PM`;
}

