# LinkedIn-Based Podcast Recommender

A modern web application that provides personalized podcast recommendations based on LinkedIn profiles. The app analyzes your professional background and interests to suggest relevant podcasts and identifies potential speaking opportunities if you're interested in being featured as a guest.

## Features
- LinkedIn profile analysis for personalized recommendations
- Smart podcast matching based on skills and interests
- Guest speaker opportunity suggestions
- Modern, responsive UI with Tailwind CSS
- RESTful Flask backend

## Local Development Setup

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the development server:
   ```bash
   python app.py
   ```
   The server will start at http://localhost:5002

### Frontend
The frontend is a static HTML/JavaScript application using Tailwind CSS. Simply open `frontend/index.html` in your browser or serve it using a static file server.

## Deployment

### Deployment with Render.com

#### Option 1: Automatic Deployment (Recommended)
1. Fork this repository to your GitHub account
2. Sign up for a [Render.com](https://render.com) account if you haven't already
3. Click the Deploy to Render button below:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

This will automatically:
- Deploy the backend API service
- Deploy the frontend static site
- Configure all necessary environment variables
- Set up automatic deployments on future commits

#### Option 2: Manual Deployment
If you prefer to set up the services manually:

1. Backend API Service:
   ```bash
   # On render.com:
   1. Create a new Web Service
   2. Connect your GitHub repository
   3. Use these settings:
      - Name: podcast-recommender-api
      - Environment: Python
      - Build Command: cd backend && pip install -r requirements.txt
      - Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
      - Environment Variables:
        FLASK_ENV=production
        PYTHON_VERSION=3.9.0
   ```

2. Frontend Static Site:
   ```bash
   # On render.com:
   1. Create a new Static Site
   2. Connect your GitHub repository
   3. Use these settings:
      - Name: podcast-recommender-frontend
      - Build Command: (leave empty)
      - Publish Directory: frontend
   ```

3. Configure CORS:
   - After deployment, get your frontend URL from Render
   - Add it to the backend's environment variables:
     ```
     ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
     ```

#### Post-Deployment
- Backend API will be available at: `https://podcast-recommender-api.onrender.com`
- Frontend will be available at: `https://podcast-recommender-frontend.onrender.com`
- Monitor your deployments in the Render dashboard
- Set up automatic deployments from your GitHub repository

## Architecture
- **Backend**: Python Flask application with:
  - LinkedIn profile analysis
  - Podcast recommendation engine
  - CORS and security headers for production
  - Gunicorn WSGI server

- **Frontend**: Static HTML/JS with:
  - Tailwind CSS for styling
  - Responsive design
  - Dynamic profile preview
  - Real-time LinkedIn URL validation

## Security Features
- Input validation for LinkedIn URLs
- CORS configuration for production
- Security headers (XSS Protection, HSTS, etc.)
- Environment-based configurations

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
