"""
Authentication utilities
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models.database import User, db

# JWT Configuration
SECRET_KEY = 'your-secret-key-change-in-production'  # Change this in production!
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_HOURS = 24

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current user from token"""
    token = request.headers.get('Authorization')
    if not token:
        return None
    
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]
    
    user_id = verify_token(token)
    if user_id:
        return User.query.get(user_id)
    return None

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        return f(*args, **kwargs)
    return decorated_function

