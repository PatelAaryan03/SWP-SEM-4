# Setup Instructions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser

## Installation Steps

### 1. Install Python Dependencies

Navigate to the project root directory and install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server

From the project root directory, run:

```bash
cd backend
python app.py
```

The backend server will start on `http://localhost:5000`

### 3. Open the Frontend

You have two options:

#### Option A: Using a Simple HTTP Server (Recommended)

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend/public
python -m http.server 8000
```

Then open your browser and go to: `http://localhost:8000`

#### Option B: Direct File Access

Simply open `frontend/public/index.html` in your web browser.

**Note:** If you use Option B, you may need to configure CORS or use a browser extension to allow local file access to APIs.

## Usage

1. **Upload CSV File**: Click on "📂 Upload CSV File" and select a CSV file with your social media post data.

2. **CSV Format**: Your CSV should include columns like:
   - `date` or `post_date` (date/time of post)
   - `platform` (Instagram, Facebook, LinkedIn)
   - `content_type` (Image, Video, Text)
   - `caption` (post caption text)
   - `hashtags` (hashtags used)
   - `likes` (number of likes)
   - `comments` (number of comments)
   - `shares` (number of shares)
   - `followers` (follower count at time of posting)

3. **View Predictions**: After uploading, the system will automatically analyze your data and display:
   - Average predicted likes
   - Maximum and minimum predicted likes
   - Best posting time
   - Platform-specific analysis

4. **Sample Data**: Click on "Sample CSV" in the navigation to download a sample CSV file for testing.

## Project Structure

```
SWP-SEM-4/
├── backend/
│   ├── app.py              # Flask API server
│   ├── models/             # Data models
│   ├── routes/             # API routes
│   ├── uploads/            # Uploaded CSV files
│   └── utils/              # Utility functions
├── frontend/
│   ├── public/
│   │   └── index.html      # Main HTML file
│   └── src/
│       ├── css/
│       │   └── styles.css  # Styling
│       └── js/
│           └── app.js      # Frontend JavaScript
├── ml/
│   ├── data/               # Sample data
│   ├── models/             # Trained ML models
│   ├── notebooks/          # Jupyter notebooks
│   └── trainings/
│       └── train_model.py  # Model training script
└── requirements.txt        # Python dependencies
```

## API Endpoints

- `GET /` - API information
- `POST /api/upload` - Upload CSV file
- `POST /api/predict` - Get predictions for uploaded data
- `GET /api/sample-csv` - Download sample CSV file

## Troubleshooting

### Backend won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is already in use
- Verify Python version: `python --version` (should be 3.8+)

### Frontend can't connect to backend
- Ensure the backend server is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify the API_BASE_URL in `frontend/src/js/app.js`

### CSV upload fails
- Check that your CSV has the required columns (at minimum: `likes`)
- Ensure the file is a valid CSV format
- Check file size (max 16MB)

## Development

To modify the machine learning model, edit `ml/trainings/train_model.py`.

To modify the frontend, edit files in `frontend/src/`.

To modify the API, edit `backend/app.py`.

