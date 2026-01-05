from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import pandas as pd
from datetime import datetime
import joblib
import numpy as np
import sys
import json
import io

# Import database and auth
from models.database import db, User, Upload, Prediction, init_db
from utils.auth import generate_token, get_current_user, login_required, optional_auth

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MODEL_FOLDER = os.path.join(BASE_DIR, '..', 'ml', 'models')
DATABASE_FOLDER = os.path.join(BASE_DIR, '..', 'database')
ALLOWED_EXTENSIONS = {'csv'}

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DATABASE_FOLDER, "postpredict.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # Change in production!

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Initialize database
init_db(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def train_model_safe(df_processed, model_path):
    """Safely train model with error handling"""
    try:
        ml_path = os.path.join(BASE_DIR, '..', 'ml')
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)
        from trainings.train_model import train_model
        model = train_model(df_processed)
        joblib.dump(model, model_path)
        return model
    except Exception as e:
        raise Exception(f"Model training failed: {str(e)}")

def preprocess_data(df):
    """
    Preprocess the uploaded CSV data using advanced feature engineering
    Uses the feature_engineering module for comprehensive feature creation
    """
    try:
        # Import feature engineering module
        ml_path = os.path.join(BASE_DIR, '..', 'ml')
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)
        from trainings.feature_engineering import engineer_features
        
        # Use advanced feature engineering
        df_processed = engineer_features(df)
        return df_processed
    except ImportError:
        # Fallback to basic preprocessing if module not found
        df_processed = df.copy()
        
        # Basic date parsing
        date_columns = ['post_date', 'date', 'timestamp', 'datetime', 'created_at']
        for col in date_columns:
            if col in df_processed.columns:
                df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
                df_processed['posting_hour'] = df_processed[col].dt.hour
                df_processed['posting_day'] = df_processed[col].dt.dayofweek
                df_processed['month'] = df_processed[col].dt.month
                break
        
        # Platform encoding
        if 'platform' in df_processed.columns:
            platform_map = {'instagram': 0, 'facebook': 1, 'linkedin': 2, 'Instagram': 0, 'Facebook': 1, 'LinkedIn': 2}
            df_processed['platform_encoded'] = df_processed['platform'].str.lower().map(platform_map).fillna(0).astype(int)
        
        # Content type encoding
        if 'content_type' in df_processed.columns:
            content_map = {'image': 0, 'video': 1, 'carousel': 2, 'text': 3, 'Image': 0, 'Video': 1, 'Carousel': 2, 'Text': 3}
            df_processed['content_type_encoded'] = df_processed['content_type'].str.lower().map(content_map).fillna(0).astype(int)
        
        # Fill missing values
        numeric_cols = ['likes', 'comments', 'shares', 'followers_at_post_time', 'followers', 'caption_length', 'hashtags_count', 'hashtag_count']
        for col in numeric_cols:
            if col in df_processed.columns:
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').fillna(0).astype(int)
        
        df_processed = df_processed.replace([np.inf, -np.inf], 0)
        return df_processed

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        
        # Create user
        user = User(email=email, name=name or email.split('@')[0])
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            "message": "Registration successful",
            "token": token,
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user_info():
    """Get current user information"""
    user = get_current_user()
    return jsonify({"user": user.to_dict()}), 200

# ==================== UPLOAD ROUTES ====================

@app.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle CSV file upload"""
    user = get_current_user()
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only CSV files are allowed"}), 400
    
    try:
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and validate CSV
        df = pd.read_csv(filepath)
        
        # Check required columns
        required_cols = ['likes']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return jsonify({
                "error": f"Missing required columns: {', '.join(missing_cols)}",
                "available_columns": list(df.columns)
            }), 400
        
        # Preprocess data
        df_processed = preprocess_data(df)
        
        # Save upload to database
        upload = Upload(
            user_id=user.id,
            filename=filename,
            original_filename=file.filename,
            file_path=filepath,
            total_posts=len(df),
            columns=json.dumps(list(df.columns))
        )
        db.session.add(upload)
        db.session.commit()
        
        # Get basic stats
        stats = {
            "total_posts": len(df),
            "columns": list(df.columns),
            "preview": df.head(5).to_dict('records'),
            "upload_id": upload.id
        }
        
        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "upload_id": upload.id,
            "stats": stats
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    """Predict post performance"""
    user = get_current_user()
    
    try:
        data = request.json
        
        if 'filename' not in data and 'upload_id' not in data:
            return jsonify({"error": "Filename or upload_id required"}), 400
        
        # Get upload record
        upload_id = data.get('upload_id')
        if upload_id:
            upload = Upload.query.filter_by(id=upload_id, user_id=user.id).first()
            if not upload:
                return jsonify({"error": "Upload not found"}), 404
            filepath = upload.file_path
        else:
            filename = data['filename']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({"error": "File not found"}), 404
        
        # Load data
        df = pd.read_csv(filepath)
        df_processed = preprocess_data(df)
        
        # Load or train models (for both likes and follower growth)
        model_path_likes = os.path.join(MODEL_FOLDER, 'likes_predictor.pkl')
        model_path_growth = os.path.join(MODEL_FOLDER, 'follower_growth_predictor.pkl')
        
        # Train models if needed
        ml_path = os.path.join(BASE_DIR, '..', 'ml')
        if ml_path not in sys.path:
            sys.path.insert(0, ml_path)
        from trainings.train_model import train_models, prepare_features
        
        # Check if models exist, otherwise train
        if not os.path.exists(model_path_likes):
            models_dict, _ = train_models(df_processed, model_type='random_forest')
            if 'likes_random_forest' in models_dict:
                joblib.dump(models_dict['likes_random_forest'], model_path_likes)
            if 'follower_growth_random_forest' in models_dict:
                joblib.dump(models_dict['follower_growth_random_forest'], model_path_growth)
        
        # Load models
        try:
            model_likes = joblib.load(model_path_likes)
        except:
            models_dict, _ = train_models(df_processed, model_type='random_forest')
            model_likes = models_dict.get('likes_random_forest')
            if model_likes:
                joblib.dump(model_likes, model_path_likes)
        
        model_growth = None
        if os.path.exists(model_path_growth):
            try:
                model_growth = joblib.load(model_path_growth)
            except:
                pass
        
        # Prepare features for prediction
        available_features = prepare_features(df_processed)
        
        if len(available_features) == 0:
            return jsonify({"error": "No valid features found in data"}), 400
        
        X = df_processed[available_features].fillna(0)
        X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
        X = X.replace([np.inf, -np.inf], 0)
        
        # Make predictions for LIKES
        try:
            predictions_likes = model_likes.predict(X)
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
        
        # Make predictions for FOLLOWER GROWTH (if model available)
        predictions_growth = None
        if model_growth:
            try:
                predictions_growth = model_growth.predict(X)
            except:
                pass
        
        # Calculate statistics for LIKES
        avg_predicted_likes = float(np.mean(predictions_likes))
        max_predicted_likes = float(np.max(predictions_likes))
        min_predicted_likes = float(np.min(predictions_likes))
        
        # Calculate statistics for FOLLOWER GROWTH
        avg_predicted_growth = float(np.mean(predictions_growth)) if predictions_growth is not None else None
        max_predicted_growth = float(np.max(predictions_growth)) if predictions_growth is not None else None
        min_predicted_growth = float(np.min(predictions_growth)) if predictions_growth is not None else None
        
        # Get best posting time
        hour_col = 'posting_hour' if 'posting_hour' in df_processed.columns else ('hour' if 'hour' in df_processed.columns else None)
        if hour_col:
            df_processed['predicted_likes'] = predictions_likes
            best_hour = int(df_processed.groupby(hour_col)['predicted_likes'].mean().idxmax())
        else:
            best_hour = None
        
        # Platform analysis
        platform_analysis = {}
        if 'platform' in df_processed.columns:
            for platform in df_processed['platform'].unique():
                platform_data = df_processed[df_processed['platform'] == platform]
                platform_analysis[platform] = {
                    "avg_predicted_likes": float(np.mean(predictions_likes[df_processed['platform'] == platform])),
                    "post_count": int(len(platform_data))
                }
        
        # Save prediction to database
        prediction = Prediction(
            user_id=user.id,
            upload_id=upload_id if upload_id else None,
            average_likes=avg_predicted_likes,
            max_likes=max_predicted_likes,
            min_likes=min_predicted_likes,
            best_posting_hour=best_hour,
            platform_analysis=json.dumps(platform_analysis),
            total_posts_analyzed=len(df)
        )
        db.session.add(prediction)
        db.session.commit()
        
        # Prepare response with both likes and follower growth
        response_data = {
            "predictions": {
                "likes": {
                    "average": avg_predicted_likes,
                    "max": max_predicted_likes,
                    "min": min_predicted_likes
                },
                "follower_growth": {
                    "average": avg_predicted_growth,
                    "max": max_predicted_growth,
                    "min": min_predicted_growth
                } if avg_predicted_growth is not None else None,
                "best_posting_hour": best_hour
            },
            "platform_analysis": platform_analysis,
            "total_posts_analyzed": len(df),
            "prediction_id": prediction.id
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

# ==================== DASHBOARD ROUTES ====================

@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    """Get user dashboard data"""
    user = get_current_user()
    
    try:
        # Get user's predictions
        predictions = Prediction.query.filter_by(user_id=user.id).order_by(Prediction.created_at.desc()).all()
        uploads = Upload.query.filter_by(user_id=user.id).order_by(Upload.created_at.desc()).all()
        
        # Calculate statistics
        total_predictions = len(predictions)
        avg_likes = np.mean([p.average_likes for p in predictions]) if predictions else 0
        
        # Get best posting time from most recent prediction
        best_time = None
        if predictions:
            best_time = predictions[0].best_posting_hour
        
        # Platform breakdown
        platform_counts = {}
        for pred in predictions:
            if pred.platform_analysis:
                platforms = json.loads(pred.platform_analysis)
                for platform in platforms.keys():
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return jsonify({
            "stats": {
                "total_predictions": total_predictions,
                "avg_likes": float(avg_likes),
                "best_time": best_time,
                "platforms_count": len(platform_counts)
            },
            "recent_predictions": [p.to_dict() for p in predictions[:5]],
            "recent_uploads": [u.to_dict() for u in uploads[:5]],
            "platform_breakdown": platform_counts
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error fetching dashboard: {str(e)}"}), 500

@app.route('/api/predictions', methods=['GET'])
@login_required
def get_predictions():
    """Get all user predictions"""
    user = get_current_user()
    
    try:
        predictions = Prediction.query.filter_by(user_id=user.id).order_by(Prediction.created_at.desc()).all()
        return jsonify({
            "predictions": [p.to_dict() for p in predictions]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching predictions: {str(e)}"}), 500

@app.route('/api/predictions/<int:prediction_id>', methods=['GET'])
@login_required
def get_prediction(prediction_id):
    """Get specific prediction"""
    user = get_current_user()
    
    try:
        prediction = Prediction.query.filter_by(id=prediction_id, user_id=user.id).first()
        if not prediction:
            return jsonify({"error": "Prediction not found"}), 404
        
        return jsonify(prediction.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching prediction: {str(e)}"}), 500

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    return jsonify({"message": "Social Media Post Performance Prediction API"})

@app.route('/api/sample-csv', methods=['GET'])
def get_sample_csv():
    """Generate and return a sample CSV file"""
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
    platforms = np.random.choice(['Instagram', 'Facebook', 'LinkedIn'], 50)
    content_types = np.random.choice(['Image', 'Video', 'Text'], 50)
    
    sample_data = {
        'date': dates,
        'platform': platforms,
        'content_type': content_types,
        'caption': [f"Sample caption {i}" for i in range(50)],
        'hashtags': [f"#tag{i} #social #media" for i in range(50)],
        'likes': np.random.randint(50, 1000, 50),
        'comments': np.random.randint(5, 100, 50),
        'shares': np.random.randint(0, 50, 50),
        'followers': np.random.randint(1000, 10000, 50)
    }
    
    df = pd.DataFrame(sample_data)
    df['caption_length'] = df['caption'].str.len()
    df['hashtag_count'] = df['hashtags'].str.count('#')
    
    # Convert to CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=sample_data.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
