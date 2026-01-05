"""
Advanced Feature Engineering for Social Media Post Performance Prediction
"""
import pandas as pd
import numpy as np
from datetime import datetime

def engineer_features(df):
    """
    Perform advanced feature engineering on social media post data
    
    Args:
        df: DataFrame with raw social media post data
        
    Returns:
        DataFrame with engineered features
    """
    df_processed = df.copy()
    
    # ========== DATE/TIME FEATURES ==========
    # Parse post_date and post_time
    date_col = None
    for col in ['post_date', 'date', 'timestamp', 'datetime', 'created_at']:
        if col in df_processed.columns:
            date_col = col
            break
    
    if date_col:
        df_processed[date_col] = pd.to_datetime(df_processed[date_col], errors='coerce')
        
        # Extract time features
        df_processed['posting_hour'] = df_processed[date_col].dt.hour
        df_processed['posting_day'] = df_processed[date_col].dt.dayofweek  # 0=Monday, 6=Sunday
        df_processed['month'] = df_processed[date_col].dt.month
        df_processed['day_of_month'] = df_processed[date_col].dt.day
        df_processed['is_weekend'] = (df_processed['posting_day'] >= 5).astype(int)
    
    # If separate post_time column exists
    if 'post_time' in df_processed.columns:
        try:
            time_parts = df_processed['post_time'].astype(str).str.split(':')
            df_processed['posting_hour'] = time_parts.str[0].astype(int)
        except:
            pass
    
    # ========== PLATFORM ENCODING ==========
    if 'platform' in df_processed.columns:
        platform_map = {
            'instagram': 0,
            'facebook': 1,
            'linkedin': 2,
            'Instagram': 0,
            'Facebook': 1,
            'LinkedIn': 2
        }
        df_processed['platform_encoded'] = df_processed['platform'].str.lower().map(platform_map).fillna(0).astype(int)
    
    # ========== CONTENT TYPE ENCODING ==========
    if 'content_type' in df_processed.columns:
        content_map = {
            'image': 0,
            'video': 1,
            'carousel': 2,
            'text': 3,
            'Image': 0,
            'Video': 1,
            'Carousel': 2,
            'Text': 3
        }
        df_processed['content_type_encoded'] = df_processed['content_type'].str.lower().map(content_map).fillna(0).astype(int)
    
    # ========== CAPTION FEATURES ==========
    if 'caption_length' not in df_processed.columns:
        if 'caption' in df_processed.columns:
            df_processed['caption_length'] = df_processed['caption'].astype(str).str.len()
        else:
            df_processed['caption_length'] = 0
    
    # ========== HASHTAG FEATURES ==========
    if 'hashtags_count' not in df_processed.columns:
        if 'hashtags' in df_processed.columns:
            df_processed['hashtags_count'] = df_processed['hashtags'].astype(str).str.count('#')
        elif 'hashtag_count' in df_processed.columns:
            df_processed['hashtags_count'] = df_processed['hashtag_count']
        else:
            df_processed['hashtags_count'] = 0
    
    # ========== ENGAGEMENT FEATURES ==========
    # Calculate engagement rate
    if 'followers_at_post_time' in df_processed.columns:
        followers_col = 'followers_at_post_time'
    elif 'followers' in df_processed.columns:
        followers_col = 'followers'
    else:
        followers_col = None
    
    if followers_col:
        # Engagement rate = (likes + comments + shares) / followers
        total_engagement = (
            df_processed.get('likes', 0) + 
            df_processed.get('comments', 0) + 
            df_processed.get('shares', 0)
        )
        df_processed['engagement_rate'] = np.where(
            df_processed[followers_col] > 0,
            total_engagement / df_processed[followers_col],
            0
        )
        df_processed['engagement_rate'] = df_processed['engagement_rate'].fillna(0)
    else:
        df_processed['engagement_rate'] = 0
    
    # ========== ROLLING AVERAGES ==========
    # Sort by date for rolling calculations
    if date_col and len(df_processed) > 1:
        df_processed = df_processed.sort_values(date_col).reset_index(drop=True)
        
        # Rolling average of likes (7-day window)
        if 'likes' in df_processed.columns:
            df_processed['rolling_avg_likes'] = df_processed['likes'].rolling(
                window=min(7, len(df_processed)), 
                min_periods=1
            ).mean().fillna(df_processed['likes'].mean() if 'likes' in df_processed.columns else 0)
        
        # Rolling average of engagement rate
        df_processed['rolling_avg_engagement'] = df_processed['engagement_rate'].rolling(
            window=min(7, len(df_processed)),
            min_periods=1
        ).mean().fillna(0)
        
        # Calculate follower growth
        if followers_col:
            df_processed['follower_growth'] = df_processed[followers_col].diff().fillna(0)
    else:
        if 'likes' in df_processed.columns:
            df_processed['rolling_avg_likes'] = df_processed['likes'].mean()
        else:
            df_processed['rolling_avg_likes'] = 0
        df_processed['rolling_avg_engagement'] = 0
        df_processed['follower_growth'] = 0
    
    # ========== INTERACTION FEATURES ==========
    # Platform x Content Type interaction
    if 'platform_encoded' in df_processed.columns and 'content_type_encoded' in df_processed.columns:
        df_processed['platform_content_interaction'] = (
            df_processed['platform_encoded'] * 10 + df_processed['content_type_encoded']
        )
    
    # Time x Platform interaction
    if 'posting_hour' in df_processed.columns and 'platform_encoded' in df_processed.columns:
        df_processed['hour_platform_interaction'] = (
            df_processed['posting_hour'] * 10 + df_processed['platform_encoded']
        )
    
    # ========== NORMALIZE NUMERIC FEATURES ==========
    # Fill missing values
    numeric_cols = ['likes', 'comments', 'shares', 'caption_length', 'hashtags_count']
    for col in numeric_cols:
        if col in df_processed.columns:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').fillna(0).astype(int)
    
    if followers_col:
        df_processed[followers_col] = pd.to_numeric(df_processed[followers_col], errors='coerce').fillna(0).astype(int)
    
    # Replace infinite values
    df_processed = df_processed.replace([np.inf, -np.inf], 0)
    
    return df_processed

