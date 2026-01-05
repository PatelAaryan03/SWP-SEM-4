// Authentication utilities

const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:5000/api';

// Token management
function getToken() {
    return localStorage.getItem('authToken');
}

function setToken(token) {
    localStorage.setItem('authToken', token);
}

function removeToken() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function isAuthenticated() {
    return !!getToken();
}

// API request with auth
async function apiRequest(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Token expired or invalid
        removeToken();
        if (window.location.pathname !== '/login.html' && !window.location.pathname.includes('login.html')) {
            window.location.href = 'login.html';
        }
        throw new Error('Authentication required');
    }
    
    return response;
}

// Login with optimized error handling
async function login(email, password) {
    try {
        // Use AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout
        
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }
        
        if (!data.token) {
            throw new Error('No token received from server');
        }
        
        setToken(data.token);
        setUser(data.user);
        
        return data;
    } catch (error) {
        // Handle timeout
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please check your connection.');
        }
        // Handle network errors
        if (error.message.includes('fetch') || error.message.includes('Failed')) {
            throw new Error('Cannot connect to server. Make sure the backend is running on http://localhost:5000');
        }
        throw error;
    }
}

// Register with timeout handling
async function register(email, password, name = '') {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, name }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }
        
        setToken(data.token);
        setUser(data.user);
        
        return data;
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please try again.');
        }
        throw error;
    }
}

// Logout
function logout() {
    removeToken();
    window.location.href = 'index.html';
}

// Check auth and redirect if needed
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Update navigation based on auth status
function updateNavigation() {
    const user = getUser();
    const navLinks = document.querySelector('.nav-links');
    
    if (!navLinks) return;
    
    // Find login button
    const loginBtn = Array.from(navLinks.querySelectorAll('a, li')).find(
        el => el.textContent.trim() === 'Login' || el.classList.contains('login-btn')
    );
    
    if (user) {
        // User is logged in
        if (loginBtn) {
            loginBtn.textContent = `Logout (${user.email})`;
            loginBtn.href = '#';
            loginBtn.onclick = (e) => {
                e.preventDefault();
                logout();
            };
        }
    } else {
        // User is not logged in
        if (loginBtn) {
            loginBtn.textContent = 'Login';
            loginBtn.href = 'login.html';
            loginBtn.onclick = null;
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
});

