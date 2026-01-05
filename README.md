# Social Media Performance Predictor

A complete, production-ready machine learning-based web application that predicts the performance of future social media posts (likes and follower growth) on Instagram, Facebook, and LinkedIn using historical posting data.

## 📌 Problem Statement

Content creators and businesses often struggle to understand when, what, and how to post to achieve maximum engagement on social media platforms. Posting without data-driven insights can lead to inconsistent growth and low engagement.

**This project addresses**: "Based on my past social media performance, how will my next post perform?"

## ✨ Core Features

1. ✅ **Upload CSV** file containing past social media data
2. ✅ **Preprocess and validate** the data automatically
3. ✅ **Train ML models** (Linear Regression + Random Forest)
4. ✅ **Predict**:
   - Expected Likes
   - Expected Follower Growth
5. ✅ **Dashboard** with clean analytics and insights
6. ✅ **User Authentication** with secure JWT tokens
7. ✅ **Database Storage** for predictions and history
8. ✅ **Platform-specific** analysis (Instagram, Facebook, LinkedIn)

## 🛠️ Tech Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with dark theme
- **JavaScript (ES6+)**: Interactive functionality

### Backend
- **Python 3.8+**: Core language
- **Flask**: REST API framework
- **SQLAlchemy**: Database ORM
- **JWT**: Authentication tokens

### Machine Learning
- **Pandas**: Data processing
- **NumPy**: Numerical operations
- **Scikit-learn**: ML models
  - Linear Regression (baseline)
  - Random Forest (advanced)
- **Joblib**: Model serialization

## 📊 Dataset Format (CSV)

Your CSV file should include these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `platform` | Instagram / Facebook / LinkedIn | Instagram |
| `post_date` | Date of post | 2024-01-01 |
| `post_time` | Time of post | 10:00:00 |
| `content_type` | image / video / carousel / text | image |
| `caption_length` | Length of caption | 125 |
| `hashtags_count` | Number of hashtags | 5 |
| `likes` | Number of likes | 245 |
| `comments` | Number of comments | 18 |
| `shares` | Number of shares | 12 |
| `followers_at_post_time` | Follower count | 3500 |

**Sample CSV**: Available at `ml/data/sample_social_media_data.csv`

## 🏗️ Project Structure

```
SWP-SEM-4/
├── frontend/              # Frontend application
│   ├── public/            # HTML pages
│   ├── src/               # CSS and JavaScript
│   └── README.md          # Frontend documentation
├── backend/               # Backend API server
│   ├── app.py             # Main Flask application
│   ├── models/            # Database models
│   ├── utils/             # Utility functions
│   └── README.md          # Backend documentation
├── ml/                    # Machine Learning module
│   ├── data/              # Sample datasets
│   ├── models/            # Trained models (.pkl)
│   ├── trainings/         # Training scripts
│   └── README.md          # ML documentation
├── docs/                  # Project documentation
│   ├── project_report.md  # Complete project report
│   └── README.md          # Documentation index
├── database/              # SQLite database
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**:
   ```bash
   cd backend
   python app.py
   ```
   Backend runs on `http://localhost:5000`

4. **Start the frontend server** (in a new terminal):
   ```bash
   cd frontend/public
   python -m http.server 8000
   ```
   Frontend runs on `http://localhost:8000`

5. **Open your browser**:
   Visit `http://localhost:8000`

### Quick Start Script
```bash
./run.sh
```

## 📖 Usage Guide

### 1. Register/Login
- Click "Register" to create an account
- Or use default admin: `admin@postpredict.com` / `admin123`

### 2. Upload Data
- Go to Upload page
- Drag & drop or select CSV file
- File is validated automatically

### 3. Get Predictions
- After upload, predictions are generated automatically
- View results on Results page
- Check Dashboard for analytics

### 4. View Analytics
- Dashboard shows:
  - Total predictions
  - Average predicted likes
  - Best posting time
  - Platform breakdown

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/me` - Get current user

### Upload & Predictions
- `POST /api/upload` - Upload CSV (Protected)
- `POST /api/predict` - Get predictions (Protected)
- `GET /api/dashboard` - Dashboard data (Protected)
- `GET /api/predictions` - All predictions (Protected)

### Public
- `GET /api/sample-csv` - Download sample CSV

## 🎯 Feature Engineering

The system automatically creates these features:

### Time Features
- `posting_hour`: Hour of day (0-23)
- `posting_day`: Day of week (0=Monday)
- `month`: Month of year
- `is_weekend`: Binary indicator

### Engagement Features
- `engagement_rate`: (likes + comments + shares) / followers
- `rolling_avg_likes`: 7-day rolling average
- `rolling_avg_engagement`: 7-day engagement average

### Growth Features
- `follower_growth`: Change in followers

### Encoded Features
- `platform_encoded`: Instagram=0, Facebook=1, LinkedIn=2
- `content_type_encoded`: Image=0, Video=1, Carousel=2, Text=3

## 📈 Machine Learning Models

### Linear Regression
- **Use**: Baseline model
- **Advantages**: Fast, interpretable
- **Best For**: Quick predictions

### Random Forest
- **Use**: Production model (default)
- **Advantages**: Better accuracy, handles non-linear patterns
- **Best For**: Final predictions

## 🔐 Security

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Werkzeug secure hashing
- **Protected Routes**: Authentication required
- **Input Validation**: All inputs validated
- **SQL Injection Protection**: ORM-based queries

## 📝 Documentation

- **Frontend**: See `frontend/README.md`
- **Backend**: See `backend/README.md`
- **ML Module**: See `ml/README.md`
- **Project Report**: See `docs/project_report.md`

## 🎓 Educational Value

This project demonstrates:
- Full-stack web development
- Machine learning implementation
- REST API design
- Database design
- Authentication systems
- Feature engineering
- Model evaluation

## 🚨 Important Notes

1. **Database**: Auto-creates on first run
2. **Models**: Auto-train on first prediction
3. **Default Admin**: `admin@postpredict.com` / `admin123`
4. **File Size**: Maximum 16MB per upload
5. **Token Expiry**: 24 hours

## 🤝 Contributing

This is a college group project. For questions or improvements:
1. Check documentation in each module
2. Review code comments
3. Test thoroughly before changes

## 📄 License

This project is built for educational purposes as a college mini project.

## 🎉 Project Status

✅ **Complete and Production-Ready**

All features implemented:
- ✅ User authentication
- ✅ File upload & validation
- ✅ Advanced feature engineering
- ✅ ML model training (Linear + Random Forest)
- ✅ Likes prediction
- ✅ Follower growth prediction
- ✅ Dashboard analytics
- ✅ Database storage
- ✅ Responsive UI
- ✅ Complete documentation

---

**Built with ❤️ for College Group Project**

For detailed setup instructions, see [SETUP.md](SETUP.md)
