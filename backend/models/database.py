"""
Database models and initialization
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    uploads = db.relationship('Upload', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Upload(db.Model):
    """Upload model for tracking file uploads"""
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    total_posts = db.Column(db.Integer, nullable=False)
    columns = db.Column(db.Text)  # JSON string of columns
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='upload', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert upload to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'total_posts': self.total_posts,
            'columns': json.loads(self.columns) if self.columns else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Prediction(db.Model):
    """Prediction model for storing prediction results"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id'), nullable=True)
    
    # Prediction results
    average_likes = db.Column(db.Float, nullable=False)
    max_likes = db.Column(db.Float, nullable=False)
    min_likes = db.Column(db.Float, nullable=False)
    best_posting_hour = db.Column(db.Integer, nullable=True)
    
    # Platform analysis (JSON)
    platform_analysis = db.Column(db.Text)  # JSON string
    
    # Metadata
    total_posts_analyzed = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'upload_id': self.upload_id,
            'predictions': {
                'average_likes': self.average_likes,
                'max_likes': self.max_likes,
                'min_likes': self.min_likes,
                'best_posting_hour': self.best_posting_hour
            },
            'platform_analysis': json.loads(self.platform_analysis) if self.platform_analysis else {},
            'total_posts_analyzed': self.total_posts_analyzed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def init_db(app):
    """Initialize database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Create admin user if doesn't exist
        admin = User.query.filter_by(email='admin@postpredict.com').first()
        if not admin:
            admin = User(email='admin@postpredict.com', name='Admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

