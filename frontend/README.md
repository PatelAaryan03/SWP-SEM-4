# Frontend Module

Modern, responsive web interface for the Social Media Performance Predictor built with HTML, CSS, and JavaScript.

## 📁 Folder Structure

```
frontend/
├── public/                 # Public HTML files
│   ├── index.html          # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── upload.html         # CSV upload page
│   ├── dashboard.html      # Analytics dashboard
│   ├── results.html        # Prediction results
│   ├── about.html          # Features & information
│   └── assets/             # Static assets
├── src/
│   ├── css/                # Stylesheets
│   │   ├── base.css        # Shared/base styles
│   │   ├── home.css        # Home page styles
│   │   ├── login.css       # Login/register styles
│   │   ├── upload.css      # Upload page styles
│   │   ├── dashboard.css   # Dashboard styles
│   │   ├── results.css     # Results page styles
│   │   └── about.css       # About page styles
│   └── js/                 # JavaScript files
│       ├── config.js       # Configuration
│       ├── auth.js         # Authentication utilities
│       ├── navigation.js  # Navigation handling
│       ├── upload.js       # File upload logic
│       ├── dashboard.js    # Dashboard data loading
│       ├── results.js      # Results display
│       └── login.js        # Login form handling
└── README.md               # This file
```

## 🎯 Purpose

The frontend provides:
1. **User Interface** for interacting with the prediction system
2. **File Upload** with drag & drop support
3. **Authentication** pages (login/register)
4. **Dashboard** for viewing analytics
5. **Results Display** for prediction outcomes
6. **Responsive Design** for all devices

## 🎨 Design Features

### Theme
- **Dark Theme**: Modern dark color scheme
- **Color Palette**: 
  - Primary: `#4a9eff` (Blue)
  - Background: `#0e0e0e` (Dark)
  - Cards: `#1a1a1a` (Dark Gray)
  - Text: `#ffffff` (White)

### Components
- **Navigation Bar**: Sticky header with logo and menu
- **Cards**: Hover effects and shadows
- **Forms**: Clean input fields with validation
- **Buttons**: Primary and secondary styles
- **Progress Bars**: For upload progress
- **Error Messages**: User-friendly error display

## 📄 Pages

### 1. Landing Page (`index.html`)
- Hero section with call-to-action
- Feature cards explaining platform capabilities
- How it works section
- Responsive grid layout

### 2. Login Page (`login.html`)
- Email/password login form
- Social login buttons (UI only)
- Link to registration
- Error message display

### 3. Register Page (`register.html`)
- User registration form
- Password confirmation
- Validation feedback
- Link to login

### 4. Upload Page (`upload.html`)
- Drag & drop file upload area
- File selection and preview
- CSV requirements display
- Progress indicator
- Sample CSV download

### 5. Dashboard (`dashboard.html`)
- Statistics cards (Total Predictions, Avg Likes, Best Time)
- Platform performance breakdown
- Recent predictions list
- Quick action cards

### 6. Results Page (`results.html`)
- Main prediction cards (Average, Max, Min)
- Best posting time display
- Platform analysis
- Summary statistics

### 7. About Page (`about.html`)
- Project overview
- Feature descriptions
- How it works steps
- Technologies used

## 🔧 JavaScript Modules

### `config.js`
Centralized configuration:
- API base URL
- File size limits
- Supported file types

### `auth.js`
Authentication utilities:
- Token management (localStorage)
- Login/register functions
- API request with auth headers
- Navigation updates

### `upload.js`
File upload handling:
- Drag & drop support
- File validation
- Progress tracking
- API communication

### `dashboard.js`
Dashboard data loading:
- Fetch user statistics
- Display platform breakdown
- Show recent predictions
- Handle empty states

### `results.js`
Results display:
- Load prediction data
- Display metrics
- Platform analysis
- Format data for display

## 🚀 Running the Frontend

### Option 1: Simple HTTP Server (Recommended)
```bash
cd frontend/public
python -m http.server 8000
# Visit http://localhost:8000
```

### Option 2: Node.js HTTP Server
```bash
cd frontend/public
npx http-server -p 8000
```

### Option 3: Direct File Access
Open `frontend/public/index.html` directly in browser
(Note: Some features may not work due to CORS)

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 968px (Full layout)
- **Tablet**: 768px - 968px (Adjusted grid)
- **Mobile**: < 768px (Single column, stacked)

### Mobile Optimizations
- Stacked navigation
- Single column layouts
- Touch-friendly buttons
- Optimized font sizes

## 🎯 User Flow

1. **Landing** → View features and information
2. **Register/Login** → Create account or sign in
3. **Upload** → Upload CSV with social media data
4. **Predict** → System analyzes and predicts
5. **Dashboard** → View statistics and history
6. **Results** → See detailed predictions

## 🔐 Authentication Integration

- **Token Storage**: localStorage
- **Auto-redirect**: Unauthenticated users → login
- **Token Refresh**: Automatic on API calls
- **Logout**: Clear tokens and redirect

## 📊 API Integration

All API calls use:
- **Base URL**: `http://localhost:5000/api`
- **Authentication**: Bearer token in headers
- **Error Handling**: User-friendly messages
- **Loading States**: Progress indicators

## 🎨 CSS Architecture

### Base Styles (`base.css`)
- Reset and normalization
- Typography
- Navigation
- Footer
- Common components
- Responsive utilities

### Page-Specific Styles
Each page has its own CSS file for:
- Layout
- Component styling
- Animations
- Page-specific features

## 🔍 Browser Support

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📝 Code Quality

- **Semantic HTML**: Proper element usage
- **CSS Organization**: Modular stylesheets
- **JavaScript**: ES6+ features
- **Comments**: Clear code documentation
- **Error Handling**: Comprehensive try-catch

## 🚨 Important Notes

1. **CORS**: Backend must have CORS enabled
2. **API URL**: Update `config.js` if backend URL changes
3. **Authentication**: Tokens expire after 24 hours
4. **File Upload**: Maximum 16MB file size
5. **Browser Console**: Check for errors during development

---

**Status**: Production-ready frontend with authentication, responsive design, and complete user flow.
