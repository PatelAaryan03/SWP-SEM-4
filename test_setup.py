#!/usr/bin/env python3
"""
Simple test script to verify the setup
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import flask
        print("✅ Flask installed")
    except ImportError:
        print("❌ Flask not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import flask_cors
        print("✅ flask-cors installed")
    except ImportError:
        print("❌ flask-cors not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import pandas
        print("✅ pandas installed")
    except ImportError:
        print("❌ pandas not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import numpy
        print("✅ numpy installed")
    except ImportError:
        print("❌ numpy not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn installed")
    except ImportError:
        print("❌ scikit-learn not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import joblib
        print("✅ joblib installed")
    except ImportError:
        print("❌ joblib not installed. Run: pip install -r requirements.txt")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    dirs = [
        'backend',
        'backend/uploads',
        'frontend',
        'frontend/public',
        'frontend/src',
        'frontend/src/css',
        'frontend/src/js',
        'ml',
        'ml/models',
        'ml/data'
    ]
    
    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"❌ {dir_path} missing")
            all_exist = False
    
    return all_exist

def test_files():
    """Test if required files exist"""
    print("\nTesting files...")
    files = [
        'backend/app.py',
        'frontend/public/index.html',
        'frontend/src/css/styles.css',
        'frontend/src/js/app.js',
        'ml/trainings/train_model.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

if __name__ == '__main__':
    print("=" * 50)
    print("Social Media Post Performance Prediction System")
    print("Setup Verification Test")
    print("=" * 50)
    
    imports_ok = test_imports()
    dirs_ok = test_directories()
    files_ok = test_files()
    
    print("\n" + "=" * 50)
    if imports_ok and dirs_ok and files_ok:
        print("✅ All tests passed! Setup looks good.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

