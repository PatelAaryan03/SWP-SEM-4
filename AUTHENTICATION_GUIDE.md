# Authentication & Database Guide

## ✅ Completed Features

### 1. **Database Setup**
- SQLite database with SQLAlchemy ORM
- Three main models:
  - **User**: Authentication and user management
  - **Upload**: Tracks file uploads per user
  - **Prediction**: Stores prediction results

### 2. **Authentication System**
- JWT-based authentication
- User registration with email/password
- User login with token generation
- Protected routes with `@login_required` decorator
- Token stored in localStorage
- Automatic token validation

### 3. **API Endpoints**

#### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/me` - Get current user info

#### Protected Routes (Require Authentication)
- `POST /api/upload` - Upload CSV file
- `POST /api/predict` - Get predictions
- `GET /api/dashboard` - Get dashboard data
- `GET /api/predictions` - Get all predictions
- `GET /api/predictions/<id>` - Get specific prediction

#### Public Routes
- `GET /api/sample-csv` - Download sample CSV

### 4. **Frontend Integration**
- `auth.js` - Authentication utilities
- Login page with working authentication
- Register page for new users
- Automatic token injection in API requests
- Protected page redirects
- Navigation updates based on auth status

## 🚀 Usage

### Register a New User
1. Go to `/register.html`
2. Fill in name, email, and password
3. Click "Create Account"
4. Automatically logged in and redirected to dashboard

### Login
1. Go to `/login.html`
2. Enter email and password
3. Click "Sign In"
4. Redirected to dashboard

### Using Protected Features
- All upload and prediction features require authentication
- Token is automatically included in API requests
- If token expires, user is redirected to login

## 🔐 Security Features

- Passwords are hashed using Werkzeug's password hashing
- JWT tokens with 24-hour expiration
- Protected routes check authentication
- User-specific data isolation
- SQL injection protection via ORM

## 📊 Database Schema

### Users Table
- id (Primary Key)
- email (Unique, Indexed)
- password_hash
- name
- created_at
- updated_at

### Uploads Table
- id (Primary Key)
- user_id (Foreign Key)
- filename
- original_filename
- file_path
- total_posts
- columns (JSON)
- created_at

### Predictions Table
- id (Primary Key)
- user_id (Foreign Key)
- upload_id (Foreign Key, Optional)
- average_likes
- max_likes
- min_likes
- best_posting_hour
- platform_analysis (JSON)
- total_posts_analyzed
- created_at

## 🎯 Default Admin Account

On first run, an admin account is created:
- **Email**: admin@postpredict.com
- **Password**: admin123

**⚠️ Change this in production!**

## 📝 Notes

- Database file: `database/postpredict.db`
- Tokens stored in browser localStorage
- All user data is isolated by user_id
- Predictions are linked to uploads and users

---

**Status**: ✅ Authentication and Database Fully Implemented

