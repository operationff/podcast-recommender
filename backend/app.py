from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from podcast_data import search_podcasts, get_all_podcasts
from linkedin_scraper import extract_profile_data, analyze_profile_for_podcasts

app = Flask(__name__)

# Configure CORS for production
if os.environ.get('FLASK_ENV') == 'production':
    # In production, only allow requests from your frontend domain
    CORS(app, resources={
        r"/api/*": {
            "origins": os.environ.get('ALLOWED_ORIGINS', '').split(','),
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"]
        }
    })
else:
    # In development, allow all origins
    CORS(app)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

def get_podcast_recommendations(linkedin_url, wants_to_be_featured):
    """Get podcast recommendations based on LinkedIn profile."""
    try:
        # Extract and analyze LinkedIn profile data
        profile_data = extract_profile_data(linkedin_url)
        analysis = analyze_profile_for_podcasts(profile_data, wants_to_be_featured)
        
        # Get all available podcasts
        all_podcasts = get_all_podcasts()
        
        # Score podcasts based on profile analysis
        scored_podcasts = []
        for podcast in all_podcasts:
            score = 0
            reasons = []
            
            # Score based on keywords from profile
            matching_keywords = []
            for keyword in analysis['keywords']:
                keyword_lower = keyword.lower()
                if keyword_lower in podcast['title'].lower():
                    score += 3
                    matching_keywords.append(keyword)
                elif keyword_lower in podcast['description'].lower():
                    score += 2
                    matching_keywords.append(keyword)
            if matching_keywords:
                reasons.append(f"Matches your expertise in: {', '.join(matching_keywords)}")
            
            # Score based on categories
            matching_categories = []
            for category in analysis['categories']:
                category_lower = category.lower()
                if category_lower in podcast['title'].lower():
                    score += 3
                    matching_categories.append(category)
                elif category_lower in podcast['description'].lower():
                    score += 2
                    matching_categories.append(category)
                elif any(category_lower in pc.lower() for pc in podcast['categories']):
                    score += 2
                    matching_categories.append(category)
            if matching_categories:
                reasons.append(f"Aligns with your interests in: {', '.join(set(matching_categories))}")
            
            # Add bonus points for featured opportunities if user wants to be featured
            if wants_to_be_featured:
                matching_opportunities = []
                for opportunity in analysis['featured_opportunities']:
                    if opportunity.lower() in podcast['title'].lower() or \
                       opportunity.lower() in podcast['description'].lower():
                        score += 4
                        matching_opportunities.append(opportunity)
                if matching_opportunities:
                    reasons.append("Perfect for guest appearances based on your profile")
            
            # Add bonus points for top-rated and featured podcasts
            if 'Top Rated' in podcast['categories']:
                score += 3
                reasons.append("Highly rated by listeners")
            if 'Featured' in podcast['categories']:
                score += 2
                reasons.append("Featured podcast")
            
            if score > 0:  # Only include podcasts with some relevance
                scored_podcasts.append((score, podcast, reasons))
        
        # Sort by score and get top 10
        scored_podcasts.sort(key=lambda x: x[0], reverse=True)
        recommendations = [
            {
                'title': p['title'],
                'description': p['description'],
                'image': p['image'],
                'website': p['website'],
                'categories': p['categories'],
                'reasons': reasons
            }
            for _, p, reasons in scored_podcasts[:10]
        ]
        
        return recommendations
    
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        return []

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Endpoint to get podcast recommendations based on LinkedIn profile."""
    try:
        data = request.json
        if not data or 'linkedinUrl' not in data:
            return jsonify({'error': 'LinkedIn URL is required'}), 400

        linkedin_url = data['linkedinUrl']
        wants_to_be_featured = data.get('wantsToBeFeatured', False)

        # Get recommendations and profile analysis
        recommendations = get_podcast_recommendations(linkedin_url, wants_to_be_featured)
        
        # Get profile data for display
        profile_data = extract_profile_data(linkedin_url)
        analysis = analyze_profile_for_podcasts(profile_data, wants_to_be_featured)
        
        return jsonify({
            'recommendations': recommendations,
            'profile': {
                'summary': profile_data['summary'],
                'skills': profile_data['skills'][:5],  # Top 5 skills
                'interests': profile_data['interests'],
                'featuredOpportunities': analysis['featured_opportunities'] if wants_to_be_featured else []
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file."""
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_ENV') != 'production'
    )
