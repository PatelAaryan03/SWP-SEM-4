# Machine Learning Module

This folder contains all machine learning-related code for training and evaluating models to predict social media post performance.

## 📁 Folder Structure

```
ml/
├── data/                    # Sample datasets
│   └── sample_social_media_data.csv
├── models/                  # Trained model files (.pkl)
├── notebooks/               # Jupyter notebooks for exploration
├── trainings/               # Training scripts
│   ├── train_model.py      # Main training script
│   └── feature_engineering.py  # Feature engineering utilities
└── README.md               # This file
```

## 🎯 Purpose

The ML module is responsible for:
1. **Feature Engineering**: Creating meaningful features from raw social media data
2. **Model Training**: Training Linear Regression and Random Forest models
3. **Prediction**: Generating predictions for likes and follower growth
4. **Model Evaluation**: Calculating performance metrics (MAE, RMSE, R²)

## 📊 Models Implemented

### 1. Linear Regression
- **Use Case**: Baseline model, fast training
- **Advantages**: Interpretable, fast, good for linear relationships
- **Best For**: Quick predictions, understanding feature importance

### 2. Random Forest Regressor
- **Use Case**: Advanced model, better accuracy
- **Advantages**: Handles non-linear relationships, feature interactions
- **Best For**: Production predictions, complex patterns

## 🔧 Features Engineered

### Time Features
- `posting_hour`: Hour of day (0-23)
- `posting_day`: Day of week (0=Monday, 6=Sunday)
- `month`: Month of year (1-12)
- `is_weekend`: Binary indicator (0/1)

### Platform & Content
- `platform_encoded`: Numeric encoding (Instagram=0, Facebook=1, LinkedIn=2)
- `content_type_encoded`: Numeric encoding (Image=0, Video=1, Carousel=2, Text=3)

### Engagement Features
- `engagement_rate`: (likes + comments + shares) / followers
- `rolling_avg_likes`: 7-day rolling average of likes
- `rolling_avg_engagement`: 7-day rolling average of engagement rate

### Growth Features
- `follower_growth`: Change in followers between posts

### Interaction Features
- `platform_content_interaction`: Platform × Content Type
- `hour_platform_interaction`: Hour × Platform

## 📈 Prediction Targets

1. **Likes**: Expected number of likes for a post
2. **Follower Growth**: Expected change in followers after posting

## 🚀 Usage

### Training Models

```python
from trainings.train_model import train_models
from trainings.feature_engineering import engineer_features
import pandas as pd

# Load data
df = pd.read_csv('data/sample_social_media_data.csv')

# Engineer features
df_engineered = engineer_features(df)

# Train models
models, metrics = train_models(df_engineered, model_type='both')

# Save models
import joblib
joblib.dump(models['likes_random_forest'], 'models/likes_rf.pkl')
joblib.dump(models['follower_growth_random_forest'], 'models/growth_rf.pkl')
```

### Making Predictions

```python
import joblib
import pandas as pd
from trainings.feature_engineering import engineer_features

# Load model
model = joblib.load('models/likes_rf.pkl')

# Prepare new data
new_data = pd.DataFrame({
    'platform': ['Instagram'],
    'post_date': ['2024-03-01'],
    'post_time': ['14:00:00'],
    'content_type': ['image'],
    'caption_length': [150],
    'hashtags_count': [5],
    'followers_at_post_time': [5000]
})

# Engineer features
new_data = engineer_features(new_data)

# Predict
prediction = model.predict(new_data[feature_cols])
```

## 📝 Model Evaluation Metrics

- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors more
- **R² Score**: Proportion of variance explained (0-1, higher is better)

## 🔄 Model Workflow

1. **Data Loading**: Load CSV with historical posts
2. **Feature Engineering**: Create engineered features
3. **Data Splitting**: Train/Test split (80/20)
4. **Model Training**: Train Linear Regression and Random Forest
5. **Evaluation**: Calculate metrics on test set
6. **Model Saving**: Save best model as .pkl file
7. **Prediction**: Use saved model for new predictions

## 📚 Dependencies

- pandas
- numpy
- scikit-learn
- joblib

## 🎓 Educational Notes

- **Why Linear Regression?**: Simple baseline, easy to understand
- **Why Random Forest?**: Better accuracy, handles complex patterns
- **Feature Engineering**: Critical for model performance
- **Rolling Averages**: Capture trends over time
- **Engagement Rate**: Normalizes engagement by follower count

## 🔍 Model Selection

The system uses **Random Forest** as the default model because:
- Better accuracy on non-linear data
- Handles feature interactions automatically
- More robust to outliers
- Good performance on small-medium datasets

Linear Regression is kept as a baseline for comparison.

---

**Note**: Models are automatically trained when first prediction is made, or can be pre-trained using the training scripts.

