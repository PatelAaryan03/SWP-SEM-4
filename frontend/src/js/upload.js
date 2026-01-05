// Upload Page JavaScript - Optimized

// Load config and auth
const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:5000/api';
const MAX_FILE_SIZE = typeof CONFIG !== 'undefined' ? CONFIG.MAX_FILE_SIZE : 16 * 1024 * 1024;

// Load throttle utility
const throttle = typeof throttle !== 'undefined' ? throttle : function(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

// Check authentication
if (typeof requireAuth === 'function') {
    requireAuth();
}

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const uploadBtn = document.getElementById('uploadBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultPreview = document.getElementById('resultPreview');
const previewStats = document.getElementById('previewStats');
const downloadSample = document.getElementById('downloadSample');

let selectedFile = null;

// Optimized drag and drop handlers with throttling
const throttledDragOver = throttle((e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}, 100);

uploadArea.addEventListener('dragover', throttledDragOver);

uploadArea.addEventListener('dragleave', (e) => {
    // Only remove if leaving the upload area
    if (!uploadArea.contains(e.relatedTarget)) {
        uploadArea.classList.remove('dragover');
    }
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Click on upload area
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Remove file
removeFile.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
});

// Upload button
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    await uploadFile(selectedFile);
});

// Download sample CSV
if (downloadSample) {
    downloadSample.addEventListener('click', async (e) => {
        e.preventDefault();
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

// Handle file selection
function handleFileSelect(file) {
    if (!file.name.endsWith('.csv')) {
        alert('Please select a CSV file');
        return;
    }
    
    if (file.size > MAX_FILE_SIZE) {
        alert(`File size must be less than ${(MAX_FILE_SIZE / (1024 * 1024)).toFixed(0)}MB`);
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Upload file with optimized error handling
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Show progress
        if (progressSection) {
            progressSection.style.display = 'block';
            updateProgress(30, 'Uploading file...');
        }
        
        // Get auth token
        const token = typeof getToken === 'function' ? getToken() : null;
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Use AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60s timeout
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            headers: headers,
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        if (progressSection) updateProgress(60, 'Processing data...');
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        if (progressSection) updateProgress(80, 'Analyzing patterns...');
        
        // Get predictions with optimized headers
        const predictHeaders = {
            'Content-Type': 'application/json'
        };
        if (token) {
            predictHeaders['Authorization'] = `Bearer ${token}`;
        }
        
        // Use AbortController for timeout
        const predictController = new AbortController();
        const predictTimeoutId = setTimeout(() => predictController.abort(), 60000);
        
        const predictResponse = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: predictHeaders,
            body: JSON.stringify({ 
                filename: data.filename,
                upload_id: data.upload_id 
            }),
            signal: predictController.signal
        });
        
        clearTimeout(predictTimeoutId);
        if (progressSection) updateProgress(100, 'Complete!');
        
        const predictData = await predictResponse.json();
        
        if (!predictResponse.ok) {
            throw new Error(predictData.error || 'Prediction failed');
        }
        
        // Store data in sessionStorage (with error handling)
        try {
            sessionStorage.setItem('predictionData', JSON.stringify(predictData));
            sessionStorage.setItem('uploadStats', JSON.stringify(data.stats));
        } catch (e) {
            console.warn('SessionStorage full, using memory cache');
        }
        
        // Show preview
        displayPreview(predictData, data.stats);
        
        if (progressSection) {
            setTimeout(() => {
                progressSection.style.display = 'none';
            }, 1000);
        }
        
    } catch (error) {
        if (progressSection) progressSection.style.display = 'none';
        
        if (error.name === 'AbortError') {
            showError('Request timeout. Please try again.');
        } else {
            showError(`Error: ${error.message}`);
        }
    }
}

// Helper function for progress updates
function updateProgress(percent, text) {
    if (progressFill) progressFill.style.width = `${percent}%`;
    if (progressText) progressText.textContent = text;
}

// Improved error display
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = 'background: #ff4444; color: white; padding: 15px; border-radius: 8px; margin: 20px 0;';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
        setTimeout(() => errorDiv.remove(), 5000);
    } else {
        alert(message);
    }
}

// Display preview with optimized rendering
function displayPreview(predictData, stats) {
    if (!previewStats || !resultPreview) return;
    
    const predictions = predictData.predictions || {};
    const likesData = predictions.likes || {};
    const avgLikes = likesData.average || predictions.average_likes || predictions.average || 0;
    const bestHour = predictions.best_posting_hour;
    
    // Use DocumentFragment for better performance
    const fragment = document.createDocumentFragment();
    const container = document.createElement('div');
    
    container.innerHTML = `
        <div class="preview-stat">
            <div class="preview-stat-label">Total Posts</div>
            <div class="preview-stat-value">${stats.total_posts || 0}</div>
        </div>
        <div class="preview-stat">
            <div class="preview-stat-label">Avg Predicted Likes</div>
            <div class="preview-stat-value">${Math.round(avgLikes)}</div>
        </div>
        <div class="preview-stat">
            <div class="preview-stat-label">Best Time</div>
            <div class="preview-stat-value">${bestHour !== null && bestHour !== undefined ? bestHour + ':00' : 'N/A'}</div>
        </div>
    `;
    
    fragment.appendChild(container);
    previewStats.innerHTML = '';
    previewStats.appendChild(fragment);
    resultPreview.style.display = 'block';
}

