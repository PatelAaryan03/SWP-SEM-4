// Shared Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    MAX_FILE_SIZE: 16 * 1024 * 1024, // 16MB
    SUPPORTED_FILE_TYPES: ['.csv']
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

