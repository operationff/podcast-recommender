# Podcast Recommender API

A Flask-based REST API that provides personalized podcast recommendations based on LinkedIn profiles.

## Features

- LinkedIn profile analysis
- Personalized podcast recommendations
- Rate limiting and caching
- Health monitoring endpoint

## Deployment Instructions

### Prerequisites

- Python 3.11.7
- GitHub account
- Render account (free tier available)

### Quick Start

1. Create a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/podcast-recommender.git
   git push -u origin main
   ```

2. Fork the repository on GitHub:
   - Go to your GitHub repository
   - Click the 'Fork' button
   - Select your account as the destination

### Environment Variables

Set the following environment variables:

```
FLASK_ENV=production
ALLOWED_ORIGINS=https://your-frontend-domain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://user:password@host:port
SENTRY_DSN=your-sentry-dsn  # Optional, for error tracking
```

### Deployment Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/podcast-recommender.git
   cd podcast-recommender/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   flask db upgrade
   ```

4. Start the application:
   ```bash
   gunicorn app:app --workers=4 --worker-class=gevent
   ```

### Deployment Platforms

#### Render (Recommended)

1. Create a new Web Service on Render:
   - Go to [render.com](https://render.com) and sign up/login
   - From your dashboard, click 'New +' and select 'Web Service'
   - Find and select your GitHub repository
   - You might need to configure GitHub permissions if this is your first time

2. Configure the service:
   - Name: `podcast-recommender-api` (or your preferred name)
   - Environment: `Python`
   - Region: Choose the closest to your users
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --workers=4 --worker-class=gevent --bind=0.0.0.0:$PORT --timeout=30`

3. Set environment variables:
   ```
   FLASK_ENV=production
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

4. Deploy:
   - Click 'Create Web Service'
   - Render will automatically build and deploy your application
   - Monitor the deployment logs for any issues

5. Access your API:
   - Once deployed, your API will be available at `https://your-service-name.onrender.com`
   - Test the health endpoint at `https://your-service-name.onrender.com/api/health`

#### Alternative Deployment Options

##### Docker

1. Build the image:
   ```bash
   docker build -t podcast-recommender .
   ```

2. Run the container:
   ```bash
   docker run -p 5002:5002 podcast-recommender
   ```

##### Manual Deployment

1. Set up a server with Python 3.11.7
2. Clone and install dependencies:
   ```bash
   git clone https://github.com/your-username/podcast-recommender.git
   cd podcast-recommender/backend
   pip install -r requirements.txt
   ```
3. Configure environment variables
4. Start with gunicorn:
   ```bash
   gunicorn app:app --workers=4 --worker-class=gevent
   ```

## API Documentation

### Endpoints

#### POST /api/recommend
Get podcast recommendations based on LinkedIn profile.

Request:
```json
{
    "linkedinUrl": "https://www.linkedin.com/in/username",
    "wantsToBeFeatured": false
}
```

Response:
```json
{
    "recommendations": [
        {
            "title": "Podcast Title",
            "description": "Description",
            "image": "image_url",
            "website": "website_url",
            "categories": ["category1", "category2"],
            "reasons": ["reason1", "reason2"]
        }
    ],
    "profile": {
        "summary": "Profile summary",
        "skills": ["skill1", "skill2"],
        "interests": ["interest1", "interest2"]
    }
}
```

#### GET /api/health
Check API health status.

Response:
```json
{
    "status": "healthy",
    "timestamp": 1234567890,
    "caches": {
        "profile_cache": {
            "size": 10,
            "maxsize": 100,
            "ttl": 3600
        },
        "podcast_cache": {
            "size": 50,
            "maxsize": 1000,
            "ttl": 86400
        }
    },
    "rate_limits": {
        "recommend": "10 per minute",
        "global": ["200 per day", "50 per hour"]
    }
}
```

## Monitoring and Maintenance

- Monitor application logs through your deployment platform
- Use Sentry for error tracking
- Check /api/health endpoint for system status
- Monitor cache and rate limit statistics

## Security

- CORS is configured for production
- Rate limiting is enabled
- Security headers are set
- Input validation for LinkedIn URLs
