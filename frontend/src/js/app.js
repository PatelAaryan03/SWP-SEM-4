// Main application JavaScript (Legacy - Minimal compatibility layer)
// Note: Most functionality moved to page-specific files (upload.js, dashboard.js, etc.)

const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:5000/api';

// DOM Elements
const fileInput = document.querySelector('input[type="file"]');
const uploadBox = document.querySelector('.upload-box');
const resultBox = document.querySelector('.result-box');

let uploadedFilename = null;

// File upload handler
if (fileInput) {
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.csv')) {
            alert('Please upload a CSV file');
            return;
        }

        await uploadFile(file);
    });
}

// Upload file to backend
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading('Uploading file...');

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        uploadedFilename = data.filename;
        showSuccess('File uploaded successfully! Analyzing data...');

        // Automatically trigger prediction
        setTimeout(() => {
            predictPerformance(data.filename);
        }, 1000);

    } catch (error) {
        showError(`Upload failed: ${error.message}`);
    }
}

// Predict performance
async function predictPerformance(filename) {
    try {
        showLoading('Analyzing patterns and making predictions...');

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: filename })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }

        displayResults(data);

    } catch (error) {
        showError(`Prediction failed: ${error.message}`);
    }
}

// Display prediction results
function displayResults(data) {
    const predictions = data.predictions;
    const platformAnalysis = data.platform_analysis;

    let html = `
        <div class="prediction-results">
            <h3>📊 Prediction Results</h3>
            
            <div class="prediction-stats">
                <div class="stat-card">
                    <div class="stat-label">Average Predicted Likes</div>
                    <div class="stat-value">${Math.round(predictions.average_likes)}</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Maximum Predicted Likes</div>
                    <div class="stat-value">${Math.round(predictions.max_likes)}</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-label">Minimum Predicted Likes</div>
                    <div class="stat-value">${Math.round(predictions.min_likes)}</div>
                </div>
            </div>
    `;

    if (predictions.best_posting_hour !== null) {
        html += `
            <div class="best-time">
                <strong>⏰ Best Posting Time:</strong> ${predictions.best_posting_hour}:00 (${formatHour(predictions.best_posting_hour)})
            </div>
        `;
    }

    if (Object.keys(platformAnalysis).length > 0) {
        html += `
            <div class="platform-analysis">
                <h4>📱 Platform Analysis</h4>
                <div class="platform-cards">
        `;
        
        for (const [platform, stats] of Object.entries(platformAnalysis)) {
            html += `
                <div class="platform-card">
                    <div class="platform-name">${platform}</div>
                    <div class="platform-avg">Avg: ${Math.round(stats.avg_predicted_likes)} likes</div>
                    <div class="platform-count">${stats.post_count} posts</div>
                </div>
            `;
        }
        
        html += `
                </div>
            </div>
        `;
    }

    html += `
            <div class="total-posts">
                <p>Total posts analyzed: <strong>${data.total_posts_analyzed}</strong></p>
            </div>
        </div>
    `;

    resultBox.innerHTML = html;
    resultBox.style.border = '1px solid #4a9eff';
    resultBox.style.background = '#1a1a1a';
}

// Helper functions
function showLoading(message) {
    resultBox.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
    resultBox.style.border = '1px dashed #555';
}

function showSuccess(message) {
    resultBox.innerHTML = `
        <div class="success">
            ✅ ${message}
        </div>
    `;
    resultBox.style.border = '1px solid #4a9eff';
}

function showError(message) {
    resultBox.innerHTML = `
        <div class="error">
            ❌ ${message}
        </div>
    `;
    resultBox.style.border = '1px solid #ff4444';
    resultBox.style.background = '#2a1a1a';
}

function formatHour(hour) {
    if (hour === 0) return '12:00 AM';
    if (hour < 12) return `${hour}:00 AM`;
    if (hour === 12) return '12:00 PM';
    return `${hour - 12}:00 PM`;
}

// Download sample CSV
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links li');
    
    navLinks.forEach(link => {
        if (link.textContent.trim() === 'Sample CSV') {
            link.style.cursor = 'pointer';
            link.addEventListener('click', async () => {
                try {
                    const response = await fetch(`${API_BASE_URL}/sample-csv`);
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'sample_data.csv';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } catch (error) {
                    alert('Failed to download sample CSV');
                }
            });
        }
    });
});

