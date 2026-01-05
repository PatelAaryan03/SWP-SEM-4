// Login Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Social login buttons (placeholder)
    document.querySelectorAll('.social-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Social login coming soon!');
        });
    });
});

function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Placeholder login logic
    // In a real application, this would make an API call
    if (email && password) {
        // Simulate login
        alert('Login functionality coming soon! For now, you can use the app without logging in.');
        // Could redirect to dashboard
        // window.location.href = 'dashboard.html';
    } else {
        alert('Please fill in all fields');
    }
}

