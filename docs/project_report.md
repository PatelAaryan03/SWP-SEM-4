# Social Media Performance Predictor
## Project Report

### 1. Problem Statement

Content creators and businesses struggle to understand when, what, and how to post on social media platforms to achieve maximum engagement. Without data-driven insights, posting strategies are often based on guesswork, leading to inconsistent growth and low engagement rates.

**Research Question**: "Based on my past social media performance, how will my next post perform?"

### 2. Objectives

1. Analyze historical social media post data
2. Identify patterns affecting engagement and growth
3. Predict future post performance using machine learning
4. Help users improve posting strategy and timing
5. Provide insights for data-driven decision making

### 3. Methodology

#### 3.1 Data Collection
- Historical post data including:
  - Posting time and date
  - Content type (image, video, carousel, text)
  - Caption length and hashtag count
  - Engagement metrics (likes, comments, shares)
  - Follower count at time of posting

#### 3.2 Feature Engineering
- **Time Features**: posting_hour, posting_day, month, is_weekend
- **Platform Encoding**: Numeric encoding (Instagram=0, Facebook=1, LinkedIn=2)
- **Content Encoding**: Numeric encoding (Image=0, Video=1, Carousel=2, Text=3)
- **Engagement Rate**: (likes + comments + shares) / followers
- **Rolling Averages**: 7-day rolling average of likes and engagement
- **Follower Growth**: Change in followers between posts

#### 3.3 Machine Learning Models

**Linear Regression**:
- Baseline model for comparison
- Fast training and prediction
- Interpretable coefficients

**Random Forest Regressor**:
- Advanced model with better accuracy
- Handles non-linear relationships
- Feature interaction handling

#### 3.4 Evaluation Metrics
- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors
- **R² Score**: Proportion of variance explained

### 4. Implementation

#### 4.1 System Architecture
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask REST API
- **ML**: Scikit-learn models
- **Database**: SQLite with SQLAlchemy ORM

#### 4.2 Key Features
1. User authentication with JWT tokens
2. CSV file upload and validation
3. Advanced feature engineering
4. ML model training and prediction
5. Dashboard with analytics
6. Platform-specific insights

### 5. Results

The system successfully:
- Predicts expected likes with good accuracy
- Predicts follower growth trends
- Identifies optimal posting times
- Provides platform-specific recommendations
- Stores prediction history for users

### 6. Conclusion

The Social Media Performance Predictor successfully addresses the problem of unpredictable social media engagement by leveraging machine learning to analyze historical data and predict future performance. The system provides actionable insights to help users optimize their posting strategy.

### 7. Future Enhancements

1. Real-time social media API integration
2. Advanced deep learning models
3. Sentiment analysis of captions
4. Automated post scheduling recommendations
5. Multi-user collaboration features

---

**Project Status**: ✅ Complete and Production-Ready

