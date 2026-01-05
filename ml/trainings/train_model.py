"""
Enhanced Machine Learning Model Training
Trains both Linear Regression and Random Forest models
Predicts: Likes and Follower Growth
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def prepare_features(df):
    """
    Prepare features for model training
    Includes all engineered features
    """
    features = []
    
    # Time features
    if 'posting_hour' in df.columns:
        features.append('posting_hour')
    elif 'hour' in df.columns:
        features.append('hour')
    
    if 'posting_day' in df.columns:
        features.append('posting_day')
    elif 'day_of_week' in df.columns:
        features.append('day_of_week')
    
    if 'month' in df.columns:
        features.append('month')
    
    # Platform (encoded)
    if 'platform_encoded' in df.columns:
        features.append('platform_encoded')
    
    # Content type (encoded)
    if 'content_type_encoded' in df.columns:
        features.append('content_type_encoded')
    
    # Caption and hashtags
    if 'caption_length' in df.columns:
        features.append('caption_length')
    
    if 'hashtags_count' in df.columns:
        features.append('hashtags_count')
    elif 'hashtag_count' in df.columns:
        features.append('hashtag_count')
    
    # Engagement features
    if 'engagement_rate' in df.columns:
        features.append('engagement_rate')
    
    if 'rolling_avg_likes' in df.columns:
        features.append('rolling_avg_likes')
    
    # Followers at post time
    if 'followers_at_post_time' in df.columns:
        features.append('followers_at_post_time')
    elif 'followers' in df.columns:
        features.append('followers')
    
    return features

def train_models(df, model_type='both'):
    """
    Train machine learning models to predict likes and follower growth
    
    Args:
        df: Preprocessed DataFrame with features
        model_type: 'linear', 'random_forest', or 'both'
        
    Returns:
        Dictionary with trained models for likes and follower_growth
    """
    # Prepare features
    feature_cols = prepare_features(df)
    
    if len(feature_cols) == 0:
        raise ValueError("No valid features found in data")
    
    # Check required columns
    if 'likes' not in df.columns:
        raise ValueError("Target column 'likes' not found in data")
    
    # Prepare X
    X = df[feature_cols].fillna(0)
    X = X.replace([np.inf, -np.inf], 0)
    
    # Prepare y for likes
    y_likes = df['likes'].fillna(0).replace([np.inf, -np.inf], 0)
    
    # Prepare y for follower growth (if available)
    y_follower_growth = None
    if 'follower_growth' in df.columns:
        y_follower_growth = df['follower_growth'].fillna(0).replace([np.inf, -np.inf], 0)
    elif 'followers_at_post_time' in df.columns and len(df) > 1:
        # Calculate follower growth as difference
        df_sorted = df.sort_values('post_date' if 'post_date' in df.columns else df.index)
        y_follower_growth = df_sorted['followers_at_post_time'].diff().fillna(0)
    
    # Split data
    if len(X) > 5:
        X_train, X_test, y_likes_train, y_likes_test = train_test_split(
            X, y_likes, test_size=0.2, random_state=42
        )
        
        if y_follower_growth is not None:
            _, _, y_growth_train, y_growth_test = train_test_split(
                X, y_follower_growth, test_size=0.2, random_state=42
            )
        else:
            y_growth_train, y_growth_test = None, None
    else:
        X_train, X_test = X, X
        y_likes_train, y_likes_test = y_likes, y_likes
        y_growth_train, y_growth_test = y_follower_growth, y_follower_growth if y_follower_growth is not None else (None, None)
    
    models = {}
    metrics = {}
    
    # Train models for LIKES prediction
    if model_type in ['linear', 'both']:
        print("\n=== Training Linear Regression for LIKES ===")
        lr_likes = LinearRegression()
        lr_likes.fit(X_train, y_likes_train)
        models['likes_linear'] = lr_likes
        
        if len(X_test) > 0:
            y_pred = lr_likes.predict(X_test)
            metrics['likes_linear'] = {
                'mae': mean_absolute_error(y_likes_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_likes_test, y_pred)),
                'r2': r2_score(y_likes_test, y_pred)
            }
            print(f"  MAE: {metrics['likes_linear']['mae']:.2f}")
            print(f"  RMSE: {metrics['likes_linear']['rmse']:.2f}")
            print(f"  R² Score: {metrics['likes_linear']['r2']:.4f}")
    
    if model_type in ['random_forest', 'both']:
        print("\n=== Training Random Forest for LIKES ===")
        rf_likes = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        rf_likes.fit(X_train, y_likes_train)
        models['likes_random_forest'] = rf_likes
        
        if len(X_test) > 0:
            y_pred = rf_likes.predict(X_test)
            metrics['likes_random_forest'] = {
                'mae': mean_absolute_error(y_likes_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_likes_test, y_pred)),
                'r2': r2_score(y_likes_test, y_pred)
            }
            print(f"  MAE: {metrics['likes_random_forest']['mae']:.2f}")
            print(f"  RMSE: {metrics['likes_random_forest']['rmse']:.2f}")
            print(f"  R² Score: {metrics['likes_random_forest']['r2']:.4f}")
    
    # Train models for FOLLOWER GROWTH prediction (if data available)
    if y_growth_train is not None and len(y_growth_train[y_growth_train != 0]) > 0:
        if model_type in ['linear', 'both']:
            print("\n=== Training Linear Regression for FOLLOWER GROWTH ===")
            lr_growth = LinearRegression()
            lr_growth.fit(X_train, y_growth_train)
            models['follower_growth_linear'] = lr_growth
            
            if len(X_test) > 0 and y_growth_test is not None:
                y_pred = lr_growth.predict(X_test)
                metrics['follower_growth_linear'] = {
                    'mae': mean_absolute_error(y_growth_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_growth_test, y_pred)),
                    'r2': r2_score(y_growth_test, y_pred)
                }
                print(f"  MAE: {metrics['follower_growth_linear']['mae']:.2f}")
                print(f"  RMSE: {metrics['follower_growth_linear']['rmse']:.2f}")
                print(f"  R² Score: {metrics['follower_growth_linear']['r2']:.4f}")
        
        if model_type in ['random_forest', 'both']:
            print("\n=== Training Random Forest for FOLLOWER GROWTH ===")
            rf_growth = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            rf_growth.fit(X_train, y_growth_train)
            models['follower_growth_random_forest'] = rf_growth
            
            if len(X_test) > 0 and y_growth_test is not None:
                y_pred = rf_growth.predict(X_test)
                metrics['follower_growth_random_forest'] = {
                    'mae': mean_absolute_error(y_growth_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_growth_test, y_pred)),
                    'r2': r2_score(y_growth_test, y_pred)
                }
                print(f"  MAE: {metrics['follower_growth_random_forest']['mae']:.2f}")
                print(f"  RMSE: {metrics['follower_growth_random_forest']['rmse']:.2f}")
                print(f"  R² Score: {metrics['follower_growth_random_forest']['r2']:.4f}")
    
    return models, metrics

def train_model(df, model_type='random_forest'):
    """
    Main training function (backward compatibility)
    Returns the best model for likes prediction
    """
    models, metrics = train_models(df, model_type)
    
    # Return Random Forest for likes as default (usually better performance)
    if 'likes_random_forest' in models:
        return models['likes_random_forest']
    elif 'likes_linear' in models:
        return models['likes_linear']
    else:
        raise ValueError("No model trained successfully")

if __name__ == '__main__':
    # Example usage
    print("Enhanced ML Model Training Script")
    print("Supports both Linear Regression and Random Forest")
    print("Predicts: Likes and Follower Growth")
