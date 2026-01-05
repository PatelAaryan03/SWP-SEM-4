# Backend Module

Flask-based REST API server handling file uploads, data preprocessing, ML predictions, and user authentication.

## 📁 Folder Structure

```
backend/
├── app.py                 # Main Flask application
├── models/                # Database models
│   ├── database.py        # SQLAlchemy models (User, Upload, Prediction)
│   └── __init__.py
├── routes/                # API route handlers (future expansion)
│   └── __init__.py
├── uploads/               # Uploaded CSV files storage
├── utils/                 # Utility functions
│   ├── auth.py            # JWT authentication utilities
│   └── __init__.py
└── README.md              # This file
```

## 🎯 Purpose

The backend provides:
1. **REST API Endpoints** for frontend communication
2. **File Upload & Validation** for CSV data
3. **Data Preprocessing** using feature engineering
4. **ML Model Integration** for predictions
5. **User Authentication** with JWT tokens
6. **Database Management** for users, uploads, and predictions

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/me` - Get current user info

### Upload & Predictions
- `POST /api/upload` - Upload CSV file (Protected)
- `POST /api/predict` - Get predictions (Protected)
- `GET /api/dashboard` - Dashboard data (Protected)
- `GET /api/predictions` - All predictions (Protected)
- `GET /api/predictions/<id>` - Specific prediction (Protected)

### Public
- `GET /api/sample-csv` - Download sample CSV file

## 🏗️ Architecture

### Service-Based Structure

```
app.py (Main Application)
├── Authentication Routes
├── Upload Routes
├── Prediction Routes
├── Dashboard Routes
└── Public Routes

models/database.py
├── User Model
├── Upload Model
└── Prediction Model

utils/auth.py
├── JWT Token Generation
├── Token Verification
└── Protected Route Decorators
```

## 📊 Data Flow

1. **Upload CSV** → Validate → Save to disk → Store metadata in DB
2. **Preprocess Data** → Feature engineering → Prepare for ML
3. **Train/Load Model** → Check for existing model → Train if needed
4. **Make Predictions** → Predict likes & follower growth → Save to DB
5. **Return Results** → JSON response with predictions

## 🔐 Security Features

- **JWT Authentication**: Token-based auth with 24-hour expiration
- **Password Hashing**: Werkzeug secure password hashing
- **Protected Routes**: `@login_required` decorator
- **Input Validation**: CSV format and column validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique, indexed
- `password_hash`: Hashed password
- `name`: User's name
- `created_at`, `updated_at`: Timestamps

### Uploads Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `filename`: Stored filename
- `original_filename`: Original filename
- `file_path`: Full file path
- `total_posts`: Number of posts in file
- `columns`: JSON array of column names
- `created_at`: Timestamp

### Predictions Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `upload_id`: Foreign key to uploads (optional)
- `average_likes`: Predicted average likes
- `max_likes`: Maximum predicted likes
- `min_likes`: Minimum predicted likes
- `best_posting_hour`: Optimal posting hour
- `platform_analysis`: JSON object with platform breakdown
- `total_posts_analyzed`: Number of posts analyzed
- `created_at`: Timestamp

## 🚀 Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
cd backend
python app.py

# Server runs on http://localhost:5000
```

## 📝 Configuration

### Environment Variables (Optional)
- `SECRET_KEY`: JWT secret key (default: development key)
- `DATABASE_URL`: Database connection string
- `UPLOAD_FOLDER`: Path to upload directory
- `MAX_FILE_SIZE`: Maximum upload size (default: 16MB)

### File Paths
- **Uploads**: `backend/uploads/`
- **Models**: `ml/models/`
- **Database**: `database/postpredict.db`

## 🔄 Error Handling

All endpoints include comprehensive error handling:
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (authentication required)
- **404**: Not Found (file/resource not found)
- **500**: Internal Server Error (server errors)

## 📚 Dependencies

- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-CORS: Cross-origin resource sharing
- Pandas: Data processing
- NumPy: Numerical operations
- Scikit-learn: Machine learning
- Joblib: Model serialization
- PyJWT: JWT token handling
- Werkzeug: Password hashing

## 🎓 Code Quality

- **Clean Architecture**: Separation of concerns
- **Error Handling**: Comprehensive try-catch blocks
- **Input Validation**: All inputs validated
- **Type Hints**: Where applicable
- **Comments**: Clear documentation
- **No Hard-coded Paths**: All paths use configuration

## 🔍 Key Functions

### `preprocess_data(df)`
Preprocesses uploaded CSV data for ML prediction:
- Date/time parsing
- Platform encoding
- Content type encoding
- Feature calculation

### `train_model_safe(df, model_path)`
Safely trains ML model with error handling:
- Checks for existing model
- Trains if needed
- Saves model to disk
- Error recovery

### `@login_required`
Decorator for protected routes:
- Validates JWT token
- Returns 401 if unauthorized
- Provides user context

## 🚨 Important Notes

1. **Database**: SQLite database auto-creates on first run
2. **Models**: ML models are trained on first prediction
3. **Uploads**: Files are stored with timestamp prefixes
4. **Tokens**: JWT tokens expire after 24 hours
5. **CORS**: Enabled for frontend communication

---

**Status**: Production-ready backend with authentication, database, and ML integration.

