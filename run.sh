#!/bin/bash

# Script to run the Social Media Post Performance Prediction System

echo "🚀 Starting Social Media Post Performance Prediction System"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "venv" ] && [ ! -d "env" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start backend server
echo "🔧 Starting backend server on http://localhost:5000"
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "🌐 Starting frontend server on http://localhost:8000"
cd frontend/public
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ../..

echo ""
echo "✅ Servers started!"
echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

